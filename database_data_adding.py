import pandas as pd
import sqlite3
import os

# Connect to the SQLite database
conn = sqlite3.connect('uk_climate.db')

# Get the list of CSV files in the folder
csv_files = os.listdir('./csv_files')

# Loop through each CSV file
for file in csv_files:
    # Get the station name from the file name
    station_name = file.split('.')[0]

    # Read the CSV file
    df = pd.read_csv(os.path.join('./csv_files', file))

    #Ignore Unnamed column:
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

    # Rename the columns to match the Weather_Data table
    df = df.rename(columns={'yyyy': 'year', 'mm': 'month'})

    # Get the station_id from the Weather_Stations table
    cursor = conn.cursor()
    cursor.execute("SELECT station_id FROM Weather_Stations WHERE station_name = ?", (station_name,))
    result = cursor.fetchone()
    if result is not None:
        station_id = result[0]
    else:
        print(f"Skipping station_name '{station_name}'")
        continue
        
    # Add the station_id to the DataFrame
    df['station_id'] = station_id

    # Insert the data into the Weather_Data table
    df.to_sql('Weather_Data', conn, if_exists='append', index=False)

# Close the connection
conn.close()