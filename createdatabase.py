import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('car_listings.db')

# Create a new SQLite table with appropriate columns
conn.execute('''
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY,
    make TEXT,
    model TEXT,
    year INTEGER,
    price REAL,
    mileage INTEGER
);
''')

print("Table created successfully")

# Close the connection to the database
conn.close()
