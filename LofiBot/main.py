from orchestrator import Orchestrator
import logging
from tqdm import tqdm


def main():
    logging.basicConfig(level=logging.INFO)

    for i in tqdm(range(10)):
        orchestrator = Orchestrator(4)
        orchestrator.create(1)


if __name__ == "__main__":
    main()
