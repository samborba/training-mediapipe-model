import argparse
import glob
import logging
import os
import shutil

from utils import MediapipeManager
from utils import structuring


def main(input_folder, classification_label):
    logging.info("Checking input folder.")
    file_list = [files for files in glob.glob(os.path.abspath(input_folder) + "**/*.mp4",
                                              recursive=True)]
    input_counting = 0
    folder_name = input_folder.split("/")[-2] if input_folder.split("/")[-1] == "" \
                       else input_folder.split("/")[-1]
    output_folder = f"data/{folder_name}/"

    mediapipe_dependencies = ["calculators", "graphs", "models"]

    if not all([os.path.isdir(f"mediapipe/{dep}") for dep in mediapipe_dependencies]):
        raise FileNotFoundError # return error

    if len(file_list) == 0:
        raise FileNotFoundError

    logging.info("%i files were found.", len(file_list))

    if not os.path.exists(f"data"):
        logging.info("Creating data folder...")
        os.mkdir(f"data")

    if not os.path.exists(output_folder):
        logging.info("Creating %s folder...", folder_name)
    else:
        logging.info("Output %s folder already exist. Cleaning it up...", folder_name)
        shutil.rmtree(output_folder)

    os.mkdir(output_folder)

    mediapipe = MediapipeManager(output_folder)
    try:
        for file_path in file_list:
            mediapipe.run_mediapipe(file_path)
            input_counting += 1
            logging.info("Done.")
            logging.info("Progress so far: %.1f%%", (input_counting/len(file_list)) * 100)

        logging.info(">>> Coordinate extraction done.")
        logging.info("Videos analyzed: %i", input_counting)

        logging.info("Starting data prepation.")
        logging.info("Adding new column to all .csv files.")
        csv_list = [files for files in glob.glob(os.path.abspath(f"{output_folder}/*.csv"),
                                                 recursive=True)]
        for csv_path in csv_list:
            if classification_label is not None:
                structuring.add_label(csv_path, output_folder, classification_label)
            else:
                structuring.add_label(csv_path, output_folder)

        logging.info(">>> Data prepation done.")
        logging.info("Combining all the .csv of the dataset to serve the model.")
        structuring.convert_to_one(output_folder)

        logging.info(">>> Pre-processing has been completed.")
    except ProcessLookupError:
        print(ProcessLookupError)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run mediapipe framework.")
    parser.add_argument("-i", "--input_data_path",
                        help="Folder containing files with .mp4 \
                              extension to be converted by mediapipe",
                        required=True)
    parser.add_argument("-c", "--classification", help="Adds a classification for the dataset \
                        that already exists (the parameter input_data_folder must be provided, \
                        as this value is used as input).",
                        type=str, required=False, default=None)
    arguments = parser.parse_args()

    input_data_path = arguments.input_data_path
    classification = arguments.classification
    main(input_data_path, classification)
