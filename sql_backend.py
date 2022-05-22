import sqlite3 as sq

from json_backend import database_detail, get_address, get_po_part
from PyQt5.QtWidgets import QMessageBox


def message_box(header, fe):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle(header)
    msg.setText(str(fe))
    msg.exec_()


def reading_address(card):
    read_address = get_address(card)
    return read_address


def key_search(input_string):
    var = database_detail(input_string)
    return var


def find_bar_detail(barcode=None):
    part, po = get_po_part(barcode)
    return part, po


def create_template(barcode_scan):
    d2 = barcode_scan
    var = str(find_bar_detail(d2)[1])
    part = str(find_bar_detail(d2)[0])
    path = reading_address(part)
    try:
        conn = sq.connect(path + part + '.db')
        cursor = conn.cursor()
        create = '''CREATE TABLE IF NOT EXISTS {PO_} (
        {Date_IN} , {Card_Name} ,{Card_Code} ,{Serial_No},{Testing_by},{Status},{ATE},{OF},{KC},{RA},{R_ENG},{RT_ENG},{R_D}, {R_S}, {Remark})''' \
            .format(PO_="'" + var + "'",
                    Date_IN=key_search("date_input"),
                    Card_Name=key_search("card_name"),
                    Card_Code=key_search("card_code"),
                    Serial_No=key_search("serial_no"),
                    Testing_by=key_search("tested_by"),
                    Status=key_search("tested_status"),
                    ATE=key_search("ATE_fault"),
                    OF=key_search("observed_fault"),
                    KC=key_search("Key_Comp"),
                    RA=key_search("Repair_Action"),
                    R_ENG=key_search("R_Eng"),
                    RT_ENG=key_search("RT_Eng"),
                    R_D=key_search("R_Date"),
                    R_S=key_search("R_Status"),
                    Remark=key_search("Remark"), )
        cursor.execute(create)
        conn.commit()

        conn.close()  # Closing the connection
    except Exception as e:
        message_box("Database Error", e)


def insert_sql(date_, card_name, card_code, serial_no, tested_by, status_testing, ate_fault, ob_fault='', key_comp='',
               r_action='', r_eng='', rt_eng='', r_date='', r_status='', remark=''):
    d2 = serial_no
    var = find_bar_detail(d2)[1]
    part = find_bar_detail(d2)[0]
    path = reading_address(part)
    conn = sq.connect(path + part + '.db')
    # print("Connection Established")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO '{PO}' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(PO=var),
                       (date_, card_name, card_code, serial_no, tested_by, status_testing, ate_fault,
                        ob_fault, key_comp, r_action, r_eng, rt_eng, r_date, r_status, remark))
    except FileNotFoundError:
        create_template(serial_no)
    except Exception as e:
        message_box("Entry Error", e)
    conn.commit()
    conn.close()


def view_data(part, po_):
    path = reading_address(part)
    # print(var, part)
    conn = sq.connect(path + part + '.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM  '{PO}'".format(PO=po_))
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_data(serial_number):
    d2 = serial_number
    var = find_bar_detail(d2)[1]
    part = find_bar_detail(d2)[0]
    path = reading_address(part)
    conn = sq.connect(path + part + '.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM  '{PO}' WHERE Serial_Number = '{SR}' ".format(PO=var, SR=serial_number))
    # cursor.execute("SELECT * FROM  '{PO}' WHERE Serial_Number = 'HE314142#D10161011111001'".format(PO=var))
    rows = cursor.fetchone()
    conn.close()
    return rows


def update_data(fault_observe='', key_component='', repair_action='', repair_engineer='', retest='',
                repairing_date='', repair_status='', serial_no=None):
    d2 = serial_no
    var = find_bar_detail(d2)[1]
    part = find_bar_detail(d2)[0]
    path = reading_address(part)
    # print(var, part)
    conn = sq.connect(path + part + '.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE '{PO_}' SET Fault_Observe=?,Key_Component=?,Repair_Action=?,Repair_Engineer=?,Retest=?,"
        "Repairing_Date=?, Repair_Status=? WHERE Serial_Number =?".format(PO_=var),
        (
            fault_observe, key_component, repair_action, repair_engineer,
            retest, repairing_date, repair_status, serial_no))

    conn.commit()
    conn.close()


def find_table(part_num):
    table_list = []
    path = reading_address(part_num)
    conn = sq.connect(path + part_num + '.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = cursor.fetchall()
    conn.close()
    for i in rows:
        for j in i:
            table_list.append(j)
    return table_list


# For Trail

def find_status_group(part, var):
    path = reading_address(part)
    conn = sq.connect(path + part + '.db')
    cur = conn.cursor()
    cur.execute("SELECT Status, COUNT(Status) FROM  '{PO}' GROUP BY Status".format(PO=var))
    rows = cur.fetchall()
    conn.close()
    return rows


def find_ate_fault_group(part, var):
    path = reading_address(part)
    conn = sq.connect(path + part + '.db')
    cur = conn.cursor()
    cur.execute("SELECT Fault_ATE, COUNT(Fault_ATE) FROM  '{PO}' GROUP BY Fault_ATE".format(PO=var))
    rows = cur.fetchall()
    conn.close()
    return rows
