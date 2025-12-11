from PyQt5 import QtWidgets, QtCore, QtGui
from ui_base import BaseWindow


class AdminPanel(BaseWindow):
    def __init__(self, db):
        super().__init__("Панель администратора")
        self.db = db
        self.show_admin_main()

    def show_admin_main(self):
        self.clear_center()

        self.add_title("👑 Панель администратора")
        self.add_subtitle("Управление системой конфигураций")

        self.add_button("📋 Все конфигурации пользователей", self.view_all_configs)
        self.add_button("👥 Управление пользователями", self.manage_users)
        self.add_button("📊 Статистика", self.show_stats)
        self.add_button("⚙️ Настройки системы", self.system_settings)
        self.add_button("🏠 В главное меню", self.close)

        self.back_button.clicked.connect(self.close)

    def view_all_configs(self):
        self.clear_center()

        self.add_title("📋 Все конфигурации")

        configurations = self.db.view_all_configurations_for_edit()

        if not configurations:
            self.add_subtitle("Нет сохраненных конфигураций")
        else:
            scroll = QtWidgets.QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background: transparent;
                }
            """)

            scroll_widget = QtWidgets.QWidget()
            scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

            for config in configurations:
                frame = QtWidgets.QFrame()
                frame.setStyleSheet("""
                    QFrame {
                        background-color: rgba(30, 41, 59, 0.8);
                        border-radius: 15px;
                        border: 2px solid #475569;
                        padding: 15px;
                        margin: 10px;
                    }
                """)

                frame_layout = QtWidgets.QVBoxLayout(frame)

                info = QtWidgets.QLabel(f"""
                <b>ID:</b> {config[0]}<br>
                <b>Пользователь:</b> {config[1]}<br>
                <b>Конфигурация:</b> {config[2][:100]}...
                """)
                info.setTextFormat(QtCore.Qt.RichText)
                frame_layout.addWidget(info)

                scroll_layout.addWidget(frame)

            scroll_layout.addStretch()
            scroll.setWidget(scroll_widget)
            self.center_layout.addWidget(scroll)

        self.add_button("⬅️ Назад", self.show_admin_main, is_secondary=True)
        self.back_button.clicked.connect(self.show_admin_main)

    def manage_users(self):
        self.clear_center()
        self.add_title("👥 Управление пользователями")
        self.add_subtitle("Функция в разработке")
        self.add_button("⬅️ Назад", self.show_admin_main, is_secondary=True)
        self.back_button.clicked.connect(self.show_admin_main)

    def show_stats(self):
        self.clear_center()
        self.add_title("📊 Статистика")
        self.add_subtitle("Функция в разработке")
        self.add_button("⬅️ Назад", self.show_admin_main, is_secondary=True)
        self.back_button.clicked.connect(self.show_admin_main)

    def system_settings(self):
        self.clear_center()
        self.add_title("⚙️ Настройки системы")
        self.add_subtitle("Функция в разработке")
        self.add_button("⬅️ Назад", self.show_admin_main, is_secondary=True)
        self.back_button.clicked.connect(self.show_admin_main)