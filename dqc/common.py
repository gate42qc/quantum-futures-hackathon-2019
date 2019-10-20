from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def binStrToInt(binary_str):


    """The function binStrToInt() takes in one input, a string of ones and
    zeros (no spaces) called BINARY_STR.  It treats that input as a binary
    number (base 2) and converts it to a decimal integer (base 10). It
    returns an integer result."""

    length = len(binary_str)

    num = 0
    for i in range(length):
        num = num + int(binary_str[i])
        num = num * 2
    return int(num / 2)


def split_circuit(qc: QuantumCircuit, n: int):
    registers = []
    circuits = []
    remaining_qubits = qc.n_qubits
    qubits_per_circ = int(qc.n_qubits/n)
    for i in range(n):
        reg_len = min(qubits_per_circ, remaining_qubits)
        q_reg = QuantumRegister(reg_len)
        c_reg = ClassicalRegister(reg_len)
        sub_qc = QuantumCircuit(q_reg, c_reg)

        for inst, (q_reg, q_index), (c_index, c_reg) in qc:
            if i * qubits_per_circ <= q_index <= (i+1)*qubits_per_circ:
                curr_index = q_index
                sub_qc.append(inst, q_reg[q_index], c_reg[c_index])

        registers.append(q_reg)
