from math import pi
from typing import List, Tuple

from cqc.pythonLib import CQCConnection, qubit

from dqc.common import binStrToInt


class BaseInstruction:
    name: str
    params: List


class SingeQubitInstruction(BaseInstruction):
    name: str
    qubit: int
    connection_name: str

    def apply(self, q: qubit):
        raise NotImplementedError


class CNOTInstruction(BaseInstruction):
    name = "CNOT"
    params = []

    control: int
    control_connection_name: str
    target: int
    target_connection_name: str

    def __init__(self, control: Tuple[str, int], target: Tuple[str, int]):
        self.control_connection_name, self.control = control
        self.target_connection_name, self.target = target
        self.qubits = [control, target]

    def apply_on_control(self, cqc: CQCConnection, target_cqc_name: str, control: qubit):
        # Create an EPR pair
        q = cqc.createEPR(target_cqc_name)
        control.cnot(q)

        local_result = q.measure(inplace=True)
        q.reset()

        cqc.sendClassical(name=target_cqc_name, msg=local_result)

        print("\n ")
        print("Alice sent message: ", local_result)

        remote_result = binStrToInt(cqc.recvClassical())

        print("Alice received message: ", remote_result)
        if remote_result == 1:
            control.Z()

    def apply_on_target(self, cqc: CQCConnection, control_cqc_name: str, target: qubit):
        # Receive qubit
        q = cqc.recvEPR()
        remote_result = binStrToInt(cqc.recvClassical())
        print("Bob received message: ", remote_result)
        if remote_result == 1:
            q.X()

        q.cnot(target)
        q.H()
        local_result = q.measure(inplace=True)
        q.reset()

        print("Bob sent message: ", local_result)
        cqc.sendClassical(control_cqc_name, msg=local_result)

    def apply(self, control: qubit, target: qubit):
        if control._cqc.name != target._cqc.name:
            raise ValueError()
        control.cnot(target)


class XInstruction(SingeQubitInstruction):
    name = "X"
    params = []

    def __init__(self, connection_name: str, qubit: int):
        self.connection_name = connection_name
        self.qubit = qubit

    def apply(self, q: qubit):
        q.X()


class HInstruction(SingeQubitInstruction):
    name = "H"
    params = []

    def __init__(self, connection_name: str, qubit: int):
        self.connection_name = connection_name
        self.qubit = qubit

    def apply(self, q: qubit):
        q.H()


class TInstruction(SingeQubitInstruction):
    name = "T"
    params = []

    def __init__(self, connection_name: str, qubit: int):
        self.connection_name = connection_name
        self.qubit = qubit

    def apply(self, q: qubit):
        q.T()


class TInstruction(SingeQubitInstruction):
    name = "T"
    params = []

    def __init__(self, connection_name: str, qubit: int):
        self.connection_name = connection_name
        self.qubit = qubit

    def apply(self, q: qubit):
        q.T()


class RXInstruction(SingeQubitInstruction):
    name = "RX"
    params = []
    theta: float

    def __init__(self, connection_name: str, qubit: int, theta: float):
        self.connection_name = connection_name
        self.qubit = qubit
        self.params = [theta]
        self.theta = theta

    def apply(self, q: qubit):
        q.rot_X(int(self.theta/(2*pi/256)))


class RYInstruction(SingeQubitInstruction):
    name = "RY"
    params = []
    theta: float

    def __init__(self, connection_name: str, qubit: int, theta: float):
        self.connection_name = connection_name
        self.qubit = qubit
        self.params = [theta]
        self.theta = theta

    def apply(self, q: qubit):
        q.rot_Y(int(self.theta/(2*pi/256)))


class RZInstruction(SingeQubitInstruction):
    name = "RZ"
    params = []
    theta: float

    def __init__(self, connection_name: str, qubit: int, theta: float):
        self.connection_name = connection_name
        self.qubit = qubit
        self.params = [theta]
        self.theta = theta

    def apply(self, q: qubit):
        q.rot_Z(int(self.theta*256/(2*pi)))


class MeasureInstruction(SingeQubitInstruction):
    name = "MEASURE"
    params = []
    theta: float

    def __init__(self, connection_name: str, qubit: int):
        self.connection_name = connection_name
        self.qubit = qubit

    def apply(self, q: qubit):
        q.measure(inplace=True)


class TInstruction(SingeQubitInstruction):
    name = "T"
    params = []

    def __init__(self, connection_name: str, qubit: int):
        self.connection_name = connection_name
        self.qubit = qubit

    def apply(self, q: qubit):
        q.T()
