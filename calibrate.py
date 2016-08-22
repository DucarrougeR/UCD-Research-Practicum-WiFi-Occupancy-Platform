"""
Runs scripts to generate predictions for the entire database, calculate room scores and calibrate the sensor baselines in the database. 
"""
from app.mod_stat import *
from app.mod_sensors import *

predict.generate_scores()
predict.predict_all()
calibration.calibrate_baselines("app/mod_sensors/data/B002-21-08-2016-14-08-50.csv", "B002")
calibration.calibrate_baselines("app/mod_sensors/data/B003-21-08-2016-14-08-50.csv", "B003")
calibration.calibrate_baselines("app/mod_sensors/data/B004-21-08-2016-14-08-50.csv", "B004")
