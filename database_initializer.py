import sqlite3
import os


def initialize_database(db_name):
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"Existing database '{db_name}' deleted.")

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Experiments (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ExperimentName TEXT NOT NULL,
            Location TEXT NOT NULL,
            Description TEXT,
            Image BLOB
        )
    ''')

    experiments = [
        ("MAXI", "JEM EFU1", "X-ray astronomy from 0.5 to 30 keV", None),
        ("STP-H8", "JEM EFU2", "Payload-COWVR and TEMPEST", None),
        ("OCO-3", "JEM EFU3", "Monitoring of carbon dioxide in the Earth's atmosphere", None),
        ("NREP", "JEM EFU4", "Nanoracks External Platform for launching cubesats.", None),
        ("i-SEEP", "JEM EFU5", "IVA-replaceable Small Exposed Experience Platform JAXA", None),
        ("GEDI", "JEM EFU6", "Global Ecosystem Dynamics Investigation on ISS", None),
        ("STP-H9-SWELL", "JEM EFU7", "A test payload for Laser Communications.", None),
        ("HISUI", "JEM EFU8", "Hyperspectral Image Suite (METI) Replacement for HREP.", None),
        ("CALET", "JEM EFU9", "CALorimetric Electron Telescope (JAXA), observation for high energy cosmic rays.", None),
        ("ECOSTRESS", "JEM EFU10", "Ecosystem Spaceborne Thermal Radiometer Experiment on Space Station.", None),
        ("i-SEEP2", "JEM EFU11", "IVA-replaceable Small Exposed Experience Platform2", None),
        ("CREAM", "JEM EFU12", "Cosmic Ray Energetics and Mass Experiment", None),
        ("ExHAM 1 and 2", "JEM EFU13", "External Facility Handrail Attach Mechanism", None)
    ]

    cursor.executemany('''
        INSERT INTO Experiments (ExperimentName, Location, Description, Image)
        VALUES (?, ?, ?, ?)
    ''', experiments)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' initialized successfully with table 'Experiments'.")


if __name__ == "__main__":
    initialize_database("experiments.db")
