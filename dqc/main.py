from dqc.BaseInstructions import CNOTInstruction, XInstruction
from dqc.example import get_example_circuit
from dqc.node import ComputingNode
from dqc.transpiler import from_qiskit_to_base_instructions


def main():
    instructions = from_qiskit_to_base_instructions(get_example_circuit(), ['Alice', 'Bob'])
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
    main()

