
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
