from typing import List

from qiskit import QuantumCircuit

from dqc.example import get_example_circuit
from dqc.node import ComputingNode
from dqc.transpiler import from_qiskit_to_base_instructions


def run_on_network(qc: QuantumCircuit, node_names: List[str]):
    instructions = from_qiskit_to_base_instructions(qc, node_names)
    print(instructions)

    alice = ComputingNode("Alice", instructions["Alice"])
    bob = ComputingNode("Bob", instructions["Bob"])

    process1 = alice.get_process()
    process2 = bob.get_process()

    process1.start()
    process2.start()
    process1.join()
    process2.join()


if __name__ == '__main__':
    circuit = get_example_circuit()
    network_nodes = ['Alice', 'Bob']
    run_on_network(circuit, network_nodes)

