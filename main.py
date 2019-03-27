import features
import model
import preprocess

preprocess.process_air_quality()
preprocess.process_observed_weather()
preprocess.process_grid_weather()
features.process_all()
model.run()