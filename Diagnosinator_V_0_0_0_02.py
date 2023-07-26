from my_decorators import benchmark
import sqlite3 as sql
import time
from Patients_Database import Patients_Database
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

# def benchmark(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         execution_time = end_time - start_time
#         print(f"Function {func.__name__} executed in {execution_time:.4f} seconds")
#         return result
#     return wrapper


class MainWindow(qtw.QMainWindow):
    #
    @benchmark
    def __init__(self):
        super().__init__()
        self.PT_DB = Patients_Database()
        self.set_mainwindow_settings()
    #
    @benchmark
    def set_mainwindow_settings(self):
        #
        screen_resolution = qtw.QApplication.desktop().screenGeometry()
        desired_width = screen_resolution.width() * 0.9
        desired_height = screen_resolution.height() * 0.9
        self.setWindowTitle("Diagnosinator")
        self.resize(int(desired_width), int(desired_height))
        self.move(int(desired_width * 0.02), int(desired_height * 0.02))
        #
        self.layout_mw = qtw.QGridLayout(self)
        self.layout_mw.setColumnStretch(0, 1)
        self.layout_mw.setRowStretch(0, 1)
        #
        self.centralwidget_mw = qtw.QWidget()
        self.centralwidget_mw.setLayout(self.layout_mw)
        #
        self.setCentralWidget(self.centralwidget_mw)
        self.setLayout(self.layout_mw)
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
        self.set_mainwindow_toolbar()
    #
    @benchmark
    def set_mainwindow_toolbar(self):
        #
        self.toolbar_mw = self.addToolBar("Toolbar")
        self.toolbar_mw.setMovable(False)
        self.toolbar_mw.setFloatable(False)
        self.toolbar_mw.setToolButtonStyle(1)
        #
        self.toolbar_mw.addAction("Add Patient", self.open_add_patient_window)
        self.toolbar_mw.addAction("Exit", self.close)
        #
        self.set_mainwindow_statusbar()
    #
    @benchmark
    def set_mainwindow_statusbar(self):
        #
        self.statusbar_mw = self.statusBar()
        self.setStatusBar(self.statusbar_mw)
        #
        self.widget_statusbar_layout = qtw.QWidget()
        self.layout_statusbar = qtw.QHBoxLayout()
        self.widget_statusbar_layout.setLayout(self.layout_statusbar)
        self.statusbar_mw.addWidget(self.widget_statusbar_layout)
        #
        self.label_current_datetime = qtw.QLabel()
        #
        self.layout_statusbar.addSpacerItem(qtw.QSpacerItem(10000, 0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum))
        self.layout_statusbar.addWidget(self.label_current_datetime)
        #
        self.layout_statusbar.setAlignment(self.label_current_datetime, qtc.Qt.AlignRight)
        #
        self.set_tablewidget_mw_all_patients()
        self.update_DateTime()
    #
    @benchmark
    def set_tablewidget_mw_all_patients(self):
        #
        self.tablewidget_mw_all_patients = qtw.QTableWidget()
        self.tablewidget_mw_all_patients.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        self.tablewidget_mw_all_patients.setContentsMargins(0, 0, 0, 0)
        self.tablewidget_mw_all_patients.verticalHeader().setVisible(False)
        self.tablewidget_mw_all_patients.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.tablewidget_mw_all_patients.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        self.tablewidget_mw_all_patients.setAlternatingRowColors(True)
        self.layout_mw.addWidget(self.tablewidget_mw_all_patients, 0, 0)
        self.layout_mw.addItem(qtw.QSpacerItem(0,0, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding), 1, 1, 1, 1)
        self.layout_mw.setContentsMargins(25, 25, 25, 25)
        self.load_tablewidget_mw_all_patients(self.PT_DB.load_patients_list())
        

    # # # ^ ^  Widgets  ^ ^ # # #
      # #  #  #  # #  #  #  # # 
    # # # V v Functions v V # # #

    @benchmark
    def load_tablewidget_mw_all_patients(self, patients):
        #
        self.tablewidget_mw_all_patients.clear()
        #
        self.headerlabels_tablewidget_mw_all_patients = ["MRN", "Last Name", "First Name", "Middle Name"]
        self.tablewidget_mw_all_patients.setColumnCount(len(self.headerlabels_tablewidget_mw_all_patients))
        self.tablewidget_mw_all_patients.setHorizontalHeaderLabels(self.headerlabels_tablewidget_mw_all_patients)
        self.tablewidget_mw_all_patients.setRowCount(len(patients))
        #
        for row, patient in enumerate(patients):    
                for col in range(3):
                    if col == None:
                        pass
                    else:
                        self.tablewidget_mw_all_patients.setItem(row, col, qtw.QTableWidgetItem(str(patient[col])))
                
    

        
            
    @benchmark
    def open_add_patient_window(self):
        self.add_patient_window = Add_Patient_Window()
        
        
        self.add_patient_window.show()
    #
    def update_DateTime(self):
        self.label_current_datetime.setText(qtc.QDateTime.currentDateTime().toString("MM-dd-yyyy hh:mm:ss"))
        qtc.QTimer.singleShot(1000, self.update_DateTime)

class Add_Patient_Window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add Patient")
        self.apw_layout = qtw.QGridLayout()
        self.setLayout(self.apw_layout)
        #
        self.fields_apw = [
            (qtw.QLabel("MRN:"), qtw.QLineEdit()),
            (qtw.QLabel("Last Name:"), qtw.QLineEdit()),
            (qtw.QLabel("First Name:"), qtw.QLineEdit()),
            (qtw.QLabel("Middle Name:"), qtw.QLineEdit()),
            (qtw.QLabel("Date of Birth:"), qtw.QLineEdit()),
            (qtw.QLabel("Gender:"), qtw.QComboBox()),
            (qtw.QPushButton("Clear"), qtw.QPushButton("Save"))
        ]
        #
        for widget in self.fields_apw:
            widget[1].setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        #
        self.fields_apw[0][1].setText(str(mw.PT_DB.find_next_available_mrn()))
        self.fields_apw[0][1].adjustSize()
        self.fields_apw[0][1].setReadOnly(True)
        self.fields_apw[0][1].setEnabled(False)

        # Add items to the gender combo box
        self.fields_apw[-2][1].addItems(["", "Male", "Female"])
        #
        for row, (label, input_field) in enumerate(self.fields_apw, start=1):
            self.apw_layout.addWidget(label, row+1, 0)
            self.apw_layout.addWidget(input_field, row+1, 1)
            self.apw_layout.setAlignment(label, qtc.Qt.AlignRight)
        #
        self.fields_apw[-1][0].clicked.connect(lambda: self.clear_fields(self.fields_apw))
        self.fields_apw[-1][1].clicked.connect(lambda: self.save_patient(self.fields_apw))

    @benchmark
    def save_patient(self, fields_apw):
        #
        mrn = fields_apw[0][1].text()
        last_name = fields_apw[1][1].text()
        first_name = fields_apw[2][1].text()
        middle_name = fields_apw[3][1].text()
        dob = fields_apw[4][1].text()
        #
        mw.PT_DB.add_patient(mrn, last_name, first_name, middle_name, dob)

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




