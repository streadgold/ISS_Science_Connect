import sqlite3

def initialize_database(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create the Positions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position_name TEXT NOT NULL
    );
    ''')

    # Create the Slots table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_name TEXT NOT NULL,
        position_id INTEGER NOT NULL,
        FOREIGN KEY (position_id) REFERENCES Positions(id)
    );
    ''')

    # Create the Payloads table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Payloads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payload_name TEXT NOT NULL,
        payload_type TEXT NOT NULL
    );
    ''')

    # Create the FRAMs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FRAMs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fram_name TEXT NOT NULL,
        slot_id INTEGER NOT NULL,
        payload_id INTEGER,
        FOREIGN KEY (slot_id) REFERENCES Slots(id),
        FOREIGN KEY (payload_id) REFERENCES Payloads(id)
    );
    ''')

    # Create the Types table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT NOT NULL
    );
    ''')

    # Create the PayloadTypeAssignments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PayloadTypeAssignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payload_id INTEGER NOT NULL,
        type_id INTEGER NOT NULL,
        FOREIGN KEY (payload_id) REFERENCES Payloads(id),
        FOREIGN KEY (type_id) REFERENCES Types(id)
    );
    ''')

    # Create the History table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS History (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fram_id INTEGER NOT NULL,
        event_date DATE NOT NULL,
        event_description TEXT NOT NULL,
        FOREIGN KEY (fram_id) REFERENCES FRAMs(id)
    );
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    db_name = "database.db"  # Name of the SQLite database file
    initialize_database(db_name)
    print(f"Database '{db_name}' initialized successfully.")
