import os
import sqlite3 as sq
from pandas import read_sql
from json_backend import get_address
from pathlib import Path


def find_folder():
    path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
    return path_to_download_folder


# def view_data_pandas(serial_number):
#     part, var = get_po_part(serial_number)
#     path = get_address(part)
#     # print((var), (part))
#     conn = sq.connect(path + part + '.db')
#     cursor = conn.cursor()
#     rows = read_sql("SELECT * FROM '{PO}'".format(PO=var), conn,
#                     parse_dates={"Date_In": {"dayfirst": True}})
#     # cursor.execute("SELECT * FROM  '{PO}'".format(PO=var))
#     # rows = cursor.fetchall()
#     conn.close()
#     return rows
#     # export_to_excel(rows)

def view_data_pandas(part, var):
    path = get_address(part)
    conn = sq.connect(path + part + '.db')
    # cursor = conn.cursor()
    rows = read_sql("SELECT * FROM '{PO}'".format(PO=var), conn,index_col=None,
                    parse_dates={"Date_In": {"dayfirst": True}})

    # Drop first column of dataframe
    rows = rows.drop()
    conn.close()
    export_to_excel(rows)


def export_to_excel(combine_data):
    base_filename = "output"
    filename_suffix = "xlsx"
    complete_path = os.path.join(find_folder(), base_filename + "." + filename_suffix)
    excel_data = combine_data
    excel_data.to_excel(complete_path)

d1, d2 = "HE317161-30.22","1042219"
view_data_pandas(d1,d2)