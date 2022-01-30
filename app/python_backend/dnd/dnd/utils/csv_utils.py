import pandas as pd


def import_csv(file_path):
    data_frame = pd.read_csv(file_path, index_col='Name', sep="|")
    return data_frame.to_dict('index')
