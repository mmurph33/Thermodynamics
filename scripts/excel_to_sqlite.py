import pandas as pd
import sqlite3
import os



# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'table.xlsx')
DB_PATH = os.path.join(BASE_DIR, 'db', 'properties_of_substances.db')

# Before connecting to the SQLite database
if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))
# Read data from Excel
data = pd.read_excel(DATA_PATH, engine='openpyxl')

# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH)

# Insert data from Excel into the SQLite database
data.to_sql('your_table_name', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()
