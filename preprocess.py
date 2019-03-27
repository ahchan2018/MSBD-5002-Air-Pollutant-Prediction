import pandas as pd
import numpy as np
def process_air_quality():
    root_path = 'data/'
    files = ['aiqQuality_201804.csv', 
			'airQuality_201701-201801.csv',
			'airQuality_201802-201803.csv']
    
    air_quality = pd.DataFrame()
    for file in files:
        abs_path = root_path+file
        current_df = pd.read_csv(abs_path)
        air_quality = air_quality.append(current_df,ignore_index=True)
    air_quality = air_quality.sort_values(by='utc_time')
    air_quality.to_csv('processed-data/air_quality.csv', index=False)


def process_observed_weather():
    root_path = 'data/'
    files = ['observedWeather_201802-201803.csv','observedWeather_201804.csv',
			'observedWeather_20180501-20180502.csv']
    init_observed = pd.read_csv(root_path+'observedWeather_201701-201801.csv')
    init_observed = init_observed.drop(['longitude','latitude'], axis=1)
    observedWeather_201804 = pd.read_csv(root_path+files[1])
    observedWeather_201804 = observedWeather_201804.drop('id', axis=1)
    observedWeather_20180501_20180502 = pd.read_csv(root_path+files[2])
    observedWeather_20180501_20180502 = observedWeather_20180501_20180502.drop('id',axis=1)
	

    observedWeather_201802_201803 = pd.read_csv(root_path+files[0])

    observed_weather = pd.concat([init_observed, observedWeather_201804,
								 observedWeather_20180501_20180502,
								 observedWeather_201802_201803], ignore_index=True)
    observed_weather = observed_weather.sort_values(by=['utc_time'])
    std_time = []
    for item in observed_weather['utc_time'].values:
        try:
            item = item.split(' ')
            pre = item[0].split('/')
            time = pre[0]+'-'+pre[1]+'-'+pre[2]+' '+item[1]
            std_time.append(time)
        except:
            std_time.append(item[0])
    observed_weather['utc_time'] = std_time
    observed_weather.to_csv('processed-data/observed_weather.csv', index=False)


def process_grid_weather():
    grid_weather_201804 = pd.read_csv('data/gridWeather_201804.csv')
    grid_weather_201804 = grid_weather_201804.drop('id', axis=1)
    grid_weather_20180501_20180502 = pd.read_csv('data/gridWeather_20180501-20180502.csv')
    grid_weather_20180501_20180502 = grid_weather_20180501_20180502.drop('id',axis=1)

    gridWeather_201701_201803 = pd.read_csv('data/gridWeather_201701-201803.csv')
    gridWeather_201701_201803 = gridWeather_201701_201803.drop(['longitude','latitude'], axis=1)
    grid_weather = pd.concat([grid_weather_201804, gridWeather_201701_201803,
							 grid_weather_20180501_20180502], ignore_index=True)
	
    grid_weather = grid_weather.sort_values(by=['utc_time'])
    grid_weather.to_csv('processed-data/grid_weather.csv', index=False)
    
    grid_weather.describe()

if __name__ == '__main__':
    process_air_quality()
    process_observed_weather()
    process_grid_weather()




