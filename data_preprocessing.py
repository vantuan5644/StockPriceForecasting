import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from metrics import MAPE
from utils import get_data_splits

pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)

## Dataset

data = pd.read_csv('../dataset/excel_msn.csv')

columns = [i.replace('<', '').replace('>', '') for i in data.columns]

data = data.rename(columns={data.columns[i]: columns[i] for i in range(len(data.columns))})

data.index = pd.to_datetime(data['DTYYYYMMDD'], format='%Y%m%d')
data.drop(columns=['DTYYYYMMDD', 'Ticker'], inplace=True)

data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

df = data[data.index.year.isin([2019, 2020])]

df = df.sort_index()
df.head()

df['date'] = df.index
# df['hour'] = df['date'].dt.hour
df['dayofweek'] = df['date'].dt.dayofweek
df['quarter'] = df['date'].dt.quarter
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['dayofyear'] = df['date'].dt.dayofyear
df['dayofmonth'] = df['date'].dt.day
df['weekofyear'] = df['date'].dt.weekofyear
df.drop(columns=['date'], inplace=True)

ma_day = [3, 5, 7, 14, 28]
ma_cols = []
for ma in ma_day:
    column_name = f"MA_{ma}"
    ma_cols.append(column_name)
    df[column_name] = df['Close'].shift(1).rolling(ma).mean()

cols = ['Open', 'High', 'Low', 'Close', 'Volume']

for col in cols:
    for i in range(1, 8):
        df[f'{col}_{i}'] = df[col].shift(i)

df['lowerbound'] = 0.93 * df['Close_1']
df['upperbound'] = 1.07 * df['Close_1']

df.dropna(how='any', inplace=True)

cols = [i for i in df.columns if i not in ['Open', 'High', 'Low', 'Volume']]
print(cols)

df = df[cols]

target_col = 'Close'
feature_cols = [i for i in df.columns if i != target_col]

train_data, _, test_data = get_data_splits(df, train_ratio=0.5, validation_ratio=0, test_ratio=0.5)

import sklearn.preprocessing


train_scaler = sklearn.preprocessing.MinMaxScaler()
train_data = pd.DataFrame(train_scaler.fit_transform(train_data), columns=train_data.columns, index=train_data.index)

X_train, y_train = train_data.drop(columns=[target_col]), train_data[target_col]
X_test, y_test = test_data.drop(columns=[target_col]), test_data[target_col]

from sklearn.linear_model import LinearRegression

linear_reg = LinearRegression()
linear_reg.fit(X_train, y_train)

from sklearn.metrics import mean_squared_error, r2_score

y_pred = linear_reg.predict(X_test)
y_pred = pd.Series(y_pred, index=y_test.index)
print(MAPE(y_test, y_pred))

print(mean_squared_error(y_test, y_pred))

print(r2_score(y_test, y_pred))

k = 5
top_k_coefs = np.abs(linear_reg.coef_).argsort()[::-1][:k]
print(linear_reg.coef_[top_k_coefs])
print(X_train.columns[top_k_coefs])
