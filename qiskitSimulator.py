#
# Copyright (c) 2017, Stephanie Wehner and Axel Dahlberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by Stephanie Wehner, QuTech.
# 4. Neither the name of the QuTech organization nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from typing import List

from qiskit.circuit import Qubit

try:
    from qiskit import QuantumCircuit, Aer, execute, QuantumRegister, ClassicalRegister
except ImportError:
    raise RuntimeError("If you want to use the qiskit backend you need to install the python package 'qiskit'")
import numpy as np

from simulaqron.virtNode.basics import quantumEngine, quantumError, noQubitError


def run_and_get_results(qc: QuantumCircuit):
    qc.measure_all()
    simulator = Aer.get_backend('statevector_simulator')
    job = execute(qc, simulator)
    result = job.result()
    return result.get_statevector()


class qiskitQEngine(quantumEngine):
    """
    Basic quantum engine which uses Qiskit.

    Attributes:
        maxQubits:	maximum number of qubits this engine will support.
    """

    qRegister: QuantumRegister
    cRegister: ClassicalRegister
    activeQubits: int
    qc: QuantumCircuit

    def __init__(self, node, num, maxQubits=10):
        """
        Initialize the simple engine. If no number is given for maxQubits, the assumption will be 10.
        """

        super().__init__(node=node, num=num, maxQubits=maxQubits)

        # We start with no active qubits
        self.activeQubits = 0

        self.qRegister = QuantumRegister(maxQubits)
        self.cRegister = ClassicalRegister(maxQubits)
        self.qc = QuantumCircuit(self.qRegister, self.cRegister)

    def add_fresh_qubit(self):
        """
        Add a new qubit initialized in the \|0\> state.
        """
        # Check if we are still allowed to add qubits
        if self.activeQubits >= self.maxQubits:
            raise noQubitError("No more qubits available in register.")

        num = self.activeQubits
        self.activeQubits += 1

        return num

    def add_qubit(self, newQubit):
        """
        Add new qubit in the state described by the vector newQubit ([a, b])
        """

        norm = np.dot(np.array(newQubit), np.array(newQubit).conj())
        if not norm <= 1:
            raise quantumError("State {} is not normalized.".format(newQubit))

        # Create a fresh qubit
        num = self.add_fresh_qubit()

        qubit_register = QuantumRegister(1)
        init_circuit = QuantumCircuit(qubit_register, name="initializer_circ")
        init_circuit.initialize(newQubit, qubit_register)

        self.qc.append(init_circuit, [self.cRegister[num]])

        return num

    def remove_qubit(self, qubitNum):
        """
        Removes the qubit with the desired number qubitNum
        """
        if (qubitNum + 1) > self.activeQubits:
            raise quantumError("No such qubit to remove")

        self.measure_qubit(qubitNum)

    def get_register_RI(self):
        """
        Retrieves the entire register in real and imaginary parts and returns the result as a
        list. Twisted only likes to send real valued lists, not complex ones.
        """
        state = run_and_get_results(self.qc)

        Re = tuple(n.real for n in state)
        Im = tuple(n.imag for n in state)

        return Re, Im

    def apply_sub_circuit(self, sub_qc: QuantumCircuit, qubit_number: int):
        self.qc.append(sub_qc, [self.qRegister[qubit_number]])

    def apply_H(self, qubitNum):
        """
        Applies a Hadamard gate to the qubits with number qubitNum.
        """

        self.qc.h(qubitNum)

    def apply_K(self, qubitNum):
        """
        Applies a K gate to the qubits with number qubitNum. Maps computational basis to Y eigenbasis.
        """
        k_gate = QuantumCircuit(1)
        k_gate.h(0)
        k_gate.s(0)
        k_gate.z(0)
        self.apply_sub_circuit(k_gate, qubitNum)

    def apply_X(self, qubitNum):
        """
        Applies a X gate to the qubits with number qubitNum.
        """
        self.qc.x(qubitNum)

    def apply_Z(self, qubitNum):
        """
        Applies a Z gate to the qubits with number qubitNum.
        """
        self.qc.z(qubitNum)

    def apply_Y(self, qubitNum):
        """
        Applies a Y gate to the qubits with number qubitNum.
        """
        self.qc.y(qubitNum)

    def apply_T(self, qubitNum):
        """
        Applies a T gate to the qubits with number qubitNum.
        """
        self.qc.t(qubitNum)

    def apply_rotation(self, qubitNum, n, a):
        """
        Applies a rotation around the axis n with the angle a to qubit with number qubitNum. If n is zero a ValueError
        is raised.

        :param qubitNum: int
            Qubit number
        :param n: tuple of floats
            A tuple of three numbers specifying the rotation axis, e.g n=(1,0,0)
        :param a: float
            The rotation angle in radians.
        """
        n = tuple(n)
        if n == (1, 0, 0):
            self.qc.rx(a, qubitNum)
        elif n == (0, 1, 0):
            self.qc.ry(a, qubitNum)
        elif n == (0, 0, 1):
            self.qc.rz(a, qubitNum)
        else:
            raise NotImplementedError("Can only do rotations around X, Y, or Z axis right now")

    def apply_CNOT(self, qubitNum1, qubitNum2):
        """
        Applies the CNOT to the qubit with the numbers qubitNum1 and qubitNum2.
        """
        self.qc.cx(qubitNum1, qubitNum2)

    def apply_CPHASE(self, qubitNum1, qubitNum2):
        """
        Applies the CPHASE to the qubit with the numbers qubitNum1 and qubitNum2.
        """
        self.qc.cz(qubitNum1, qubitNum2)

    def measure_qubit_inplace(self, qubitNum):
        """
        Measures the desired qubit in the standard basis. This returns the classical outcome. The quantum register
        is in the post-measurment state corresponding to the obtained outcome.

        Arguments:
        qubitNum	qubit to be measured
        """

        creg = ClassicalRegister(1)
        self.qc.add_register(creg)
        self.qc.measure(self.qRegister[qubitNum], creg[0])

        self.qc.reset(self.qc.qRegister[qubitNum])
        if creg[0] == 1:
            self.qc.x(self.qc.qRegister[qubitNum])

        return creg[0]


    def measure_qubit(self, qubitNum):
        """
        Measures the desired qubit in the standard basis. This returns the classical outcome and deletes the qubit.

        Arguments:
        qubitNum	qubit to be measured
        """
        creg = ClassicalRegister(1)
        self.qc.add_register(creg)
        self.qc.measure(self.qRegister[qubitNum], creg[0])

        return creg[0]

    def replace_qubit(self, qubitNum, state):
        """
        Replaces the qubit at position qubitNum with the one given by state.
        """
        raise NotImplementedError("Currently you cannot replace a qubit using project Q as backend")

    def absorb(self, other: 'qiskitQEngine'):
        """
        Absorb the qubits from the other engine into this one. This is done by tensoring the state at the end.
        """

        # Check whether there is space
        newNum = self.activeQubits + other.activeQubits
        if newNum > self.maxQubits:
            raise quantumError("Cannot merge: qubits exceed the maximum available.\n")

        # Check whether there are in fact qubits to tensor up....
        if self.activeQubits == 0:
            self.qRegister = other.qRegister
            self.cRegister = other.cRegister
            self.activeQubits = other.activeQubits
            self.qc = other.qc
        elif other.activeQubits > 0:
            # Get the current state of the other engine
            other_state = run_and_get_results(other.qc)

            # Allocate qubits in this engine for the new qubits from the other engine
            qreg = QuantumRegister(other.activeQubits)
            self.qc.add_register(qreg)
            self.qc.initialize(other_state, qreg)

            self.qRegister += qreg

        self.activeQubits = newNum

    def absorb_parts(self, R, I, activeQ):
        """
        Absorb the qubits, given in pieces

        Arguments:
        R		real part of the qubit state as a list
        I		imaginary part as a list
        activeQ		active number of qubits
        """
        # Check whether there is space
        newNum = self.activeQubits + activeQ
        if newNum > self.maxQubits:
            raise quantumError("Cannot merge: qubits exceed the maximum available.\n")

        if activeQ > 0:

            # Convert the real and imaginary parts to a state
            state = [re + im * 1j for re, im in zip(R, I)]

            # Allocate qubits in this engine for the new qubits from the other engine
            qreg = QuantumRegister(activeQ)
            self.qc.add_register(qreg)
            self.qc.initialize(state, qreg)

            self.qRegister += qreg

            self.activeQubits = newNum
