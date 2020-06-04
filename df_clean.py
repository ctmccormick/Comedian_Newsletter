import pandas as pd
from datetime import datetime, timedelta
import json

data = pd.read_csv('wiki_data.csv', dtype={'living_status': 'category'})
manual = pd.read_excel('improv_comedians_manual.xlsx')

df = pd.concat([data, manual])
df.rename({'Unnamed: 0': 'Name'}, axis=1, inplace=True)
df = df.fillna("")

today = pd.to_datetime(datetime.today())
end_week = pd.to_datetime(today + timedelta(days=6))
yesterday = pd.to_datetime(today - timedelta(days=1))


df['search_name'] = df['Name'].str.replace(" ", "+")


# ignore rows that have no date or partial birth or death date
def full_dates_only(row, col):
    if str(row[col]).count('-') == 2 or str(row[col]).count('/') == 2:
        return pd.to_datetime(row[col], errors='ignore', format='%d-%m-%Y')
    else:
        return pd.NaT


df['bday'] = df.apply(lambda row: full_dates_only(row, 'scraped_bday'), axis=1)
df['dday'] = df.apply(lambda row: full_dates_only(row, 'scraped_dday'), axis=1)

df['bday'] = pd.to_datetime(df['bday'], errors='coerce')
df['dday'] = pd.to_datetime(df['dday'], errors='coerce')


def day_range(row, col):
    day = row[col].day
    month = row[col].month
    year = today.year
    try:
        return datetime(year, month, day)
    except:
        return pd.NaT


df['bday_this_week'] = df.apply(lambda row: day_range(row, 'bday'), axis=1)
df['dday_this_week'] = df.apply(lambda row: day_range(row, 'dday'), axis=1)

weeks_bdays = df.loc[(df['bday_this_week'] <= end_week)
                     & (df['bday_this_week'] >= yesterday)]

weeks_ddays = df.loc[(df['dday_this_week'] <= end_week)
                     & (df['dday_this_week'] >= yesterday)]


def week_day(row, col):
    try:
        day = pd.to_datetime(datetime(2020, int(row[col].month), int(row[col].day))).day_name()
        return day
    except:
        return ""


def month_day(row, col):
    try:
        return int(row[col].day)
    except:
        return ""


def full_day(row, col):
    full_day_str = row['week_day'] + ", " + row[col].strftime("%B") + " " + str(row['month_day'])
    return full_day_str


def age(row, col):
    age_num = today.year - row[col].year
    return age_num


def add_cols(df_name, col_type):
    try:
        df_name['age'] = df_name.apply(lambda row: age(row, col_type), axis=1)
        df_name['week_day'] = df_name.apply(lambda row: week_day(row, col_type), axis=1)
        df_name['month_day'] = df_name.apply(lambda row: month_day(row, col_type), axis=1)
        df_name['full_day'] = df_name.apply(lambda row: full_day(row, col_type), axis=1)
    except:
        pass


add_cols(weeks_bdays, 'bday')
add_cols(weeks_ddays, 'dday')


wiki_data_bdays = weeks_bdays.set_index('Name').to_dict('index')
wiki_data_ddays = weeks_ddays.set_index('Name').to_dict('index')


with open('wiki_data_bdays.json', 'w') as fp:
    json.dump(wiki_data_bdays, fp, default=str)

with open('wiki_data_ddays.json', 'w') as fp:
    json.dump(wiki_data_ddays, fp, default=str)
