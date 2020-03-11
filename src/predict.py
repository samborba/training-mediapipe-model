import argparse
import os
import logging
import pickle
from random import randrange
from statistics import mode
import pandas as pd

from utils.mediapipe import MediapipeManager
from utils import structuring

MODEL_BINARY_FILE = "knnclassifier_file"
OUTPUT_PATH = os.getcwd() + "/data/"

def start_predict(video_path, k_frames=10):
    classification_list = []
    mediapipe = MediapipeManager(OUTPUT_PATH)
    file_name = video_path.split("/")[-1].split(".")[0] + ".csv"

    logging.info("Starting prediction.")
    model = pickle.load(open(os.path.abspath(f"src/model/{MODEL_BINARY_FILE}"), "rb"))

    mediapipe.run_mediapipe(video_path)
    dataframe = pd.read_csv(OUTPUT_PATH + file_name, index_col=False)

    logging.info("Running model in %i differents frames.", k_frames)
    for _ in range(1, k_frames):
        frame = structuring.get_row(dataframe, randrange(1, len(dataframe)))
        frame = frame.reshape(1, -1)
        classification_list.append(model.predict(frame)[0])

    os.remove(OUTPUT_PATH + file_name)

    logging.info("Classification: %s", mode(classification_list))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run model.")
    parser.add_argument("-i", "--input_video_path",
                        help="Path to the video.",
                        required=True)
    arguments = parser.parse_args()

    input_video_path = arguments.input_video_path
    start_predict(input_video_path)
