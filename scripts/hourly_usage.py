import pandas

df = pandas.read_csv('../data/IntervalData.csv')
df = df['USAGE_KWH']
df = df.groupby(df.index // 2).sum()
df.to_csv('../data/usage_every_thirty_min.csv', index=False)
