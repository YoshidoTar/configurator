import sys
from PyQt5 import QtWidgets
from ui_main import LoginWindow  # Исправлено: было ul_main

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Устанавливаем стиль приложения
    app.setStyle('Fusion')

    # Создаем и показываем главное окно
    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())