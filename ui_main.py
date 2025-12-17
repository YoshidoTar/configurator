from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import subprocess  # >>> ДОБАВЛЕНО <<<

from ui_base import BaseWindow
from database import Database
from logic import ConfigLogic
from help_dialogs import HelpDialogs
from admin import AdminPanel
from dialog import ConfigurationDialog


class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__("Конфигуратор ПК РАНХиГС")
        self.db = Database()
        self.current_user_id = None
        self.current_user_role = None
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_center()

        self.add_title("🎮 Конфигуратор ПК РАНХиГС")
        self.add_subtitle("Соберите свой идеальный компьютер")

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setPlaceholderText("Введите имя пользователя")
        self.center_layout.addWidget(self.username_input, alignment=QtCore.Qt.AlignCenter)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.center_layout.addWidget(self.password_input, alignment=QtCore.Qt.AlignCenter)

        self.add_button("🔐 Войти", self.login)
        self.add_button("📝 Зарегистрироваться", self.register)

        self.back_button.hide()
        self.help_button.clicked.connect(self.show_help)

    def show_help(self):
        HelpDialogs.show_amd_vs_intel(self)

    def clear_center(self):
        for i in reversed(range(self.center_layout.count())):
            widget = self.center_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        user = self.db.authenticate_user(username, password)
        if user is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверные учетные данные!")
            return

        self.current_user_id = user[0]
        self.current_user_role = user[3]

        QtWidgets.QMessageBox.information(self, "Успех", f"Добро пожаловать, {username}!")
        self.show_main_menu()

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        if self.db.register_user(username, password):
            QtWidgets.QMessageBox.information(self, "Успех", "Регистрация успешна!")
            self.username_input.clear()
            self.password_input.clear()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Имя пользователя уже существует!")

    def show_main_menu(self):
        self.clear_center()

        self.add_title("🏠 Главное меню")
        self.add_subtitle(f"Выберите действие, пользователь #{self.current_user_id}")

        if self.current_user_role == 'admin':
            self.add_button("👑 Панель администратора", self.show_admin_panel)

        self.add_button("💻 Готовая сборка", lambda: self.show_build_type_selection(False))
        self.add_button("🔧 Сборка по комплектующим", lambda: self.show_build_type_selection(True))
        self.add_button("📂 Мои сохраненные сборки", self.show_saved_configs)

        # >>> ДОБАВЛЕНО <<<
        self.add_button("🏀 Сыграть в игру", self.start_game)

        self.add_button("🚪 Выйти", self.logout)

        self.back_button.show()
        self.back_button.clicked.connect(self.logout)

    def start_game(self):  # >>> ДОБАВЛЕНО <<<
        try:
            subprocess.Popen([sys.executable, "game.py"])
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось запустить игру:\n{e}"
            )

    def show_admin_panel(self):
        self.admin_window = AdminPanel(self.db)
        self.admin_window.show()

    def show_build_type_selection(self, custom_build):
        self.clear_center()

        self.add_title("💰 Выберите бюджет сборки")
        self.add_subtitle("От бюджета зависит доступный выбор комплектующих")

        self.add_button("800$ - Бюджетная сборка", lambda: self.start_build(800, custom_build))
        self.add_button("1200$ - Средняя сборка", lambda: self.start_build(1200, custom_build))
        self.add_button("2000$ - Игровая сборка", lambda: self.start_build(2000, custom_build))
        self.add_button("⬅️ Назад", self.show_main_menu, is_secondary=True)

        self.back_button.clicked.connect(self.show_main_menu)

    def start_build(self, budget, custom_build):
        if custom_build:
            self.show_processor_selection(budget)
        else:
            self.show_ready_builds(budget)

    def show_processor_selection(self, budget):
        self.clear_center()

        self.add_title("⚙️ Выберите процессор")
        self.add_subtitle(f"Бюджет: ${budget}")

        processors = ConfigLogic.get_processors_by_budget(budget)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 10px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #0ea5e9;
                border-radius: 5px;
            }
        """)

        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        for processor in processors:
            info = ConfigLogic.get_processor_info(processor)
            brand_color = "#38bdf8" if info.get("brand") == "AMD" else "#f59e0b"
            brand_text = "AMD" if info.get("brand") == "AMD" else "Intel"

            card = QtWidgets.QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: rgba(30, 41, 59, 0.8);
                    border: 2px solid {brand_color};
                    border-radius: 10px;
                }}
                QFrame:hover {{
                    background-color: rgba({'56, 189, 248' if info.get("brand") == "AMD" else '245, 158, 11'}, 0.15);
                    border-width: 3px;
                }}
            """)

            card_layout = QtWidgets.QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card_layout.setSpacing(8)

            top_layout = QtWidgets.QHBoxLayout()

            brand_label = QtWidgets.QLabel(brand_text)
            brand_label.setStyleSheet(f"""
                QLabel {{
                    color: {brand_color};
                    font-weight: bold;
                    font-size: 12px;
                    padding: 4px 10px;
                    border: 1px solid {brand_color};
                    border-radius: 5px;
                    background-color: rgba({'56, 189, 248' if info.get("brand") == "AMD" else '245, 158, 11'}, 0.2);
                }}
            """)
            top_layout.addWidget(brand_label)

            name_label = QtWidgets.QLabel(processor)
            name_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
            top_layout.addWidget(name_label)
            top_layout.addStretch()

            card_layout.addLayout(top_layout)

            specs_label = QtWidgets.QLabel(f"Сокет: {info.get('socket', 'N/A')} | TDP: {info.get('tpd', 'N/A')}W")
            specs_label.setStyleSheet("color: #cbd5e1; font-size: 13px;")
            card_layout.addWidget(specs_label)

            desc_label = QtWidgets.QLabel(info.get('description', ''))
            desc_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
            desc_label.setWordWrap(True)
            card_layout.addWidget(desc_label)

            select_btn = QtWidgets.QPushButton("✅ Выбрать")
            select_btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {brand_color}, stop:1 {brand_color}aa);
                    color: white;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 14px;
                    border: none;
                    margin-top: 5px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {brand_color}99, stop:1 {brand_color}88);
                }}
            """)
            select_btn.clicked.connect(lambda checked, p=processor: self.show_motherboard_selection(budget, p))
            card_layout.addWidget(select_btn)

            scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        self.center_layout.addWidget(scroll)

        self.add_button("⬅️ Назад", lambda: self.show_build_type_selection(True), is_secondary=True)
        self.back_button.clicked.connect(lambda: self.show_build_type_selection(True))

    def show_motherboard_selection(self, budget, processor):
        self.clear_center()

        self.add_title("🖥️ Выберите материнскую плату")
        self.add_subtitle(f"Процессор: {processor}")

        info = ConfigLogic.get_processor_info(processor)
        motherboards = info.get("motherboards", [])

        if not motherboards:
            error_label = QtWidgets.QLabel("❌ Нет доступных материнских плат для выбранного процессора")
            error_label.setStyleSheet("color: #ef4444; font-size: 16px; font-weight: bold;")
            self.center_layout.addWidget(error_label, alignment=QtCore.Qt.AlignCenter)

            self.add_button("⬅️ Назад", lambda: self.show_processor_selection(budget), is_secondary=True)
            self.back_button.clicked.connect(lambda: self.show_processor_selection(budget))
            return

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
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        for mb in motherboards:
            if isinstance(mb, tuple):
                mb_name = mb[0]
            else:
                mb_name = mb

            card = QtWidgets.QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: rgba(30, 41, 59, 0.8);
                    border: 2px solid #8b5cf6;
                    border-radius: 10px;
                }
                QFrame:hover {
                    background-color: rgba(139, 92, 246, 0.15);
                    border-width: 3px;
                }
            """)

            card_layout = QtWidgets.QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card_layout.setSpacing(8)

            name_label = QtWidgets.QLabel(mb_name)
            name_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
            card_layout.addWidget(name_label)

            if isinstance(mb, tuple) and len(mb) > 1:
                memory = mb[1] if len(mb) > 1 else "16GB DDR4"
                specs_text = f"Совместимая память: {memory}"
            else:
                specs_text = "Совместимость: проверена с выбранным процессором"

            specs_label = QtWidgets.QLabel(specs_text)
            specs_label.setStyleSheet("color: #cbd5e1; font-size: 13px;")
            card_layout.addWidget(specs_label)

            select_btn = QtWidgets.QPushButton("✅ Выбрать")
            select_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8b5cf6, stop:1 #7c3aed);
                    color: white;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 14px;
                    border: none;
                    margin-top: 5px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a78bfa, stop:1 #8b5cf6);
                }
            """)
            select_btn.clicked.connect(lambda checked, m=mb_name: self.show_videocard_selection(budget, processor, m))
            card_layout.addWidget(select_btn)

            scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        self.center_layout.addWidget(scroll)

        self.add_button("⬅️ Назад", lambda: self.show_processor_selection(budget), is_secondary=True)
        self.back_button.clicked.connect(lambda: self.show_processor_selection(budget))

    def show_videocard_selection(self, budget, processor, motherboard):
        self.clear_center()

        self.add_title("🎮 Выберите видеокарту")
        self.add_subtitle(f"Процессор: {processor}")

        videocards = ConfigLogic.get_videocards_by_budget(budget)

        if not videocards:
            error_label = QtWidgets.QLabel("❌ Нет доступных видеокарт для выбранного бюджета")
            error_label.setStyleSheet("color: #ef4444; font-size: 16px; font-weight: bold;")
            self.center_layout.addWidget(error_label, alignment=QtCore.Qt.AlignCenter)

            self.add_button("⬅️ Назад", lambda: self.show_motherboard_selection(budget, processor), is_secondary=True)
            self.back_button.clicked.connect(lambda: self.show_motherboard_selection(budget, processor))
            return

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
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        for vc in videocards:
            info = ConfigLogic.get_videocard_info(vc)

            card = QtWidgets.QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: rgba(30, 41, 59, 0.8);
                    border: 2px solid #10b981;
                    border-radius: 10px;
                }
                QFrame:hover {
                    background-color: rgba(16, 185, 129, 0.15);
                    border-width: 3px;
                }
            """)

            card_layout = QtWidgets.QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card_layout.setSpacing(8)

            name_label = QtWidgets.QLabel(vc)
            name_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
            card_layout.addWidget(name_label)

            if info:
                specs_text = f"Потребление: {info.get('tpd', 'N/A')}W | Мин. БП: {info.get('min_psu', 'N/A')}W"
            else:
                specs_text = "Характеристики: информация отсутствует"

            specs_label = QtWidgets.QLabel(specs_text)
            specs_label.setStyleSheet("color: #cbd5e1; font-size: 13px;")
            card_layout.addWidget(specs_label)

            select_btn = QtWidgets.QPushButton("✅ Выбрать")
            select_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10b981, stop:1 #059669);
                    color: white;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 14px;
                    border: none;
                    margin-top: 5px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34d399, stop:1 #10b981);
                }
            """)
            select_btn.clicked.connect(
                lambda checked, v=vc: self.show_memory_selection(budget, processor, motherboard, v))
            card_layout.addWidget(select_btn)

            scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        self.center_layout.addWidget(scroll)

        self.add_button("⬅️ Назад", lambda: self.show_motherboard_selection(budget, processor), is_secondary=True)
        self.back_button.clicked.connect(lambda: self.show_motherboard_selection(budget, processor))

    def show_memory_selection(self, budget, processor, motherboard, videocard):
        self.clear_center()

        self.add_title("💾 Выберите оперативную память")
        self.add_subtitle(f"Видеокарта: {videocard}")

        memory_options = ConfigLogic.MEMORY_OPTIONS

        ddr4_options = [m for m in memory_options if m["type"] == "DDR4"]
        ddr5_options = [m for m in memory_options if m["type"] == "DDR5"]

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
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        if ddr4_options:
            ddr4_label = QtWidgets.QLabel("DDR4 память:")
            ddr4_label.setStyleSheet("color: #8b5cf6; font-size: 18px; font-weight: bold; margin-top: 10px;")
            scroll_layout.addWidget(ddr4_label)

            for mem in ddr4_options:
                card = QtWidgets.QFrame()
                card.setStyleSheet("""
                    QFrame {
                        background-color: rgba(30, 41, 59, 0.8);
                        border: 2px solid #8b5cf6;
                        border-radius: 10px;
                    }
                    QFrame:hover {
                        background-color: rgba(139, 92, 246, 0.15);
                        border-width: 3px;
                    }
                """)

                card_layout = QtWidgets.QVBoxLayout(card)
                card_layout.setContentsMargins(15, 15, 15, 15)
                card_layout.setSpacing(8)

                name_label = QtWidgets.QLabel(mem["name"])
                name_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
                card_layout.addWidget(name_label)

                speed_label = QtWidgets.QLabel(f"Скорость: {mem['speed']}")
                speed_label.setStyleSheet("color: #cbd5e1; font-size: 13px;")
                card_layout.addWidget(speed_label)

                select_btn = QtWidgets.QPushButton("✅ Выбрать")
                select_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8b5cf6, stop:1 #7c3aed);
                        color: white;
                        border-radius: 8px;
                        padding: 10px;
                        font-weight: bold;
                        font-size: 14px;
                        border: none;
                        margin-top: 5px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a78bfa, stop:1 #8b5cf6);
                    }
                """)
                select_btn.clicked.connect(lambda checked, m=mem["name"]:
                                           self.show_power_supply_selection(budget, processor, motherboard, videocard,
                                                                            m))
                card_layout.addWidget(select_btn)

                scroll_layout.addWidget(card)

        if ddr5_options:
            ddr5_label = QtWidgets.QLabel("DDR5 память:")
            ddr5_label.setStyleSheet("color: #0ea5e9; font-size: 18px; font-weight: bold; margin-top: 20px;")
            scroll_layout.addWidget(ddr5_label)

            for mem in ddr5_options:
                card = QtWidgets.QFrame()
                card.setStyleSheet("""
                    QFrame {
                        background-color: rgba(30, 41, 59, 0.8);
                        border: 2px solid #0ea5e9;
                        border-radius: 10px;
                    }
                    QFrame:hover {
                        background-color: rgba(14, 165, 233, 0.15);
                        border-width: 3px;
                    }
                """)

                card_layout = QtWidgets.QVBoxLayout(card)
                card_layout.setContentsMargins(15, 15, 15, 15)
                card_layout.setSpacing(8)

                name_label = QtWidgets.QLabel(mem["name"])
                name_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
                card_layout.addWidget(name_label)

                speed_label = QtWidgets.QLabel(f"Скорость: {mem['speed']}")
                speed_label.setStyleSheet("color: #cbd5e1; font-size: 13px;")
                card_layout.addWidget(speed_label)

                select_btn = QtWidgets.QPushButton("✅ Выбрать")
                select_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0ea5e9, stop:1 #0284c7);
                        color: white;
                        border-radius: 8px;
                        padding: 10px;
                        font-weight: bold;
                        font-size: 14px;
                        border: none;
                        margin-top: 5px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #38bdf8, stop:1 #0ea5e9);
                    }
                """)
                select_btn.clicked.connect(lambda checked, m=mem["name"]:
                                           self.show_power_supply_selection(budget, processor, motherboard, videocard,
                                                                            m))
                card_layout.addWidget(select_btn)

                scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        self.center_layout.addWidget(scroll)

        self.add_button("⬅️ Назад", lambda: self.show_videocard_selection(budget, processor, motherboard),
                        is_secondary=True)
        self.back_button.clicked.connect(lambda: self.show_videocard_selection(budget, processor, motherboard))

    def show_power_supply_selection(self, budget, processor, motherboard, videocard, memory):
        self.clear_center()

        self.add_title("⚡ Выберите блок питания")
        self.add_subtitle("Рекомендации основаны на ваших комплектующих")

        psu_info = ConfigLogic.calculate_required_psu(processor, videocard)

        info_frame = QtWidgets.QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 41, 59, 0.8);
                border: 2px solid #475569;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        info_layout = QtWidgets.QVBoxLayout(info_frame)

        info_title = QtWidgets.QLabel("📊 Расчет мощности:")
        info_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 16px;")
        info_layout.addWidget(info_title)

        details_text = f"""
        • Процессор: {psu_info.get('processor_tpd', 'N/A')}W
        • Видеокарта: {psu_info.get('videocard_tpd', 'N/A')}W
        • Остальные компоненты: ~100W
        • Общее потребление: {psu_info.get('total_consumption', 'N/A')}W
        • Минимальный БП: {psu_info.get('min_required', 'N/A')}W
        • Рекомендуемый БП: {psu_info.get('recommended', 'N/A')}W
        """

        details_label = QtWidgets.QLabel(details_text)
        details_label.setStyleSheet("color: #cbd5e1; font-size: 14px;")
        info_layout.addWidget(details_label)

        info_btn = QtWidgets.QPushButton("📊 Подробнее о расчете БП")
        info_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8b5cf6, stop:1 #7c3aed);
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border: none;
                margin-top: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a78bfa, stop:1 #8b5cf6);
            }
        """)
        info_btn.clicked.connect(lambda: HelpDialogs.show_power_supply_info(self, processor, videocard, psu_info))
        info_layout.addWidget(info_btn)

        self.center_layout.addWidget(info_frame)

        title_label = QtWidgets.QLabel("✅ Подходящие блоки питания:")
        title_label.setStyleSheet("color: #10b981; font-size: 18px; font-weight: bold; margin-top: 20px;")
        self.center_layout.addWidget(title_label)

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
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(10, 10, 10, 10)

        suitable_options = psu_info.get('suitable_options', [])
        if not suitable_options:
            suitable_options = [500, 650, 750, 850, 1000]  # Значения по умолчанию

        for wattage in suitable_options:
            if wattage == 500:
                card_title = f"{wattage}W (80+ Bronze)"
                card_subtitle = "Минимальный вариант"
                card_color = "#ef4444"
                button_color = "#ef4444"
            elif wattage == 650:
                card_title = f"{wattage}W (80+ Bronze)"
                card_subtitle = "Хороший выбор"
                card_color = "#f59e0b"
                button_color = "#f59e0b"
            elif wattage == 750:
                card_title = f"{wattage}W (80+ Gold)"
                card_subtitle = "Рекомендуемый вариант"
                card_color = "#10b981"
                button_color = "#10b981"
            else:
                card_title = f"{wattage}W (80+ Gold/Platinum)"
                card_subtitle = "С запасом для апгрейда"
                card_color = "#0ea5e9"
                button_color = "#0ea5e9"

            card = QtWidgets.QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: rgba(30, 41, 59, 0.8);
                    border: 2px solid {card_color};
                    border-radius: 10px;
                }}
                QFrame:hover {{
                    background-color: rgba({'239, 68, 68' if wattage == 500 else '245, 158, 11' if wattage == 650 else '16, 185, 129' if wattage == 750 else '14, 165, 233'}, 0.15);
                    border-width: 3px;
                }}
            """)

            card_layout = QtWidgets.QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card_layout.setSpacing(8)

            title_label = QtWidgets.QLabel(card_title)
            title_label.setStyleSheet(f"color: {card_color}; font-weight: bold; font-size: 16px;")
            card_layout.addWidget(title_label)

            subtitle_label = QtWidgets.QLabel(card_subtitle)
            subtitle_label.setStyleSheet("color: #cbd5e1; font-size: 13px;")
            card_layout.addWidget(subtitle_label)

            select_btn = QtWidgets.QPushButton("✅ Выбрать")
            select_btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {button_color}, stop:1 {button_color}aa);
                    color: white;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 14px;
                    border: none;
                    margin-top: 5px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {button_color}99, stop:1 {button_color}88);
                }}
            """)
            select_btn.clicked.connect(lambda checked, w=wattage:
                                       self.save_custom_build(processor, motherboard, videocard, memory, w))
            card_layout.addWidget(select_btn)

            scroll_layout.addWidget(card)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        self.center_layout.addWidget(scroll)

        self.add_button("⬅️ Назад", lambda: self.show_memory_selection(budget, processor, motherboard, videocard),
                        is_secondary=True)
        self.back_button.clicked.connect(lambda: self.show_memory_selection(budget, processor, motherboard, videocard))

    def save_custom_build(self, processor, motherboard, videocard, memory, power_supply):
        configuration = {
            "processor": processor,
            "motherboard": motherboard,
            "videocard": videocard,
            "memory": memory,
            "power_supply": f"{power_supply}W",
            "type": "custom_build"
        }

        if self.db.save_configuration(self.current_user_id, str(configuration)):

            self.show_final_build(configuration)
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось сохранить сборку")

    def show_final_build(self, configuration):
        self.clear_center()

        self.add_title("✅ Сборка сохранена!")
        self.add_subtitle("Ваша конфигурация:")

        details_frame = QtWidgets.QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 41, 59, 0.8);
                border: 3px solid #10b981;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        details_layout = QtWidgets.QVBoxLayout(details_frame)

        title = QtWidgets.QLabel("🎮 Ваша сборка:")
        title.setStyleSheet("color: #10b981; font-weight: bold; font-size: 20px;")
        details_layout.addWidget(title)

        details_text = f"""
        ⚙️ Процессор: {configuration.get('processor', 'N/A')}
        🖥️ Материнская плата: {configuration.get('motherboard', 'N/A')}
        🎮 Видеокарта: {configuration.get('videocard', 'N/A')}
        💾 Оперативная память: {configuration.get('memory', 'N/A')}
        ⚡ Блок питания: {configuration.get('power_supply', 'N/A')}
        """

        details_label = QtWidgets.QLabel(details_text)
        details_label.setStyleSheet("color: white; font-size: 16px; line-height: 1.5;")
        details_layout.addWidget(details_label)

        self.center_layout.addWidget(details_frame)

        self.add_button("💾 Сохранить еще одну копию",
                        lambda: self.db.save_configuration(self.current_user_id, str(configuration)))
        self.add_button("🏠 В главное меню", self.show_main_menu)

        self.back_button.clicked.connect(self.show_main_menu)

    def show_ready_builds(self, budget):
        self.clear_center()

        self.add_title("📦 Готовые сборки")
        self.add_subtitle(f"Бюджет: ${budget}")

        configurations = ConfigLogic.get_configurations(budget)

        if not configurations:
            self.add_subtitle("Нет доступных сборок для этого бюджета")
            self.add_button("⬅️ Назад", lambda: self.show_build_type_selection(False), is_secondary=True)
            self.back_button.clicked.connect(lambda: self.show_build_type_selection(False))
            return

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(255, 255, 255, 0.1);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #0ea5e9;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #38bdf8;
            }
        """)

        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)

        for config in configurations:
            frame = QtWidgets.QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(30, 41, 59, 0.8);
                    border-radius: 15px;
                    border: 2px solid #475569;
                }
            """)

            frame_layout = QtWidgets.QVBoxLayout(frame)

            title = QtWidgets.QLabel(f"💻 {config['processor']} + {config['videocard']}")
            title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
            frame_layout.addWidget(title)

            specs = QtWidgets.QLabel(f"""
            🖥️ Материнская плата: {config['motherboard']}
            💾 Память: {config['memory']}
            ⚡ Блок питания: {config['power_supply']}
            💰 Цена: {config['price']}$

            ✅ Плюсы: {config['pros']}
            ⚠️ Минусы: {config['cons']}
            """)
            specs.setStyleSheet("color: #cbd5e1; font-size: 14px; line-height: 1.4;")
            frame_layout.addWidget(specs)

            # Кнопка выбора
            select_btn = QtWidgets.QPushButton("✅ Выбрать эту сборку")
            select_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #10b981, stop:1 #059669);
                    color: white;
                    border-radius: 10px;
                    padding: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34d399, stop:1 #10b981);
                }
            """)
            select_btn.clicked.connect(lambda checked, c=config: self.save_ready_build(c))
            frame_layout.addWidget(select_btn)

            scroll_layout.addWidget(frame)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        self.center_layout.addWidget(scroll)

        self.add_button("⬅️ Назад", lambda: self.show_build_type_selection(False), is_secondary=True)
        self.back_button.clicked.connect(lambda: self.show_build_type_selection(False))

    def save_ready_build(self, config):
        configuration = {
            "processor": config['processor'],
            "videocard": config['videocard'],
            "memory": config['memory'],
            "motherboard": config['motherboard'],
            "power_supply": config['power_supply'],
            "price": config['price'],
            "type": "ready_build"
        }

        if self.db.save_configuration(self.current_user_id, str(configuration)):
            QtWidgets.QMessageBox.information(self, "Успех", "Сборка сохранена!")
            self.show_main_menu()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось сохранить сборку")

    def show_saved_configs(self):
        self.clear_center()

        self.add_title("📂 Мои сохраненные сборки")

        configurations = self.db.view_saved_configurations(self.current_user_id)

        if not configurations:
            self.add_subtitle("У вас пока нет сохраненных сборок")
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
                try:
                    import ast
                    config_dict = ast.literal_eval(config[0])

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

                    title = QtWidgets.QLabel(f"💾 Сборка #{configurations.index(config) + 1}")
                    title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0ea5e9;")
                    frame_layout.addWidget(title)

                    details = ""
                    if 'processor' in config_dict:
                        details += f"⚙️ Процессор: {config_dict['processor']}\n"
                    if 'videocard' in config_dict:
                        details += f"🎮 Видеокарта: {config_dict['videocard']}\n"
                    if 'memory' in config_dict:
                        details += f"💾 Память: {config_dict['memory']}\n"
                    if 'power_supply' in config_dict:
                        details += f"⚡ БП: {config_dict['power_supply']}\n"

                    details_label = QtWidgets.QLabel(details)
                    details_label.setStyleSheet("color: #cbd5e1; font-size: 14px;")
                    frame_layout.addWidget(details_label)

                    scroll_layout.addWidget(frame)
                except:
                    continue

            scroll_layout.addStretch()
            scroll.setWidget(scroll_widget)
            self.center_layout.addWidget(scroll)

        self.add_button("⬅️ Назад", self.show_main_menu, is_secondary=True)
        self.back_button.clicked.connect(self.show_main_menu)

    def logout(self):
        self.current_user_id = None
        self.current_user_role = None
        self.show_login_screen()