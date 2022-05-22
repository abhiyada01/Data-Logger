from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from sql_backend import search_data, update_data
from json_backend import get_action_list, get_category_list, message_box, get_status_list, find_date


class SecondTab(QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui()

    def load_ui(self):
        loadUi(r'ui_folder\repair.ui', self)
        self.set_combo_list()
        self.binding_function()

    def set_combo_list(self):
        self.set_action_list(get_action_list())
        self.set_category_list(get_category_list())
        self.set_repairing_status_list(get_status_list())

    def binding_function(self):
        self.search_btn.clicked.connect(self.search_data)
        self.submit_btn.clicked.connect(self.submit_data)
        self.clr_btn.clicked.connect(self.clear_entry)

    def set_barcode(self, barcode=None):
        self.serial_entry.setText(barcode)

    def get_barcode(self):
        selected = self.serial_entry.text()
        return selected

    def set_test_date(self, date_=None):
        self.test_date.setText(date_)

    def get_test_date(self):
        selected = self.test_date.text()
        return selected

    def set_code(self, code=None):
        self.test_code.setText(code)

    def get_code(self):
        selected = self.test_code.text()
        return selected

    def set_test_status(self, status=None):
        self.test_status.setText(status)

    def get_test_status(self):
        selected = self.test_status.text()
        return selected

    def set_test_ate_fault(self, fault=None):
        self.test_ate_fault.setText(fault)

    def get_test_ate_fault(self):
        selected = self.test_ate_fault.text()
        return selected

    def set_key_entry(self, barcode=None):
        self.key_entry.setText(barcode)

    def get_key_component(self):
        selected = self.key_entry.text()
        return selected

    def set_repair_date(self):
        self.r_date_entry.setText(find_date())

    def get_repair_date(self):
        selected = self.r_date_entry.text()
        return selected

    def set_eng_entry(self, entry=None):
        self.r_eng_entry.setText(entry)

    def get_eng_entry(self):
        selected = self.r_eng_entry.text()
        return selected

    def set_retest(self, entry=None):
        self.r_test_entry.setText(entry)

    def get_retest(self):
        selected = self.r_test_entry.text()
        return selected

    def set_remark(self, remark=None):
        self.remark_entry.setText(remark)

    def get_remark(self):
        selected = self.remark_entry.text()
        return selected

    def get_category(self):
        selected = self.cat_combo.currentText()
        return selected

    def set_category_list(self, cat_list=None):
        if cat_list is None:
            cat_list = []
        self.cat_combo.addItems(cat_list)

    def get_action(self):
        selected = self.action_combo.currentText()
        return selected

    def set_action_list(self, cat_list=None):
        if cat_list is None:
            cat_list = []
        self.action_combo.addItems(cat_list)

    def set_repairing_status_list(self, cat_list=None):
        if cat_list is None:
            cat_list = []
        self.r_status_combo.addItems(cat_list)

    def get_repairing_status(self):
        selected = self.r_status_combo.currentText()
        return selected

    def submit_data(self):
        try:
            self.set_repair_date()
            self.push_into_database()
            self.serial_entry.clear()

        except Exception as e:
            message_box("Error", str(e))

    def clear_entry(self, boolean):
        self.submit_btn.setEnabled(boolean)
        self.cat_combo.setEnabled(boolean)
        self.action_combo.setEnabled(boolean)
        self.r_status_combo.setEnabled(boolean)
        self.key_entry.setEnabled(boolean)
        self.clr_btn.setEnabled(boolean)

    def search_data(self):
        try:
            barcode = self.get_barcode()
            fetch_data = search_data(barcode)
            self.set_test_date(fetch_data[0])
            self.set_code(fetch_data[2])
            self.set_test_status(fetch_data[5])
            self.set_test_ate_fault(fetch_data[6])
            if self.get_test_status() == "Fail":
                self.clear_entry(True)
        except Exception as e:
            message_box("Error", str(e) + '\n No Entry Found')

    def push_into_database(self):
        try:
            fo = self.get_category()
            kc = self.get_key_component()
            ra = self.get_action()
            re = self.get_eng_entry()
            rt = self.get_retest()
            rd = self.get_repair_date()
            rs = self.get_repairing_status()
            barcode = self.get_barcode()
            update_data(fo, kc, ra, re, rt, rd, rs, barcode)
            self.clear_entry(False)
        except Exception as e:
            message_box("Error", str(e) + '\n No Entry Found')
