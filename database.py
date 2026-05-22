import sqlite3

# Create connection
connection = sqlite3.connect("predictions.db")

# Create cursor
cursor = connection.cursor()

# Create table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS predictions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        message TEXT,

        result TEXT

    )
    '''
)

print("✅ Database and table created successfully")

connection.commit()

connection.close()