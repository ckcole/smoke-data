import pandas as pd
import numpy as np
# import streamlit

df = pd.read_csv('data-2020-5-2.csv')
df = df[['Local', 'Description']]
df['Local'] = pd.to_datetime(df['Local'])
df['date'] = df['Local'].map(pd.Timestamp.date)
df['Recorded_Daily_Count'] = None
df['cig_of_the_day'] = 1


prev_date = df.sort_values(by='Local').iloc[0]['Local'].date() - pd.Timedelta(days=1)
prev_count = None
cig_number = 0
for index, row in df.sort_values(by='Local').iterrows():
    cig_number += 1
    df.at[index, 'cig_of_the_day'] = cig_number
    if prev_count is None:
        prev_count = int(str(row['Description']))
        continue
    try:
        # remove words and NaN
        recorded = int(str(row['Description']))
        new_date = row['date']
        df.at[index, 'date'] == prev_date
        calculated = (20 - recorded) + prev_count
        if calculated > 30:
            print(f'****** Calculated higher than 30: {calculated} **********')
            calculated -= 20
        if calculated < 10:
            print(f'****** Calculated lower than 10: {calculated} **********')
            calculated += 20
        df.at[index, 'Recorded_Daily_Count'] = calculated
        print(prev_date, row['Description'], calculated, cig_number)
        prev_count = recorded
        prev_date = new_date
        cig_number = 1
        df.at[index, 'cig_of_the_day'] = cig_number
    except:
        pass
# df[df.Recorded_Daily_Count.notnull()]