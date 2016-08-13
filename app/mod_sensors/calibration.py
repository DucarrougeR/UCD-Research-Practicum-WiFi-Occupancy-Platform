import pandas as pd
from ..mod_db import *

def calibrate_baselines(csv, room):
    """
    Takes a CSV file of sensor readings from an empty room, calculates 
    baselines and writes them to the database. 
    """

    # Reads the input CSV file. 
    df = pd.read_csv(csv)

    # Calculates the baseline as the mode of RSSI values in the infile. 
    baseline_audio = df["maxamp"].mode()[0]
    baseline_rssi = df["rssi"].mode()[0]

    # Writes the calculated baseline to the database for that room. 
    query = Rooms.update(room_rssi_baseline=baseline_rssi, room_audio_baseline=baseline_audio).where(Rooms.room_number == room)
    query.execute()

