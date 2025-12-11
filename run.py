import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from PyQt5 import QtWidgets

try:
    from ui_main import LoginWindow
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Создаю необходимые файлы...")

    help_dialogs_code = '''
from PyQt5 import QtWidgets, QtCore, QtGui

class HelpDialogs:
    @staticmethod
    def show_amd_vs_intel(parent):
        dialog = QtWidgets.QMessageBox(parent)
        dialog.setWindowTitle("AMD vs Intel")
        dialog.setText("Временно недоступно")
        dialog.exec_()

    @staticmethod
    def show_power_supply_info(parent, processor, videocard, psu_info):
        dialog = QtWidgets.QMessageBox(parent)
        dialog.setWindowTitle("Информация о БП")
        dialog.setText("Временно недоступно")
        dialog.exec_()
'''

    with open('help_dialogs.py', 'w', encoding='utf-8') as f:
        f.write(help_dialogs_code)

    from ui_main import LoginWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())