from orchestrator import Orchestrator
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    orchestrator = Orchestrator(4)
    orchestrator.create(2)


if __name__ == "__main__":
    main()
