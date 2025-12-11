import sys
from PyQt5 import QtWidgets
from ui_main import LoginWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle('Fusion')
    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())