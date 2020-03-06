import argparse
import logging

from utils import structuring


def main(datasets):
    """Concatenates all the main csv files (which contains the output of the coordinates \
       of all the videos) of each dataset in just one file in which the model will be trained.

    Arguments:
        datasets {str} -- all datasets with classes to train the model
    """
    logging.info("Starting main csv file concatenation...")
    structuring.mount_dataset(datasets)
    logging.info(">>> Concatenation done successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build model.")
    parser.add_argument("-d", "--datasets_compile",
                        help="Array of datasets folders which contains main csv.",
                        required=True,
                        type=str)
    arguments = parser.parse_args()

    dataset_list = arguments.datasets_compile
    main(dataset_list)
