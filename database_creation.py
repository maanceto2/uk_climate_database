import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('uk_climate.db')
cursor = conn.cursor()

# Create a new table
cursor.executescript('''
    CREATE TABLE Weather_Stations (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT,
    latitude REAL,
    longitude REAL,
    elevation REAL,
    region TEXT,
    location TEXT
);

CREATE TABLE Weather_Data (
    data_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER,
    year INTEGER,
    month INTEGER,
    tmax REAL,
    tmin REAL,
    af INTEGER,
    rain REAL,
    sun REAL,
    FOREIGN KEY (station_id) REFERENCES Weather_Stations (station_id)
);
''')

# Read the CSV file
df = pd.read_csv('weather_stations.csv')

# Insert the data into the database 
df.to_sql('Weather_Stations', conn, if_exists='append', index=False)

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()