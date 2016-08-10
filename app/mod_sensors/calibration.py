import pandas as pd
from ..mod_db import *

def calibrate_rssi_baseline(csv, room):
    """
    Takes a CSV file of RSSI readings from an empty room, calculates a
    baseline and writes it to the database. 
    """

    # Reads the input CSV file. 
    df = pd.read_csv(csv)

    # Calculates the baseline as the mode of RSSI values in the infile. 
    baseline = df["rssi"].mode()[0]

    print(baseline)

    # Writes the calculated baseline to the database for that room. 
    query = Rooms.update(rssi_baseline=baseline).where(Rooms.room_number == room)
    query.execute()

def calibrate_audio_baseline():
    """

    """
