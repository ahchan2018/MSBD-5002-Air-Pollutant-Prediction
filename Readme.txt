src: save all the codes
data:store the original data files
processed-data:store all the files that have been processed

In folder src, there are 5 python sciripts:

main.py
Program entry

EDA.ipnyb
Including EDA and data pre-processing, with visualizations.

preprocess.py:
Preprocess the original files, its function is merging different datas, including air_quality, observed files. Besides, the merged files were store in folder 'processed-data'. Other procedure includes data cleaning, as you can see in its three functons: process_air_quality(), process_observed_weather(), and process_grid_weather() by updating the problematic column names, dates format, etc.

features.py
For features engineerning, I did the feature extraction including dates, temperature of each station, wind direction, etc. And then I did the missing data by filling 0.

model.py
The model of the project is LightGBM, including loading features, training model and making predictions

evaluation.py
Use the model to evaluate the function and the SMAPE as a score function.