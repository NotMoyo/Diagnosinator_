import sqlite3 as sql
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.MainWindow_Settings()
    
    def init_Database(self):
        self.Patients_Data = Patients_Database('Patients_Database.db')
        self.Patients_Data.connect()

    def MainWindow_Settings(self):
        self.setWindowTitle("Diagnosinator")
        self.setGeometry(100, 100, 1440, 900)
        self.mainwindow_layout = qtw.QGridLayout(self)
        self.mw_layout_widget = qtw.QWidget()
        self.mw_layout_widget.setLayout(self.mainwindow_layout)
        self.setCentralWidget(self.mw_layout_widget)
        self.mainwindow_layout.setAlignment(qtc.Qt.AlignTop)
        # self.mainwindow_layout.
        self.setLayout(self.mainwindow_layout)
        self.setStyleSheet('''
            /* Main window */
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }

            /* Toolbar styles */
            QToolBar {
                background-color: #363636;
                color: #ffffff;
                border: none;
                spacing: 3px;
            }

            QToolBar QToolButton {
                background-color: #363636;
                color: #ffffff;
                border: none;
                padding: 5px;
            }

            /* Status bar styles */
            QStatusBar {
                background-color: #363636;
                color: #ffffff;
                border-top: 1px solid #8e8e8e;
            }

            /* Widget styles */
            QLabel {
                color: #ffffff;
            }

            QPushButton {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #8e8e8e;
                padding: 5px 10px;
            }

            QLineEdit {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #8e8e8e;
                padding: 5px;
                selection-background-color: #4a90d9;
            }

            QComboBox {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #8e8e8e;
                padding: 5px;
                selection-background-color: #4a90d9;
            }

            QSpinBox {
                background-color: #363636;
                color: #ffffff;
                border: 1px solid #8e8e8e;
                padding: 5px;
                selection-background-color: #4a90d9;
            }

            /* Scroll bar styles */
            QScrollBar:vertical {
                background-color: #2b2b2b;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }

            QScrollBar::handle:vertical {
                background-color: #505050;
                min-height: 20px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background-color: none;
            }
        ''')
        self.MainWindow_Toolbar()

    def MainWindow_Toolbar(self):
        self.mw_toolbar = self.addToolBar("Toolbar")
        self.mw_toolbar.setMovable(False)
        self.mw_toolbar.setFloatable(False)
        self.mw_toolbar.setToolButtonStyle(1)
        self.MainWindow_Statusbar()

        #
        self.mw_toolbar.addAction("Add Patient", self.open_add_patient_window)
        self.mw_toolbar.addAction("Tools", self.toolbar_tools)
        self.mw_toolbar.addAction("Exit", self.close)

    def toolbar_tools(self):
        print('Not Made Yet')
        
    def MainWindow_Statusbar(self):
        self.mw_statusbar = self.statusBar()
        self.setStatusBar(self.mw_statusbar)
        #
        self.statusbar_layout_widget = qtw.QWidget()
        self.statusbar_layout = qtw.QHBoxLayout()
        self.statusbar_layout_widget.setLayout(self.statusbar_layout)
        self.mw_statusbar.addWidget(self.statusbar_layout_widget)
        # self.statusbar_layout.setContentsMargins(0, 0, 0, 0)
        #
        self.current_DateTime_Label = qtw.QLabel()
        self.status_combobox = qtw.QComboBox()
        self.status_combobox.addItems(["Ready", "Busy", "Offline"])
        #
        self.statusbar_layout.addWidget(self.status_combobox)
        self.statusbar_layout.addSpacerItem(qtw.QSpacerItem(10000, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))
        self.statusbar_layout.addWidget(self.current_DateTime_Label)
        #
        self.statusbar_layout.setAlignment(self.current_DateTime_Label, qtc.Qt.AlignRight)
        self.statusbar_layout.setAlignment(self.status_combobox, qtc.Qt.AlignLeft)
        #
        self.MainWindow_Patient_List()
        self.update_DateTime()

    def MainWindow_Patient_List(self):
        self.mw_patient_list = qtw.QListWidget()
        self.mw_patient_list.setAlternatingRowColors(True)
        # self.mw_patient_list.adjustSize()
        self.mainwindow_layout.addWidget(self.mw_patient_list, 0, 0, 1, 1)
        self.mainwindow_layout.addItem(qtw.QSpacerItem(0,0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding), 1, 1, 1, 1)
        self.mainwindow_layout.setContentsMargins(25, 25, 25, 25)
        self.load_patients_list()
        

    # # # ^ ^  Widgets  ^ ^ # # #
      # #  #  #  # #  #  #  # # 
    # # # V v Functions v V # # #
    def load_patients_list(self):
        self.patients_data = sql.connect('Patients_Database.db')
        self.mw_patient_list.addItems(
            ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE", "FFFF", "GGGG", "HHHH", "IIII", "JJJJ", "KKKK", "LLLL", "MMMM", "NNNN", "OOOO", "PPPP", "QQQQ", "RRRR", "SSSS", "TTTT", "UUUU", "VVVV", "WWWW", "XXXX", "YYYY", "ZZZZ"]
        )
        try:
            self.patients_data_cursor = self.patients_data.cursor()
            self.patients_data_cursor.execute("SELECT * FROM patients")
        except:
            pass

        # print(self.mw_patient_list.children())
        for child in self.children():
            try:
                print(child.children())
            except:
                pass
        
            

    def open_add_patient_window(self):
        self.add_patient_window = Add_Patient_Window()
        
        self.add_patient_window.show()

    def update_DateTime(self):
        self.current_DateTime_Label.setText(qtc.QDateTime.currentDateTime().toString("MM-dd-yyyy hh:mm:ss"))
        qtc.QTimer.singleShot(1000, self.update_DateTime)

