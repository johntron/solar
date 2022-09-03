import pandas as pd
from calendar import month_abbr

def billed():
    lower_months = [m.lower() for m in month_abbr]
    names = [
        'year',
        'month',
        'kWh',
        'kWh carryover', # From following month's bill
        'kWh total',
        'cents per kWh',
        'cost of energy',
        'cost of delivery',
        'cost of sales',
        'cost of other',
        'cost total'
    ]
    df = pd.read_csv('./data/billed.csv', header=1, names=names)
    df['kwh'] = df['kWh total']
    df = df.drop(columns=['kWh total', 'kWh carryover'])
    # display(df)
    df['month'] = df['month'].str.lower().map(lambda m: lower_months.index(m)).astype('Int8')
    # display(df.dtypes)
    # display(df)
    # display(df.describe())
    return df


def usage():
    df = pd.read_csv('./data/IntervalData.csv')
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace('_', ' ')
    df = df.drop(['esiid', 'revision date', 'usage end time', 'estimated actual', 'consumption surplusgeneration'], axis=1)
    df['date'] = pd.to_datetime(df['usage date'] + ' ' + df['usage start time'])
    df['usage_year'] = df['date'].dt.year
    df['usage_month'] = df['date'].dt.month
    return df

def interval_cost(billed_usage, interval_usage):
    cents_per_kwh = billed_usage[['cents per kWh', 'year', 'month']]
    # display(cents_per_kwh)
    # display(interval_usage)
    df = pd.merge(cents_per_kwh, interval_usage, left_on=['year', 'month'], right_on=['usage_year', 'usage_month'])
    df['cost'] = (df['cents per kWh'] + df['usage kwh']) / 100
    df = df.sort_values('date')
    # display(interval_cost)
    # display(interval_cost.describe())
    return df
