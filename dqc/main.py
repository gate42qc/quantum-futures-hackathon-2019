from dqc.BaseInstructions import CNOTInstruction, XInstruction
from dqc.node import ComputingNode


def main():
    instructions = [CNOTInstruction(("Alice", 0), ("Bob", 1))]

    alice = ComputingNode("Alice", [XInstruction("Alice", 0)] + instructions)
    bob = ComputingNode("Bob", instructions)

    process1 = alice.get_process()
    process2 = bob.get_process()

    process1.start()
    process2.start()
    process1.join()
    process2.join()


if __name__ == '__main__':
    main()

