import argparse
import logging
import os
from glob import glob

from utils import structuring


def main(dataset_list):
    logging.info("Starting main csv file concatenation...")
    structuring.mount_dataset(dataset_list)
    logging.info(">>> Concatenation done successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build model.")
    parser.add_argument("-b", "--build",
                        help="Array of datasets folders which contains main csv.",
                        required=True,
                        type=str)
    arguments = parser.parse_args()

    dataset_list = arguments.build
    main(dataset_list)
