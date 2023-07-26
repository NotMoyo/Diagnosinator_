import sqlite3 as sql
from my_decorators import benchmark

class Patients_Database():
    #
    @benchmark
    def __init__(self):
        try: 
            if self.connection:
                self.cursor.close()
                self.connection.close()
                self.connection = None
                self.cursor = None
        except:
            pass
        self.database = 'Patients_Database.db'
        self.connection = None
        self.cursor = None
    #
    @benchmark
    def connect_to_database(self):
        if self.connection:
            return
        self.connection = sql.connect(self.database)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS patients(
        MRN INTEGER PRIMARY KEY,
        last_name TEXT,
        first_name TEXT,
        middle_name TEXT,
        date_of_birth TEXT,
        age INTEGER,
        gender TEXT
        )""")
        self.connection.commit()
    #
    @benchmark
    def disconnect_from_database(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None
    #
    @benchmark
    def add_column(self, column_name, data_type):
        alter_query = f"ALTER TABLE patients ADD COLUMN {column_name} {data_type}"
        self.cursor.execute(alter_query)
        self.connection.commit()
        print(f"Column '{column_name}' added successfully.")
    #
    @benchmark
    def find_next_available_mrn(self):
        self.connect_to_database()
        self.cursor.execute("SELECT MAX(mrn) FROM patients")
        highest_mrn = self.cursor.fetchone()[0]
        if highest_mrn == None:
            highest_mrn = 1

        self.disconnect_from_database()
        #
        for mrn in range(1, highest_mrn+2):
            print(f"Checking MRN: {mrn}")

            self.connect_to_database()
            self.cursor.execute("SELECT * FROM patients WHERE mrn = ?", (mrn,))
            patient = self.cursor.fetchone()
            self.disconnect_from_database()
            if patient:
                continue
            else:
                return mrn
        
    #
    @benchmark
    def add_patient(self, 
                    mrn = '',
                    last_name = None,
                    first_name = None,
                    middle_name = None,
                    age = None,
                    gender = None
                    ):
        self.connect_to_database()
        self.cursor.execute("""SELECT * FROM patients WHERE mrn = ? 
            """, (mrn,))
        existing_patient = self.cursor.fetchone()
        if existing_patient:
            print(f"Patient with ID {mrn} already exists in the database.")
        else:
            self.cursor.execute("INSERT INTO patients (mrn, last_name, first_name, middle_name, age, gender)VALUES (?, ?, ?, ?, ?, ?)", (mrn, last_name, first_name, middle_name, age, gender))
            self.connection.commit()
    #
    @benchmark
    def search_patient(self, patient_id):
        self.cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        patient = self.cursor.fetchone()
        if patient:
            print(f"Name: {patient[1]}")
    #
    @benchmark
    def delete_patient(self, mrn):
        self.connect_to_database()
        self.cursor.execute("SELECT * FROM patients WHERE MRN = ?", (mrn,))
        existing_patient = self.cursor.fetchone()
        if existing_patient:
            self.cursor.execute("DELETE FROM patients WHERE MRN = ?", (mrn,))
            self.connection.commit()
        else:
            print(f"Patient with ID {mrn} does not exist in the database.")
        self.disconnect_from_database()
    #
    @benchmark 
    def load_patients_list(self): 
        self.connect_to_database()
        try:
            self.cursor.execute("SELECT MRN, last_name, first_name FROM patients")
            patients = self.cursor.fetchall()
            self.disconnect_from_database()
            return patients
        except sql.Error as e:
            print(f"Error occurred while loading patient data: {str(e)}")
            self.disconnect_from_database()
            return None
    # Patients2: 
    #   [
    #       (1, 'John', 'Doe', None, None, '123 Fake St.', 'Fakeville', 'Fake State', '12345'), 
    #       (2, 'Jane', 'Doe', None, None, '123 Fake St.', 'Fakeville', 'Fake State', '12345'), 
    #       (3, 'John', 'Smith', None, None, '123 Fake St.', 'Fakeville', 'Fake State', '12345')
    #   ]