from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from data_processing import DataPreprocessing, Analysis
import pickle
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np


def pred_data():
    X_train, X_test, y_train, y_test = train_test_split(
        data_X, data_y, test_size=0.4, random_state=42
    )
    clf = LinearRegression()
    clf = make_pipeline(StandardScaler(), clf)
    clf.fit(X_train, y_train)
    print(f"score = {clf.score(X_test, y_test)}")
    clf.fit(data_X, data_y)
    df['score'] = clf.predict(data_X)
    df['diff'] = df['score']-df['price']
    df.sort_values('diff', inplace=True)
    return clf


data = DataPreprocessing()
data.set_data_from_file("autos.csv")
models = data.data.groupby('model')['model'].agg('count').sort_values(ascending=False)
models_count_less_than_10 = models[models <= 10]
data.data.model = data.data.model.apply(lambda x: 'other' if x in models_count_less_than_10.index else x)
# sn.displot(df['price'], bins=20)
# plt.show(block=True)
# dummies
data.set_dummies('seller')
data.set_dummies('offerType')
data.set_dummies('abtest')
data.set_dummies('vehicleType')
data.set_dummies('gearbox')
data.set_dummies('model')
data.set_dummies('fuelType')
data.set_dummies('brand')
data.set_dummies('notRepairedDamage')
df = data.data
df.drop(['index', 'dateCrawled', 'lastSeen', 'postalCode','nrOfPictures','monthOfRegistration'], axis=1, inplace=True)
df['dateCreated'] = df['dateCreated'].str[:4].astype(int)
df['yearOfRegistration'] = df['yearOfRegistration'].astype(int)
df['yearsOld'] = df['dateCreated'] - df['yearOfRegistration']
df.drop(['yearOfRegistration', 'dateCreated'], axis=1, inplace=True)
df.drop(df.loc[(df.yearsOld > 150) | (df.yearsOld < 0)].index, inplace=True)
df.drop(df.loc[(df.price > 5_000_000) | (df.price <= 1)].index, inplace=True)
df.drop(df.loc[(df.powerPS > 500) | (df.powerPS == 0)].index, inplace=True)
df.price = np.log(df.price)
describe = df.describe()
data_X = df.drop(['price', 'name'], axis=1)
data_y = df['price'].astype(float)

clf = pred_data()

with open('autos_price_model.pickle', 'wb') as f:
    pickle.dump(clf, f)