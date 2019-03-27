import pandas as pd
import numpy as np
from evaluation import smape
import lightgbm as lgb

def load_data():
	train = pd.read_csv('processed-data/train_weather.csv')
	test = pd.read_csv('processed-data/test_weather.csv')

	train_label = train[['PM2.5','PM10','O3']]
	train_label = train_label.astype(float)
	train_X = train.drop(['PM2.5','PM10','NO2','CO','O3','SO2','station_id','utc_time'],axis=1)
	station_id = test['station_id'].values
	test =test.drop(['station_id','utc_time'],axis=1)

	return train_X, train_label, test,station_id


def smape_error(preds, train_data):
	labels = train_data.get_label()
	return 'error', np.mean(np.fabs(preds - labels) / (preds + labels) * 2), False

def model(X_train, y_train):
	lgb_eval = lgb.Dataset(X_train[:2000],label=y_train[:2000])
	lgb_train = lgb.Dataset(X_train[2000:], label=y_train[2000:])
    
	model_param = {'lr': 0.005, 'depth': 10, 'tree': 1000, 'leaf': 400, 'sample': 0.9, 'seed': 3}
	params = {
        'task': 'train',
        'boosting_type': 'gbdt',
        'objective': 'regression_l2',
        'metric': {'l2', 'l1'},
        'max_depth': model_param['depth'],
        'num_leaves': model_param['leaf'],
        'min_data_in_leaf': 20,
        'learning_rate': model_param['lr'],
        'feature_fraction': 1,
        'bagging_fraction': model_param['sample'],
        'bagging_freq': 1,
        'bagging_seed': model_param['seed'],
        'verbose': 0
	}

	bst = lgb.train(
        params,
        lgb_train,
        num_boost_round=1000,
        valid_sets=lgb_eval,
        feval=smape_error,
        early_stopping_rounds=10,
        verbose_eval=True
    )
	return bst


def metrict(X,y,PM2_bst,PM10_bst,O3_bst):
	PM2_result = PM2_bst.predict(X)
	PM10_result = PM10_bst.predict(X)
	O3_result = O3_bst.predict(X)

	sampe_Pm2 = smape(y[:,0], PM2_result)
	sampe_Pm10 = smape(y[:,1], PM10_result)
	smape_O3 = smape(y[:,2], O3_result)
	total_smape = (sampe_Pm10+smape_O3+sampe_Pm2)/3.0
	print("smape=",total_smape)


def run():
	train_X, train_label, test,station_id = load_data()
	train_label = np.asarray(train_label)
	PM2_bst = model(train_X, train_label[:,0])
	PM10_bst = model(train_X, train_label[:,1])
	O3_bst = model(train_X, train_label[:,2])

	metrict(train_X, train_label, PM2_bst,PM10_bst,O3_bst)
	#predict 
	PM2_result = PM2_bst.predict(test)
	PM10_result = PM10_bst.predict(test)
	O3_result = O3_bst.predict(test)

	sample_submission = pd.read_csv('data/sample_submission.csv')['test_id']
	result = np.c_[station_id, PM2_result, PM10_result, O3_result]
	result = pd.DataFrame(result,columns=['test_id','PM2.5','PM10','O3'])


	std_station_id = []
	submission = pd.read_csv('data/sample_submission.csv')
	for item in submission['test_id'].values:
		id = item.split('_')[0]
		std_station_id.append(id+'_aq')
	
	std_station_id = list(set(std_station_id))
	
	observed_id = result['test_id'].tolist()
	observed_id = list(set(observed_id))

	diff_id = []
	for item in std_station_id:
		if item not in observed_id:
			diff_id.append(item)
	
	match_df = result[result['test_id']=='zhaitang_aq']
	diff_df = pd.DataFrame()
	for item in diff_id:
		tmp = match_df
		tmp['test_id'] = item
		diff_df = diff_df.append(tmp, ignore_index=True)
	result = result.append(diff_df,ignore_index=True)
	result_id = list(set(result['test_id'].tolist()))
	result = result.sort_values(by='test_id')
	
	predict_result = pd.DataFrame()
	for item in std_station_id:
		if item not in result_id:
			print(item)
			result = result.drop(item, axis=0)		 
	result['test_id'] = submission['test_id']
	result = result.dropna()
	result = result.sort_values(by='test_id')

	result.to_csv('processed-data/submission.csv', index=False)

if __name__ == '__main__':
	run()