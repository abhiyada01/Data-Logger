# Module
import sys

from PyQt5.QtWidgets import QWidget, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from testing import FirstTab
from repairing import SecondTab
from summary_ import ThirdTab
from json_backend import message_box, load_gui_formate


class MyWidget(QMainWindow):
    def __init__(self):
        # Base Widget Implementation
        super().__init__()
        self.setFixedSize(600, 650)  # setFixedSize (Width, Height)
        self.setWindowTitle("Card Logger")
        self.init_ui()

    def init_ui(self):
        try:
            loadUi(r'ui_folder//main_ui.ui', self)
        except FileNotFoundError as fe:
            print(fe)
        finally:
            self.adding_tab()

    def adding_tab(self):
        try:
            if load_gui_formate()["testing_status"] is True:
                self.tabWidget.addTab(FirstTab(), "Testing")
        except FileNotFoundError as fe:
            message_box(" File handle", fe)
            sys.exit()
        try:
            if load_gui_formate()["repairing_status"] is True:
                self.tabWidget.addTab(SecondTab(), "Repair")
        except FileNotFoundError as fe:
            message_box(" File handle", fe)
            sys.exit()

        try:
            if load_gui_formate()["summary_status"] is True:
                self.tabWidget.addTab(ThirdTab(), "Summary")
        except FileNotFoundError as fe:
            message_box(" File handle", fe)
            sys.exit()

    def binding_function(self):
        pass
