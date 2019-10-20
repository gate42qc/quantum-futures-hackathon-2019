from typing import List

from qiskit import QuantumCircuit

from dqc.example import get_example_circuit
from dqc.node import ComputingNode
from dqc.transpiler import from_qiskit_to_base_instructions


def run_on_network(qc: QuantumCircuit, node_names: List[str]):
    instructions = from_qiskit_to_base_instructions(qc, node_names)

    nodes = [ComputingNode(node_name, instructions[node_name]) for node_name in node_names]
    processes = [n.get_process() for n in nodes]

    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == '__main__':
    circuit = get_example_circuit()
    network_nodes = ['Alice', 'Bob']
    run_on_network(circuit, network_nodes)

