from orchestrator import Orchestrator
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    orchestrator = Orchestrator(1)
    orchestrator.create()


if __name__ == "__main__":
    main()
