import pandas as pd


class DataParser:
    def get_data(self, file_path):
        if 'csv' == file_path[-3:]:
            return self.data_from_csv(file_path)
        elif 'html' == file_path[-4:]:
            return self.data_from_html(file_path)
        else:
            raise NotImplementedError("No match for this file")

    def data_from_csv(self, file_path):
        """

        :param file_path: path to csv file
        :return: pandas DataFrame object
        """
        return pd.read_csv(f'{file_path}')

    def data_from_html(self, file_path, table_index=0):
        """

        :param file_path: path to html file
        :param table_index: index of the table from html
        :return: pandas DataFrame object
        """
        return pd.read_html(f"{file_path}", encoding="UTF-8")[table_index]