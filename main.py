# Importing all module
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from frontend import MyWidget


#  ********************************************

# Main Application class

class MyApplication(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        my_window = MyWidget()
        my_window.setWindowTitle("Data Logger")
        my_window.show()
        sys.exit(self.exec_())


def app():
    # Use a breakpoint in the code line below to debug your script.
    MyApplication()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()
