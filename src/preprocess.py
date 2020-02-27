import logging
import os
import glob
from util import MediapipeManager

def main():
    logging.info("Walking through the input folder.")
    file_list = [files for files in glob.glob(os.path.abspath("../data/input") + "**/*.mp4", recursive=True)]

    if len(file_list) == 0:
        logging.warn("The input folder is empty.")
        exit()

    mediapipe = MediapipeManager(os.path.abspath("../data/output/"))

    try:
        for file_path in file_list:
            mediapipe.run_mediapipe(file_path)
        logging.info("Execution has been completed.")
    except ProcessLookupError as e:
        print(e)


if __name__ == "__main__":
    main()
