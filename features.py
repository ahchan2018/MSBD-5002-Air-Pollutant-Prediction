import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d")

#transform string to datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d")

#transform string to timestamp
def string_toTimestamp(strTime):
    return time.mktime(string_toDatetime(strTime).timetuple())

#transform timestamp to string
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))

def get_which_holiday_weekend(day_today):
    # print "day:", day
    which_holiday = ['2017-01-01', '2017-01-02', '2017-01-27', '2017-01-28', '2017-01-29',
               '2017-01-30', '2017-01-31', '2017-02-01', '2017-02-02', '2017-04-02',
               '2017-04-03', '2017-04-04', '2017-04-29', '2017-04-30', '2017-05-01',
               '2017-05-28', '2017-05-29', '2017-05-30', '2017-10-01', '2017-10-02',
               '2017-10-03', '2017-10-04', '2017-10-05', '2017-10-06', '2017-10-07',
               '2017-10-08', '2017-12-30', '2017-12-31',
               '2018-01-01', '2018-02-15', '2018-02-16', '2018-02-17', '2018-02-18',
               '2018-02-19', '2018-02-20', '2018-02-21', '2018-04-05', '2018-04-06',
               '2018-04-07', '2018-04-29', '2018-04-30', '2018-05-01', '2018-06-16',
               '2018-06-17', '2018-06-18']

    which_work = ['2017-01-22', '2017-02-04', '2017-04-01', '2017-05-27', '2017-09-30',
            '2018-02-11', '2018-02-24', '2018-04-08', '2018-04-28']
    day_rest_first = ['2017-01-27', '2017-02-05', '2017-04-02', '2017-05-28', '2017-10-01', '2018-02-15', '2018-02-25',
                      '2018-04-05', '2018-04-29']
    day_rest_last = ['2017-01-02', '2017-01-21', '2017-02-02', '2017-02-05', '2017-04-04', '2017-05-01', '2017-05-30',
                     '2018-01-01', '2018-02-21', '2018-04-07', '2018-05-01']
    which_work_first_day = ['2017-01-03', '2017-01-22', '2017-02-03', '2017-04-05', '2017-05-02', '2017-05-31', '2018-01-02',
                     '2018-02-11', '2018-02-22', '2018-04-08', '2018-05-02']
    which_work_last_day = ['2017-01-26', '2017-02-04', '2017-04-01', '2017-05-27', '2017-09-30', '2018-02-14', '2018-02-24',
                     '2018-04-04', '2018-04-28']

    not_day_rest_first = ['2017-01-28', '2017-02-04', '2017-04-01', '2017-05-27', '2017-09-30', '2017-10-07',
                          '2018-02-17',
                          '2018-02-24', '2018-04-07', '2018-04-28']
    not_day_rest_last = ['2017-01-01', '2017-01-22', '2017-02-29', '2017-04-02', '2017-04-30', '2017-05-28',
                         '2017-10-01'
                         '2017-12-31', '2018-02-11', '2018-02-18', '2018-04-08', '2018-04-29']
    not_which_work_first_day = ['2017-01-02', '2017-01-23', '2017-01-30', '2017-04-03', '2017-05-01', '2017-05-29',
                         '2017-10-02',
                         '2018-01-01', '2018-02-12', '2018-02-19', '2018-04-09', '2018-04-30']
    not_which_work_last_day = ['2017-01-27', '2017-02-03', '2017-03-31', '2017-05-26', '2017-09-29', '2017-10-06',
                         '2018-02-16',
                         '2018-02-23', '2018-04-04', '2018-04-06', '2018-04-27']
    which_holiday_flag = {}
    for day in which_holiday:
        which_holiday_flag[day] = 1
    which_work_flag = {}
    for day in which_work:
        which_work_flag[day] = 1

   
    day_today = day_today.split(' ')[0]
    year = int(day_today.split("-")[0])
    month = int(day_today.split("-")[1])
    day = int(day_today.split("-")[2])
    #  print('----')
    
    temp = []
    day_now = datetime(year, month, day)
    day = day_now
    day_str = datetime_toString(day)
    # determine if it is weekend
    week = day.weekday()
    # print day
    if week >= 5:
        temp.append(1)
    else:
        temp.append(0)
    # determine if it is which_holiday
    if day_str in which_holiday_flag:
        temp.append(1)
    else:
        temp.append(0)
    # determine if it is weekday
    if (week >= 5 and (not day_str in which_work_flag)) or (day_str in which_holiday_flag):
        temp.append(0)
    else:
        temp.append(1)
    # determine if it is the last day of which_work
    if (week == 6 and (not day_str in not_day_rest_last)) or (day_str in day_rest_last):
        temp.append(1)
    else:
        temp.append(0)
    # determine if it is the first day of which_work
    if (week == 0 and (not day_str in not_which_work_first_day)) or (day_str in which_work_first_day):
        temp.append(1)
    else:
        temp.append(0)
    # determine if it is the last day of which_work
    if (week == 4 and (not day_str in not_which_work_last_day)) or (day_str in which_work_last_day):
        temp.append(1)
    else:
        temp.append(0)
    # determine if it is the first day of which_holiday
    if (week == 5 and (not day_str in not_day_rest_first)) or (day_str in day_rest_first):
        temp.append(1)
    else:
        temp.append(0)
    return temp#[is_weekend,is_which_holiday,is_which_workday,is_rest_end,is_which_work1,is_which_work_end, is_which_holiday1]


