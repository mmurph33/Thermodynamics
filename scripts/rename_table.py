import sqlite3

# Define the path to your SQLite database
DB_PATH = "/Users/mattmurphy/Thermo Program/Thermo/db/properties_of_substances.db"

# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Rename the table
cursor.execute("ALTER TABLE your_table_name RENAME TO substance_properties")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table renamed successfully!")
