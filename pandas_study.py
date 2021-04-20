import pyupbit
import pandas as pd
import numpy as np

s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s)

dates = pd.date_range('20210101', periods=6)
print(dates)

df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
print(df)

df2 = pd.DataFrame({'A': 1.,
                    'B': pd.Timestamp('20130102'),
                    'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                    'D': np.array([3]*4, dtype='int32'),
                    'E': pd.Categorical(['test', 'train', 'test', 'train']),
                    'F': 'foo'})
print(df2)
print(df2.dtypes)

#tickers = pyupbit.get_tickers(fiat='KRW')
ticker = 'KRW-XRP'
df = pyupbit.get_ohlcv(ticker, interval='day', count=2)
print(df.head(1))
print(df.tail(1))
print(df.values)
print(df.index)
print(df.columns)
print(df.describe())
print(df.T)
print(df.sort_index(axis=1), ascending=False) # 0: index, 1: column
print(df.sort_values(by='high'))
print(df['close'][0])