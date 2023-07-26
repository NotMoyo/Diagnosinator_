from my_decorators import benchmark
import sqlite3 as sql
import time
from Patients_Database import Patients_Database
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

class MainWindow(qtw.QMainWindow):
    #
    @benchmark
    def __init__(self):
        super().__init__()
        self.PT_DB = Patients_Database()
        self.build_main_window()
    #
    @benchmark
    def build_main_window(self):
        #
        screen_resolution = qtw.QApplication.desktop().screenGeometry()
        desired_width = screen_resolution.width() * 0.9
        desired_height = screen_resolution.height() * 0.9
        self.setWindowTitle("Diagnosinator")
        self.resize(int(desired_width), int(desired_height))
        self.move(int(desired_width * 0.02), int(desired_height * 0.02))
        #
        self.main_window_grid_layout = qtw.QGridLayout(self)
        self.main_window_grid_layout.setColumnStretch(0, 1)
        self.main_window_grid_layout.setRowStretch(0, 1)
        #
        self.main_window_central_widget = qtw.QWidget()
        self.main_window_central_widget.setLayout(self.main_window_grid_layout)
        #
        self.setCentralWidget(self.main_window_central_widget)
        self.setLayout(self.main_window_grid_layout)
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
        #
        self.build_main_window_toolbar()
    #
    @benchmark
    def build_main_window_toolbar(self):
        #
        self.main_window_toolbar = self.addToolBar("Toolbar")
        self.main_window_toolbar.setMovable(False)
        self.main_window_toolbar.setFloatable(False)
        self.main_window_toolbar.setToolButtonStyle(1)
        #
        self.main_window_toolbar.addAction("Add Patient", self.open_patient_add_window)
        self.main_window_toolbar.addAction("Exit", self.close)
        #
        self.build_main_window_statusbar()
    #
    @benchmark
    def build_main_window_statusbar(self):
        #
        self.main_window_statusbar = self.statusBar()
        self.setStatusBar(self.main_window_statusbar)
        #
        self.statusbar_layout_widget = qtw.QWidget()
        self.statusbar_hbox_layout = qtw.QHBoxLayout()
        self.statusbar_layout_widget.setLayout(self.statusbar_hbox_layout)
        self.main_window_statusbar.addWidget(self.statusbar_layout_widget)
        #
        self.current_datetime_label = qtw.QLabel()
        #
        self.statusbar_hbox_layout.addSpacerItem(qtw.QSpacerItem(10000, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))
        self.statusbar_hbox_layout.addWidget(self.current_datetime_label)
        #
        self.statusbar_hbox_layout.setAlignment(self.current_datetime_label, qtc.Qt.AlignRight)
        #
        self.build_main_window_patients_table()
        self.update_datetime()
    #
    @benchmark
    def build_main_window_patients_table(self):
        #
        self.main_window_patients_table = qtw.QTableWidget()
        self.main_window_patients_table.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        self.main_window_patients_table.setContentsMargins(0, 0, 0, 0)
        self.main_window_patients_table.verticalHeader().setVisible(False)
        self.main_window_patients_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.main_window_patients_table.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        self.main_window_patients_table.setAlternatingRowColors(True)
        self.main_window_patients_table.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        self.main_window_grid_layout.addWidget(self.main_window_patients_table, 0, 0)
        self.main_window_grid_layout.addItem(qtw.QSpacerItem(0,0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding), 1, 1, 1, 1)
        self.main_window_grid_layout.setContentsMargins(25, 25, 25, 25)
        self.populate_main_window_patients_table(self.PT_DB.load_patients_list())
        #
        #
        #
        #
        #
        

    # # # ^ ^  Widgets  ^ ^ # # #
      # #  #  #  # #  #  #  # # 
    # # # V v Functions v V # # #

    @benchmark
    def populate_main_window_patients_table(self, patients):
        #
        self.main_window_patients_table.clear()
        #
        self.headerlabels_main_window_patients_table = ["MRN", "Last Name", "First Name", "Middle Name"]
        self.main_window_patients_table.setColumnCount(len(self.headerlabels_main_window_patients_table))
        self.main_window_patients_table.setHorizontalHeaderLabels(self.headerlabels_main_window_patients_table)
        self.main_window_patients_table.setRowCount(len(patients))
        #
        for row, patient in enumerate(patients):    
                for col in range(3):
                    if col == None:
                        pass
                    else:
                        self.main_window_patients_table.setItem(row, col, qtw.QTableWidgetItem(str(patient[col])))
                
    

        
            
    @benchmark
    def open_patient_add_window(self):
        self.patient_add_window = Patient_add_Window()
        
        
        self.patient_add_window.show()
    #
    def update_datetime(self):
        self.current_datetime_label.setText(qtc.QDateTime.currentDateTime().toString("MM-dd-yyyy hh:mm:ss"))
        qtc.QTimer.singleShot(1000, self.update_datetime)

