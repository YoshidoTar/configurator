from PyQt5 import QtWidgets, QtCore, QtGui


class BaseWindow(QtWidgets.QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)

        # Устанавливаем стили
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:1 #16213e);
                color: #ffffff;
                font-family: "Segoe UI", sans-serif;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0ea5e9, stop:1 #0284c7);
                color: white;
                border-radius: 15px;
                padding: 20px;
                font-size: 18px;
                font-weight: bold;
                border: 3px solid #0369a1;
                min-width: 250px;
                min-height: 60px;
                margin: 10px;
                transition: all 0.3s;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #38bdf8, stop:1 #0ea5e9);
                border: 3px solid #0ea5e9;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(14, 165, 233, 0.4);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0284c7, stop:1 #0369a1);
                transform: translateY(1px);
            }
            QPushButton#secondary {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #64748b, stop:1 #475569);
                border: 3px solid #475569;
            }
            QPushButton#secondary:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #94a3b8, stop:1 #64748b);
                border: 3px solid #64748b;
            }
            QPushButton#help {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f59e0b, stop:1 #d97706);
                border: 3px solid #d97706;
                min-width: 150px;
            }
            QPushButton#help:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fbbf24, stop:1 #f59e0b);
                border: 3px solid #f59e0b;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                border: 2px solid #475569;
                min-width: 300px;
                margin: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #0ea5e9;
                background-color: rgba(255, 255, 255, 0.15);
            }
            QLabel {
                color: white;
                font-size: 18px;
                margin: 10px;
            }
            QLabel#title {
                font-size: 36px;
                font-weight: bold;
                color: #38bdf8;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                margin: 20px;
            }
            QLabel#subtitle {
                font-size: 24px;
                color: #cbd5e1;
                margin: 15px;
            }
            QListWidget {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                border: 2px solid #475569;
                margin: 10px;
            }
            QListWidget::item {
                padding: 15px;
                border-radius: 5px;
                margin: 5px;
                background-color: rgba(255, 255, 255, 0.05);
            }
            QListWidget::item:selected {
                background-color: #0ea5e9;
                color: white;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: rgba(14, 165, 233, 0.3);
            }
            QMessageBox {
                background-color: #1e293b;
                color: white;
                border-radius: 15px;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 16px;
            }
            QMessageBox QPushButton {
                min-width: 100px;
                min-height: 40px;
                font-size: 14px;
            }
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                border: 2px solid #475569;
                min-width: 300px;
                margin: 10px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1e293b;
                color: white;
                selection-background-color: #0ea5e9;
                border: 1px solid #475569;
                border-radius: 5px;
            }
        """)

        # Основной макет
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        # Добавляем верхнюю панель с кнопками
        self.top_panel = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.top_panel)

        # Кнопка "Назад"
        self.back_button = QtWidgets.QPushButton("← Назад", self)
        self.back_button.setObjectName("secondary")
        self.back_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.top_panel.addWidget(self.back_button)

        self.top_panel.addStretch()

        # Кнопка "Помощь"
        self.help_button = QtWidgets.QPushButton("❓ Помощь", self)
        self.help_button.setObjectName("help")
        self.help_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.top_panel.addWidget(self.help_button)

        # Центральная область
        self.center_widget = QtWidgets.QWidget()
        self.center_layout = QtWidgets.QVBoxLayout(self.center_widget)
        self.center_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.center_widget)

        # Нижняя панель
        self.bottom_panel = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.bottom_panel)

        self.bottom_panel.addStretch()

        # Кнопка "Закрыть"
        self.close_button = QtWidgets.QPushButton("Закрыть приложение", self)
        self.close_button.setObjectName("secondary")
        self.close_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_button.clicked.connect(self.close)
        self.bottom_panel.addWidget(self.close_button)

    def showEvent(self, event):
        self.showFullScreen()
        super().showEvent(event)

    def add_title(self, text):
        title_label = QtWidgets.QLabel(text, self)
        title_label.setObjectName("title")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.center_layout.addWidget(title_label)

    def add_subtitle(self, text):
        subtitle_label = QtWidgets.QLabel(text, self)
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.center_layout.addWidget(subtitle_label)

    def add_button(self, text, callback, is_secondary=False):
        button = QtWidgets.QPushButton(text, self)
        if is_secondary:
            button.setObjectName("secondary")
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.clicked.connect(callback)
        self.center_layout.addWidget(button, alignment=QtCore.Qt.AlignCenter)
        return button