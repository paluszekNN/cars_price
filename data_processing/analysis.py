import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


class Analysis:
    def get_cat_amount(self, categories):
        bottom = None
        fig, ax = plt.subplots()
        columns = categories.columns
        data = []
        for category in columns:
            amounts = categories[category].value_counts()
            data.append(amounts)
        data = pd.concat(data, axis=1)
        data.fillna(0, inplace=True)
        data.columns = columns

        for category in data.columns:
            if not isinstance(bottom, np.ndarray):
                bottom = np.zeros(len(data[category].index))
            p = ax.bar(data[category].index, data[category].values, label=category, bottom=bottom)
            bottom += data[category].values
            ax.bar_label(p, label_type='center')
        ax.legend()
        plt.show(block=True)
