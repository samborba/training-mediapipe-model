import argparse
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams

import structuring


def plot_frame(data_path, frame_index):
    """Show landmarks of a frame into a graph.

    Arguments:
        csv {str} -- path to the .csv file
        frame_index {int} -- index of the frame
    """
    frame_content = structuring.get_row(data_path, frame_index)
    x, y = frame_content.T
    plt.scatter(x, y)
    plt.show()


def plot_correlation_matrix(data_path):
    """Show correlation matrix between variables.

    Arguments:
        data {str} -- path to the .csv file
    """
    rcParams['figure.figsize'] = 15, 20
    fig = plt.figure()
    data = pd.read_csv(data_path)
    sns.heatmap(data.corr(), annot=True, fmt=".2f")
    fig.savefig('correlation.png')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot frame into a graph.")
    parser.add_argument("-i", "--input_dataset_path",
                        help="csv file path.",
                        required=True)
    parser.add_argument("-f", "--frame",
                        help="Frame index (same as row index).",
                        type=int)
    arguments = parser.parse_args()

    input_data_path = arguments.input_dataset_path
    frame = arguments.frame

    if frame is not None:
        plot_frame(input_data_path, frame)
    else:
        plot_correlation_matrix(input_data_path)
