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

    # Check if a record was found
    if result:
        experiment_name, description, image = result
        print(f"Experiment Name: {experiment_name}")
        print(f"Description: {description}")
        print(f"Image: {'Available' if image else 'None'}")
    else:
        print(f"No data found for Location: {location}")

    # Close the connection
    conn.close()


locations = ["JEM EFU1", "JEM EFU2"]

for location in locations:
    print(query_by_location(location))