class Add_Patient_Window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.Patients_Data = Patients_Database('Patients_Database.db')
        self.Patients_Data.connect()
        self.setWindowTitle("Add Patient")
        self.setGeometry(100, 100, 500, 400)
        self.initUI()

    def initUI(self):
        self.apw_layout = qtw.QGridLayout()
        self.setLayout(self.apw_layout)
        #
        self.apw_clear_button = qtw.QPushButton("Clear")
        self.apw_save_button = qtw.QPushButton("Save")
        #
        self.apw_id_label = qtw.QLabel("ID:")
        self.apw_id_input = qtw.QLineEdit()
        self.apw_id_input.setReadOnly(True)
        self.apw_name_label = qtw.QLabel("Name:")
        self.apw_name_input = qtw.QLineEdit()
        self.apw_age_label = qtw.QLabel("Date of Birth:")
        self.apw_age_input = qtw.QLineEdit()
        self.apw_gender_label = qtw.QLabel("Gender:")
        self.apw_gender_input = qtw.QComboBox()
        self.apw_gender_input.addItems(["","Male", "Female"])
        #
        self.apw_layout.addWidget(self.apw_save_button, 0, 0)
        self.apw_layout.addWidget(self.apw_clear_button, 0, 1)
        self.apw_layout.addWidget(self.apw_id_label, 1, 0)
        self.apw_layout.addWidget(self.apw_id_input, 1, 1)
        self.apw_layout.addWidget(self.apw_name_label, 2, 0)
        self.apw_layout.addWidget(self.apw_name_input, 2, 1)
        self.apw_layout.addWidget(self.apw_age_label, 3, 0)
        self.apw_layout.addWidget(self.apw_age_input, 3, 1)
        self.apw_layout.addWidget(self.apw_gender_label, 4, 0)
        self.apw_layout.addWidget(self.apw_gender_input, 4, 1)
        #
        self.apw_layout.setAlignment(self.apw_id_label, qtc.Qt.AlignRight)
        self.apw_layout.setAlignment(self.apw_name_label, qtc.Qt.AlignRight)
        self.apw_layout.setAlignment(self.apw_age_label, qtc.Qt.AlignRight)
        self.apw_layout.setAlignment(self.apw_gender_label, qtc.Qt.AlignRight)




class Patients_Database:
    def __init__(self, patients_db):
        self.patients_db = patients_db
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sql.connect(self.patients_db)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        age INTEGER,
        gender TEXT
        )""")
        self.connection.commit()

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None

    def add_column(self, column_name, data_type):
        alter_query = f"ALTER TABLE patients ADD COLUMN {column_name} {data_type}"
        self.cursor.execute(alter_query)
        self.connection.commit()
        print(f"Column '{column_name}' added successfully.")

    def add_patient(self, patient_id, name, age, gender):
        self.cursor.execute("""SELECT * FROM patients WHERE id = ? 
            """, (patient_id,))
        existing_patient = self.cursor.fetchone()
        if existing_patient:
            print(f"Patient with ID {patient_id} already exists in the database.")
        else:
            self.cursor.execute("INSERT INTO patients (id, name, age, gender) VALUES (?, ?, ?, ?)",
                                (patient_id, name, age, gender))
            self.connection.commit()
            print(f"Patient with ID {patient_id} added successfully.", (patient_id,))


    def search_patient(self, patient_id):
        self.cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        patient = self.cursor.fetchone()
        if patient:
            print(f"Name: {patient[1]}")

    def delete_patient(self, patient_id):
        self.cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        existing_patient = self.cursor.fetchone()
        if existing_patient:
            self.cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
            self.connection.commit()
        else:
            print(f"Patient with ID {patient_id} does not exist in the database.")
      


Patients_Data = Patients_Database('Patients_Database.db')
# Patients_Data.connect()





if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    mw.show()
    app.exec_()




