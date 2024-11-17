import sqlite3


def query_by_location(location):
    # Connect to the database
    conn = sqlite3.connect("experiments.db")
    cursor = conn.cursor()

    # Query the database for the specified location
    cursor.execute('''
        SELECT ExperimentName, Description, Image
        FROM Experiments
        WHERE Location = ?
    ''', (location,))

    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Check if a record was found
    if result:
        experiment_name, description, image = result
        print(f"Experiment Name: {experiment_name}")
        print(f"Description: {description}")
        print(f"Image: {'Available' if image else 'None'}")
        return experiment_name, description, image
    else:
        print(f"No data found for Location: {location}")
        return None, None, None



locations = [
    "JEM EFU1", "JEM EFU2", "JEM EFU3", "JEM EFU4", "JEM EFU5", "JEM EFU6", "JEM EFU7",
    "JEM EFU8", "JEM EFU9", "JEM EFU10", "JEM EFU11", "JEM EFU12", "JEM EFU13",
    "Bartolomeo Slot2", "Bartolomeo Slot3", "Bartolomeo Slot5",
    "ELC-1 FRAM 3", "ELC-3 FRAM 3", "ELC-1 FRAM 8", "ELC-2 FRAM 3",
    "ELC-2 FRAM 7", "ELC-3 FRAM 5", "ELC-4 FRAM 2", "ELC-4 FRAM 3",
    "Columbus EPF1", "Columbus EPF3"
]

for location in locations:
    print(query_by_location(location))
