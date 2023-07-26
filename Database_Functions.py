import typing
import sqlite3
# from my_decorators import benchmark

# Path: Database_Functions.py
# Create a database connection to a SQLite database.
def create_connection(db_file: str) -> sqlite3.Connection:
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to database successful")
    except sqlite3.Error as e:
        print(e)
        print("Error creating connection to database")
    return conn

# Path: Database_Functions.py
# Create a table from the create_table_sql statement.
def create_table(conn: sqlite3.Connection, table_name: str) -> None:
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param table_name: name of table to create
    :return: None
    """
    sql = f""" CREATE TABLE IF NOT EXISTS {table_name} (
                id integer PRIMARY KEY,
                first_name text, 
                last_name text, 
                email text,
                phone_number text,
                address text,
                city text,
                state text,
                zip_code text
            ); """
    try:
        c = conn.cursor()
        c.execute(sql)
        print("Table created successfully")
    except sqlite3.Error as e:
        print(e)
        print("Error creating table")

# Path: Database_Functions.py
# Insert a patient into the database.
def insert_patient(conn: sqlite3.Connection, patient: typing.Tuple) -> None:
    """ insert a patient into the database
    :param conn: Connection object
    :param patient: tuple of patient information
    :return: None
    """
    sql = ''' INSERT INTO patients(id,first_name,last_name,email,phone_number,address,city,state,zip_code)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    try:
        c = conn.cursor()
        c.executemany(sql, patient)
        conn.commit()
        print("Patient inserted successfully")
    except sqlite3.Error as e:
        print(e)
        print("Error inserting patient")



connection = create_connection("Patients_Database.db")
create_table(connection, "patients")
insert_patient(
    connection,[
    (
        1,
        "John",
        "Doe",
        None,
        None,
        "123 Fake St.",
        "Fakeville",
        "Fake State",
        "12345"
    ),
    (
        2,
        "Jane",
        "Doe",
        None,
        None,
        "123 Fake St.",
        "Fakeville",
        "Fake State",
        "12345"
    ),
    (
        3,
        "John",
        "Smith",
        None,
        None,
        "123 Fake St.",
        "Fakeville",
        "Fake State",
        "12345"
    )
]
)

# Path: Database_Functions.py
# Retrieve all patients from the database.
def select_all_patients(conn: sqlite3.Connection) -> None:
    """ select all patients from the database
    :param conn: Connection object
    :return: None
    """
    sql = "SELECT * FROM patients"
    
    try:
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        print("All patients retrieved successfully")
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)
        print("Error selecting all patients")
    a, *_  = c.execute(sql).fetchall()
    print(a, sep="\n")
    print('cat')

    def fake_function(letter):
        print(letter)
        return fake_function(letter)

    lsss = [*a]
    letters = [entry for entry in str(c.execute(sql).fetchall())]
    # print(letters)

    
    fake_function(lambda x: x for x in letters) 

select_all_patients(connection)