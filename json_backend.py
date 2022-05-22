import json
from datetime import datetime

from PyQt5.QtWidgets import QMessageBox


def message_box(header, fe):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle(header)
    msg.setText(str(fe))
    msg.exec_()


def get_po_part(barcode=None):
    if barcode is None:
        message_box("Error", "Enter the Barcode")
    else:
        var = barcode.split('#')
        part, po = var[0], var[1][4:11]
        return part, po


def load_card_format():
    try:
        with open(r'resource/card_formate.json') as f:
            data = json.load(f)
        return data
    except FileNotFoundError as fe:
        message_box("File Missing", fe)


def load_constant():
    try:
        with open(r'resource/constants.json') as f:
            data = json.load(f)
        return data
    except FileNotFoundError as fe:
        message_box("File Missing", fe)


def load_excel_formate():
    try:
        with open(r'resource/for_excel.json') as f:
            data = json.load(f)
        return data
    except FileNotFoundError as fe:
        message_box("File Missing", fe)


def load_gui_formate():
    try:
        with open(r'resource/for_gui.json') as f:
            data = json.load(f)
        return data
    except FileNotFoundError as fe:
        message_box("File Missing", fe)


def get_card_code():
    data = [x for x in load_card_format()]
    return data


def get_ate_fault(code):
    data = load_card_format()[code]["FAULTS Observed"]
    return data


def get_action_list():
    data = load_constant()["repairing_action"]
    return data


def get_category_list():
    data = load_constant()["fault category"]
    return data


def get_status_list():
    data = load_constant()["status"]
    return data


def get_name(_code):
    name = load_card_format()[_code]["Card Name"]
    return name


def get_address(_code):
    address = load_card_format()[_code]["address"]
    return address


def database_detail(key_name):
    data = load_excel_formate()[key_name]
    return data


def find_date():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

# print(get_address("HE317221-35.20"))
