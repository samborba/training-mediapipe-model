import argparse
import matplotlib.pyplot as plt

import structuring

def plot(csv, frame_index):
    frame_content = structuring.get_row(csv, frame_index)
    x, y = frame_content.T
    plt.scatter(x, y)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot frame into a graph.")
    parser.add_argument("-i", "--input_dataset_path",
                        help="csv file path.",
                        required=True)
    parser.add_argument("-f", "--frame",
                        help="Frame index (same as row index).",
                        type=int, required=True)
    arguments = parser.parse_args()

    input_data_path = arguments.input_dataset_path
    frame = arguments.frame
    plot(input_data_path, frame)
