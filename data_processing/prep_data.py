import pandas as pd
import numpy as np
from .data_parser import DataParser


class DataPreprocessing:
    def __init__(self):
        self.data = None
        self.data_parser = DataParser()
        self.info_features = []

    def set_data_from_file(self, file_path):
        self.data = self.data_parser.get_data(file_path)

    def save_data(self, file_path=None):
        if isinstance(self.data, pd.DataFrame) and not self.data.empty:
            self.data.to_csv(file_path)

    def set_dummies(self, feature: str):
        feature_data = pd.get_dummies(self.data[feature])
        self.data[feature_data.columns] = feature_data
        self.data.drop(feature, inplace=True, axis=1)

    def set_info_features(self, features):
        self.info_features = features[:]

    def join_data(self, df, id_col_name):
        self.data = pd.merge(self.data, df, on=id_col_name)

    def set_col_if_not_exist(self, col, value=0):
        if col not in self.data.columns:
            self.data[col] = value

    def concat_data_files(self, files, axis=0):
        dfs = []
        for file in files:
            self.set_data_from_file(file)
            dfs.append(self.data)
        self.data = pd.concat(dfs, axis=axis)

    def drop_feature(self, feature):
        self.data.drop(feature, axis=1, inplace=True)
