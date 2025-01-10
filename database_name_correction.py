import sqlite3
import re

# Connect to your SQLite database
conn = sqlite3.connect('UK_climate_data.db')
cursor = conn.cursor()

# Fetch current table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Function to correct table names
def correct_table_name(name):
    # Replace invalid characters with underscores
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

# Rename tables
for table in tables:
    old_name = table[0]
    new_name = correct_table_name(old_name)
    if old_name != new_name:
        cursor.execute(f'ALTER TABLE "{old_name}" RENAME TO {new_name}')
        conn.commit()

# Verify the changes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
updated_tables = cursor.fetchall()
print(updated_tables)

# Close the connection
cursor.close()
conn.close()
