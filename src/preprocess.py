import argparse
import glob
import logging
import os
from utils import MediapipeManager


def main(input_folder):
    logging.info("Checking input folder...")
    file_list = [files for files in glob.glob(os.path.abspath(input_folder) + "**/*.mp4",
                                              recursive=True)]
    preprocess_couting = 0
    new_ouput_folder = input_folder.split("/")[-2] if input_folder.split("/")[-1] == "" \
                       else input_folder.split("/")[-1]

    if len(file_list) == 0:
        raise FileNotFoundError

    logging.info("%i files were found.", len(file_list))

    if not os.path.exists(f"data/"):
        logging.info("Creating data folder...")
        os.mkdir(f"data/")

    logging.info("Creating output folder for the selected dataset.")
    os.mkdir(f"data/{new_ouput_folder}")

    mediapipe = MediapipeManager(f"data/{new_ouput_folder}/")
    try:
        for file_path in file_list:
            mediapipe.run_mediapipe(file_path)
            preprocess_couting += 1
            logging.info("Done.")
            logging.info("Progress: %.1f%%", (preprocess_couting/len(file_list)) * 100)

        logging.info("Pre-processing has been completed.")
        logging.info("Videos analyzed: %i", preprocess_couting)
        # logging.info("Time: ")
    except ProcessLookupError:
        print(ProcessLookupError)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run mediapipe framework.")
    parser.add_argument("-i", "--input_data_path",
                        help="Folder containing files with .mp4 \
                              extension to be converted by mediapipe",
                        required=True)
    arguments = parser.parse_args()
    input_data_path = arguments.input_data_path
    main(input_data_path)
