import argparse
import logging


def start_predict(video_path, k_frames=10):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run model.")
    parser.add_argument("-i", "--input_video_path",
                        help="Path to the video.",
                        required=True,
                        type="str")
    arguments = parser.parse_args()

    input_video_path = arguments.input_video_path
    start_predict(input_video_path)
