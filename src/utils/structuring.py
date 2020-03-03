import pandas as pd

LABEL_VALUE = "Open Hand"

def add_label(csv_path, output_folder, label=LABEL_VALUE):
    csv_name = csv_path.split("/")[-1]
    data = pd.read_csv(csv_path, index_col=False)
    data["label"] = label
    data.to_csv(f"{output_folder}/{csv_name}", index=False)
