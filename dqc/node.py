from typing import List
from dqc.BaseInstructions import BaseInstruction, SingeQubitInstruction, CNOTInstruction
from multiprocessing import Process


def compute(name: str, instructions: List[BaseInstruction]):
    from cqc.pythonLib import CQCConnection, qubit

    # Initialize the connection
    with CQCConnection(name) as connection:
        qubits = {}

        for inst in instructions:
            if isinstance(inst, SingeQubitInstruction):
                if inst.qubit not in qubits:
                    qubits[inst.qubit] = qubit(connection)
                inst.apply(qubits.get(inst.qubit))

            if isinstance(inst, CNOTInstruction):
                if inst.control_connection_name == inst.target_connection_name:
                    if inst.control not in qubits:
                        qubits[inst.control] = qubit(connection)
                    if inst.target not in qubits:
                        qubits[inst.target] = qubit(connection)

                    inst.apply(qubits.get(inst.control), qubits.get(inst.target))
                else:
                    if inst.control_connection_name == connection.name:
                        if inst.control not in qubits:
                            qubits[inst.control] = qubit(connection)
                        inst.apply_on_control(connection, inst.target_connection_name, qubits.get(inst.control))
                    else:
                        if inst.target not in qubits:
                            qubits[inst.target] = qubit(connection)
                        inst.apply_on_target(connection, inst.control_connection_name, qubits.get(inst.target))

        results = [q.measure() for q in qubits.values()]

        print(f"Results for {name}", results)

        return results


class ComputingNode:
    id: int
    instructions: List[BaseInstruction]

    def __init__(self, id, instructions: List[BaseInstruction]):
        self.id = id
        self.instructions = instructions

    def get_process(self):
        return Process(target=compute, args=(self.id, self.instructions,))