class Patient_add_Window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add Patient")
        self.patient_add_window_layout = qtw.QGridLayout()
        self.setLayout(self.patient_add_window_layout)
        self.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        
        #

        self.patient_add_window_fields = {
            "mrn_label": qtw.QLabel("MRN:"),
            "mrn_input": qtw.QLineEdit(),
            "last_name_label": qtw.QLabel("Last Name:"),
            "last_name_input": qtw.QLineEdit(),
            "first_name_label": qtw.QLabel("First Name:"),
            "first_name_input": qtw.QLineEdit(),
            "middle_name_label": qtw.QLabel("Middle Name:"),
            "middle_name_input": qtw.QLineEdit(),
            "dob_label": qtw.QLabel("Date of Birth:"),
            "dob_input": qtw.QLineEdit(),
            "gender_label": qtw.QLabel("Gender:"),
            "gender_input": qtw.QComboBox(),
            "clear_button": qtw.QPushButton("Clear"),
            "save_button": qtw.QPushButton("Save")
        }
        #
        # for widget in self.patient_add_window_fields.values():
        #     widget.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        #
        self.patient_add_window_fields["mrn_input"].setText(str(mw.PT_DB.find_next_available_mrn()))
        self.patient_add_window_fields["mrn_input"].setReadOnly(True)
        self.patient_add_window_fields["mrn_input"].setEnabled(False)
        # Add items to the gender combo box
        self.patient_add_window_fields["gender_input"].addItems(["", "Male", "Female"])
        #
        for row, widget in enumerate(self.patient_add_window_fields.values(), start=1):
            if isinstance(widget, qtw.QLabel):
                self.patient_add_window_layout.addWidget(widget, row, 0)
                self.patient_add_window_layout.setAlignment(widget, qtc.Qt.AlignRight)
            elif isinstance(widget, qtw.QLineEdit):
                self.patient_add_window_layout.addWidget(widget, row-1, 1)
            elif isinstance(widget, qtw.QComboBox):
                self.patient_add_window_layout.addWidget(widget, row-1, 1)
            elif isinstance(widget, qtw.QPushButton):
                self.patient_add_window_layout.addWidget(widget, row-1, 1)
                self.patient_add_window_layout.setAlignment(widget, qtc.Qt.AlignRight)
        #
        self.patient_add_window_fields["clear_button"].clicked.connect(lambda: self.clear_fields(self.patient_add_window_fields))
        self.patient_add_window_fields["save_button"].clicked.connect(lambda: self.save_patient(self.patient_add_window_fields))

    @benchmark
    def save_patient(self, patient_add_window_fields):
        #
        mrn = patient_add_window_fields["mrn_input"].text()
        last_name = patient_add_window_fields["last_name_input"].text()
        first_name = patient_add_window_fields["first_name_input"].text()
        middle_name = patient_add_window_fields["middle_name_input"].text()
        dob = patient_add_window_fields["dob_input"].text()
        gender = patient_add_window_fields["gender_input"].currentText()
        print(f'mrn = {mrn}')
        #
        mw.PT_DB.add_patient(mrn, last_name, first_name, middle_name, dob, gender)

#
#
#
#
#
#
#
#
#
#
if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    mw.show()
    app.exec_()




