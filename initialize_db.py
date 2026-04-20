import sqlite3

DB_NAME = 'example.db'


def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    print("Connected to the database.")
    cursor = connection.cursor()
    print("Cursor created.")
    # Create a sample table
    print("Creating table if it does not exist...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banking
            (id integer primary key, 
            name text, 
            age integer, 
            balance real)
    ''')

    print("Table created.")

    # Insert sample data
    print("Inserting sample data...")
    cursor.execute("SELECT COUNT(*) FROM banking")
    count = cursor.fetchone()[0]
    if count == 0: # Get rid of duplicate users being added
        cursor.execute('''
            INSERT INTO banking (name, age, balance) VALUES
            ('Harry', 20, 1989.3),
            ('Rose', 34, 12),
            ('Charlie', 45, 67.9)
        ''')
    print("Sample data inserted.")
    # Commit, close connection
    print("Committing changes... closing the connection...")
    connection.commit()
    connection.close()


initialize_database()