def map_date_features(df):
    COLUMNS = ['is_weekend','is_which_holiday','is_which_workday','is_rest_end','is_which_work',
                'is_which_work_end', 'is_which_holiday1']

    dates = df['utc_time'].values
    date_features = []
    
    for each_date in dates:
        current_features = get_which_holiday_weekend(each_date)
        date_features.append(current_features)
    date_features = pd.DataFrame(date_features, columns=COLUMNS)
    df = pd.concat([df, date_features], axis=1)

    return df

def process_categotical(vector):
  unique_vals = np.unique(vector)
  
  map_dict = {};encode=1
  for val in unique_vals:
    map_dict[val] = encode
    encode += 1

  return map_dict

def process_all():
  air_quality_path = 'processed-data/air_quality.csv'
  grid_weather_path = 'processed-data/grid_weather.csv'
  observed_weather_path = 'processed-data/observed_weather.csv'

  air_quality = pd.read_csv(air_quality_path)
  grid_weather = pd.read_csv(grid_weather_path)
  observed_weather = pd.read_csv(observed_weather_path)
  
  grid_weather['weather'] = grid_weather['weather'].fillna('none')
  grid_weather_map = process_categotical(grid_weather['weather'].values)
  grid_weather['weather'] = grid_weather['weather'].apply(lambda x:grid_weather_map[x])

  #process observed weather
  observed_weather['weather'] = observed_weather['weather'].fillna('none')
  observed_weather_map = process_categotical(observed_weather['weather'].values)
  observed_weather['weather'] = observed_weather['weather'].apply(lambda x:observed_weather_map[x])
  

  observed_weather[['wind_direction','wind_speed']] = observed_weather[['wind_direction','wind_speed']].fillna(method='pad')
  observed_weather['utc_time'] = pd.to_datetime(observed_weather['utc_time'])
  std_station_id = []
  for item in observed_weather['station_id'].values:
      item = item.split('_')
      id = item[0]+'_'+'aq'
      std_station_id.append(id)
  observed_weather['station_id']=std_station_id

  '''
  std_station_id = []
  submission = pd.read_csv('../data/sample_submission.csv')
  for item in submission['test_id'].values:
      id = item.split('_')[0]
      std_station_id.append(id+'_aq')
  
  observed_id = observed_weather['station_id'].tolist()
  diff_id = []
  for item in std_station_id:
      if item not in observed_id:
        diff_id.append(item)

  match_df = observed_weather[observed_weather['station_id']=='zhaitang_aq']
  diff_df = pd.DataFrame()
  for item in diff_id:
      temp = match_df
      temp['station_id'] = item
      diff_df = diff_df.append(temp, ignore_index=True)
  observed_weather = observed_weather.append(diff_df,ignore_index=True)
  '''

  train_date = datetime.strptime("2018-04-30 23:59:59", "%Y-%m-%d %H:%M:%S")
  test_date = datetime.strptime("2018-05-01 00:00:00", "%Y-%m-%d %H:%M:%S")

  train_weather = observed_weather[observed_weather['utc_time']<=train_date]
  test_weather = observed_weather[observed_weather['utc_time']>=test_date]
  test_weather = test_weather.sort_values(by=['station_id','utc_time'])
  train_weather = train_weather.sort_values(by=['station_id','utc_time'])
  
  train_weather['utc_time'] = train_weather['utc_time'].apply(lambda x:x.strftime("%Y-%m-%d %H:%M:%S"))
  print(train_weather['utc_time'])
  test_weather['utc_time'] = test_weather['utc_time'].apply(lambda x:x.strftime("%Y-%m-%d %H:%M:%S"))
  #train_weather = train_weather.dropna(subset=['utc_time'])

  #merge features
  print(train_weather.shape)
  print(train_weather.columns)
  print(air_quality.columns)
  air_quality.columns = ['station_id', 'utc_time', 'PM2.5', 'PM10', 'NO2', 'CO', 'O3', 'SO2']
  train_weather = pd.merge(train_weather, air_quality, on=['station_id','utc_time'], how='left')
  print(train_weather.shape)
  
  train_weather = train_weather.fillna(method='pad')
  train_weather = map_date_features(train_weather)
  print(train_weather.isna().any())
  
  test_weather = map_date_features(test_weather)
  test_weather = test_weather.fillna(method='pad')
  print(test_weather.isna().any())
  
  train_weather = train_weather.dropna()
  test_weather = test_weather.dropna()
  train_weather.to_csv('processed-data/train_weather.csv', index=False)
  test_weather.to_csv('processed-data/test_weather.csv', index=False)
  
  #observed_weather.to_csv('../processed-data/complete_features.csv', index=False)
if __name__ == '__main__':
    #df = pd.read_csv('../processed-data/air_quality.csv')
    #map_date_features(df)
    process_all()