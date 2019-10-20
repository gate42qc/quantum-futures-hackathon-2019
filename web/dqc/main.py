from multiprocessing import Pipe
from typing import List

from qiskit import QuantumCircuit

from dqc.example import get_example_circuit
from dqc.node import ComputingNode
from dqc.transpiler import from_qiskit_to_base_instructions


def run_on_network(qc: QuantumCircuit, node_names: List[str]):
    instructions = from_qiskit_to_base_instructions(qc, node_names)

    nodes = [ComputingNode(node_name, instructions[node_name]) for node_name in node_names]
    processes = []
    results = []

    for n in nodes:
        parent_conn, child_conn = Pipe()
        processes.append((parent_conn, n.get_process(child_conn)))

    for conn, p in processes:
        p.start()
        print("Process started")

    for conn, p in processes:
        results.append(conn.recv())

    for conn, p in processes:
        p.join()

    return results


if __name__ == '__main__':
    circuit = get_example_circuit()
    network_nodes = ['Alice', 'Bob']
    run_on_network(circuit, network_nodes)

