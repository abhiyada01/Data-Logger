from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView, QTableWidget
from PyQt5.uic import loadUi

from json_backend import get_card_code
from sql_backend import find_table, find_status_group, find_ate_fault_group


class ThirdTab(QWidget):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.status_df = None
        self.ate_df = None

    def load_ui(self):
        loadUi(r'ui_folder\summary.ui', self)
        self.set_part_list(get_card_code())
        self.part_combo.activated.connect(self.set_table_list)
        self.table_combo.activated.connect(self.enable_btn)
        self.ref_btn.clicked.connect(self.create_table)

    def enable_btn(self):
        self.ref_btn.setEnabled(True)
        self.graph_btn.setEnabled(True)
        self.export_btn.setEnabled(True)

    def load_data(self):
        df1 = []
        part = self.part_combo.currentText()
        po_ = self.table_combo.currentText()
        self.status_df = find_status_group(part, po_)
        for row in self.status_df:
            if row[0] == '':
                pass
            else:
                df1.append(row)
        n_row, n_column = len(df1), len(df1[0])
        self.data_table.setColumnCount(n_column)
        self.data_table.setRowCount(n_row)
        self.data_table.setHorizontalHeaderLabels(["Status", "Total"])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_index = 0
        for rows in df1:
            for j in range(n_column):
                self.data_table.setItem(table_index, j, QTableWidgetItem(str(rows[j])))
            table_index += 1

    def create_table(self):
        self.load_data()
        try:
            self.load_ate_data()
        except Exception as e:
            print(e)

    def load_ate_data(self):
        part = self.part_combo.currentText()
        po_ = self.table_combo.currentText()
        df1 = []
        self.status_df = find_ate_fault_group(part, po_)
        for row in self.status_df:
            if row[0] == '':
                pass
            else:
                df1.append(row)
        if len(df1) > 0:
            n_row, n_column = len(df1), len(df1[0])
            self.fault_table.setColumnCount(n_column)
            self.fault_table.setRowCount(n_row)
            self.fault_table.setHorizontalHeaderLabels(["Category", "Total"])
            self.fault_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table_index = 0

            for rows in df1:
                for j in range(n_column):
                    self.fault_table.setItem(table_index, j, QTableWidgetItem(str(rows[j])))
                table_index += 1

    def set_part_list(self, code=None):
        if code is None:
            code = ['code 1', 'code 2']
            self.part_combo.addItems(code)
        else:
            self.part_combo.addItems(code)

    def set_table_list(self):
        self.table_combo.clear()
        try:
            l1 = find_table(self.part_combo.currentText())
            if l1 is not None:
                self.table_combo.addItems(l1)
                self.table_combo.setEnabled(True)
            else:
                l1 = []
                self.table_combo.addItem("No PO Available")
        except Exception as e:
            print(e)
