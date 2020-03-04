from glob import glob
import pandas as pd

LABEL_VALUE = "Open Hand"


def add_label(csv_path, output_folder, label=LABEL_VALUE):
    csv_name = csv_path.split("/")[-1]
    data = pd.read_csv(csv_path, index_col=False)
    data["class"] = label
    data.to_csv(f"{output_folder}/{csv_name}", index=False)


def convert_to_one(folder_path):
    csv_list = [csv for csv in glob(folder_path + "/*.csv")]
    combine_csv = pd.concat([pd.read_csv(csv, index_col=False) for csv in csv_list])
    combine_csv.to_csv(f"{folder_path}/dataset.csv", index=False)
