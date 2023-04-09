from orchestrator import Orchestrator
import logging


def main():
    logging.basicConfig(level=logging.INFO)

    for i in range(5):
        orchestrator = Orchestrator(4)
        orchestrator.create(1)


if __name__ == "__main__":
    main()
