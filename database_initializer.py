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
        ("MAXI", "JEM EFU1", "X-ray astronomy from 0.5 to 30 keV.", "maxi_iss.jpg"),
        ("STP Houston 8 Payload-COWVR and TEMPEST", "JEM EFU2", "Launched on SpaceX CRS-24 in 2021", "STP-H8-Payload-COWVR_and_TEMPEST.png"),
        ("OCO3", "JEM EFU3", "Monitoring of Carbon Dioxide in Earth's Atmosphere", "OCO3.png"),
        ("NREP", "JEM EFU4", "Nanoracks External Platform", "Nanoracks-Extenal-Platform.jpg"),
        ("i-SEEP", "JEM EFU5", "IVA-replaceable Small Exposed Experience Platform JAXA", "i-SEEP.jpg"),
        ("GEDI", "JEM EFU6", "Global Ecosystem Dynamics Investigation on ISS", "ISS-GEDI-Image.jpeg"),
        ("STP-H9-SWELL", "JEM EFU7", "A test payload for Laser Communications.", "STP-H9-SWELL.avif"),
        ("HISUI", "JEM EFU8", "Hyperspectral Image Suite (METI) Replacement for HREP.", "Jaxa-External-Platform.jpg"),
        ("CALET", "JEM EFU9", "CALorimetric Electron Telescope (JAXA), observation for high energy cosmic rays.", "CALET.jpg"),
        ("ECOSTRESS", "JEM EFU10", "Measures the temperature of plants to understand plant stress", "ECOSTRESS.jpg"),
        ("i-SEEP2", "JEM EFU11", "IVA-replaceable Small Exposed Experience Platform2", "Jaxa-External-Platform.jpg"),
        ("CREAM", "JEM EFU12", "Cosmic Ray Energetics and Mass Experiment", "Jaxa-External-Platform.jpg"),
        ("ExHAM 1 and 2", "JEM EFU13", "External Facility Handrail Attach Mechanism", "ExHam-ISS.jpg"),
        ("ArgUS 1", "Bartolomeo Slot2", "External platform hosting Ball Aerospace’s Red Panda, Thales Alenia Space’s IMAGIN-e, and SEN’s SpaceTV-1", "Jaxa-External-Platform.jpg"),
        ("m-NLP", "Bartolomeo Slot3", "multi-Needle Langmuir Probe (m-NLP) will map the ionospheric plasma surrounding the ISS to an unprecedented high level of detail", "Jaxa-External-Platform.jpg"),
        ("ArgUS 2", "Bartolomeo Slot5", "ArgUS is an adaptation to the European Space Agency (ESA) external platform Bartolomeo, enabling it to accommodate up to 10 smaller payloads in one slot. ArgUS is compatible with all Bartolomeo locations, which allows unobstructed viewing in all directions", "Jaxa-External-Platform.jpg"),
        ("AWE", "ELC-1 FRAM 3", "Atmospheric Waves Experiment (AWE), Studies gravity waves in the Earth’s upper atmosphere by measuring emissions from hydroxyl groups in the infrared.", "Jaxa-External-Platform.jpg"),
        ("CODEX", "ELC-3 FRAM 3", "Coronal Diagnostic Experiment (CODEX) is Solar coronagraph that observes the temperature, velocity, and density of the corona.", "Jaxa-External-Platform.jpg"),
        ("EMIT", "ELC-1 FRAM 8", "", "Jaxa-External-Platform.jpg"),
        ("MISSE-FF", "ELC-2 FRAM 3", "Tested performance of materials exposed to space environment", "Jaxa-External-Platform.jpg"),
        ("NICER", "ELC-2 FRAM 7", "X-ray telescope for studying neutron stars", "Jaxa-External-Platform.jpg"),
        ("TSIS", "ELC-3 FRAM 5", "Measures solar irradiance (total amount and distribution across different bands)", "Jaxa-External-Platform.jpg"),
        ("MUSES", "ELC-4 FRAM 2", "MUSES hosting DESIS", "Jaxa-External-Platform.jpg"),
        ("SAGE III", "ELC-4 FRAM 3", "Measures stratospheric ozone, aerosols, and water vapor", "Jaxa-External-Platform.jpg"),
        ("STP-H7", "Columbus EPF1", "", "Jaxa-External-Platform.jpg"),
        ("ASIM", "Columbus EPF3", "Atmosphere-Space Interactions Monitor (ASIM)", "Jaxa-External-Platform.jpg")
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
