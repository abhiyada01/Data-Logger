from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from json_backend import get_card_code, get_ate_fault, \
    get_name, get_po_part, message_box, find_date

from sql_backend import create_template, insert_sql


class FirstTab(QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.binding_function()

    def load_ui(self):
        # testing Interface UI is created by Qt developer.
        loadUi(r"ui_folder/testing.ui", self)
        # self.binding_function()

    def binding_function(self):
        # self.code_combo.addItem(None)  # A blank line is added with list of card
        self.set_code_list(get_card_code())
        # self.set_ate_fault_list()
        self.code_combo.activated.connect(self.code_combo_selection)
        self.status_combo.activated.connect(self.status_state)
        self.submit_btn.clicked.connect(self.submit_data)

    def set_date(self):
        self.date_entry.setText(find_date())

    def set_card_name(self):
        part = self.get_code()
        name = get_name(part)
        self.name_entry.setText(name)

    def set_code_list(self, code=None):
        if code is None:
            code = ['code 1', 'code 2']
            self.code_combo.addItems(code)
        else:
            self.code_combo.addItems(code)

    def set_operator_name(self, op_name=None):
        self.oper_label.setText(op_name)

    def set_ate_fault_list(self, fault_list=None):
        if fault_list is None:
            fault_list = ["First Select Status as Fail"]
            self.fault_combo.addItems(fault_list)
        else:
            self.fault_combo.addItems(fault_list)

    def set_remark(self, remark=None):
        self.remark_label_2.setText(remark)

    def get_pcb_name(self):
        selected = self.name_entry.text()
        return selected

    def get_code(self):
        selected = self.code_combo.currentText()
        return selected

    def get_serial_num(self):
        selected = self.serial_entry.text()
        return selected

    def get_status(self):
        selected = self.status_combo.currentText()
        return selected

    def get_operator_name(self):
        selected = self.oper_label.text()
        return selected

    def get_ate_fault_list(self):
        selected = self.fault_combo.text()
        return selected

    @pyqtSlot()
    def code_combo_selection(self):
        self.combo_box_action()

    @pyqtSlot()
    def status_state(self):
        st = self.status_combo.currentText()
        if st == "Fail":
            code = self.get_code()
            self.set_ate_fault_list(get_ate_fault(code))
            self.fault_combo.setEnabled(True)
        else:
            self.fault_combo.clear()
            self.fault_combo.setEnabled(False)

    def submit_data(self):
        try:
            if get_po_part(self.get_serial_num())[0] == self.get_code():
                self.set_date()
                self.push_into_database()
                self.serial_entry.clear()
            else:
                message_box("Error", "Correct the Selection")
                self.serial_entry.clear()
        except Exception as e:
            message_box("Error", str(e))

    def combo_box_action(self):
        selected = len(self.oper_label.text())
        if selected > 3:
            self.serial_entry.setEnabled(True)
            self.set_card_name()
        else:
            self.serial_entry.setEnabled(False)
            message_box("Error", "Enter valid Operator Name")

    def push_into_database(self):
        _date = find_date()
        _card_name = self.name_entry.text()
        _card_code = self.code_combo.currentText()
        _card_serial = self.serial_entry.text()
        _status = self.status_combo.currentText()
        _operator = self.oper_label.text()
        _ate_fault = None
        if _status == "Fail":
            _ate_fault = self.fault_combo.currentText()
        else:
            _ate_fault = ''

        _remark = self.remark_label_2.text()
        create_template(_card_serial)
        try:
            insert_sql(_date, _card_name, _card_code, _card_serial, _operator, _status, _ate_fault, remark=_remark)
        except Exception as e:
            message_box("Entry Error", e)
