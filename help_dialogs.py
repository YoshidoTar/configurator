
from PyQt5 import QtWidgets, QtCore, QtGui
class HelpDialogs:
    @staticmethod
    def show_amd_vs_intel(parent):
        dialog = QtWidgets.QDialog(parent)
        dialog.setWindowTitle("AMD vs Intel: Что выбрать?")
        dialog.setGeometry(100, 100, 900, 700)

        layout = QtWidgets.QVBoxLayout(dialog)

        title = QtWidgets.QLabel("📊 Сравнение AMD и Intel")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #0ea5e9;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        text = QtWidgets.QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 15px;
                border: 2px solid #475569;
            }
        """)

        comparison_text = """
        <h3 style="color: #38bdf8;">💡 Когда выбирать AMD:</h3>

        <b>✓ Для игровых ПК (бюджет до среднего):</b>
        • AMD Ryzen 5 5600 - лучший выбор за свои деньги
        • Лучшая многопоточная производительность
        • Хорошая энергоэффективность

        <b>✓ Для профессиональной работы:</b>
        • AMD Ryzen 7/9 серии - больше ядер за меньшие деньги
        • Идеально для рендеринга, компиляции кода, виртуализации
        • Поддержка многопоточных приложений

        <b>✓ Если важна долгосрочная поддержка платформы:</b>
        • Сокет AM4 поддерживался 5 лет
        • AM5 обещает долгую поддержку

        <h3 style="color: #f59e0b;">💡 Когда выбирать Intel:</h3>

        <b>✓ Для игр (высокий бюджет):</b>
        • Intel Core i5/i7 13-го поколения - лидеры в играх
        • Лучшая однопоточная производительность
        • Выше FPS в большинстве игр

        <b>✓ Для офисных задач и легкого использования:</b>
        • Intel Core i3 - надежные и стабильные
        • Лучшая совместимость с ПО

        <b>✓ Если нужна максимальная производительность в играх:</b>
        • Intel Core i9 - абсолютный чемпион
        • Поддержка DDR5 с высокими частотами

        <h3 style="color: #10b981;">🎯 Рекомендации по бюджетам:</h3>

        <b>💰 800$ и меньше:</b> <span style="color: #38bdf8;">AMD Ryzen 5 5600</span>
        • Лучшее соотношение цена/качество
        • Энергоэффективность

        <b>💰 1200$:</b> <span style="color: #38bdf8;">AMD Ryzen 7 5800X</span> или <span style="color: #f59e0b;">Intel Core i5-13600</span>
        • Для игр: Intel
        • Для работы: AMD

        <b>💰 2000$ и больше:</b> <span style="color: #f59e0b;">Intel Core i7-13700K</span>
        • Максимальная игровая производительность
        • Лучшая для стриминга

        <h3 style="color: #ef4444;">⚠️ Важные моменты:</h3>
        • AMD часто предлагает лучшую цену за ядро
        • Intel лучше в однопоточных задачах (большинство игр)
        • Сравнивайте конкретные модели, а не только бренды
        • Учитывайте стоимость материнских плат и охлаждения
        """

        text.setHtml(comparison_text)
        layout.addWidget(text)

        close_btn = QtWidgets.QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0ea5e9, stop:1 #0284c7);
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
                min-height: 50px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #38bdf8, stop:1 #0ea5e9);
            }
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn, alignment=QtCore.Qt.AlignCenter)

        dialog.exec_()

    @staticmethod
    def show_power_supply_info(parent, processor, videocard, psu_info):
        dialog = QtWidgets.QDialog(parent)
        dialog.setWindowTitle("Информация о блоке питания")
        dialog.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout(dialog)

        title = QtWidgets.QLabel("⚡ Расчет мощности блока питания")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #f59e0b;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        text = QtWidgets.QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet("""
            QTextEdit {
                background-color: #1e293b;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 15px;
                border: 2px solid #475569;
            }
        """)

        info_text = f"""
        <h3 style="color: #38bdf8;">📊 Потребление вашей сборки:</h3>

        <b>Процессор ({processor}):</b> {psu_info['processor_tpd']}W<br>
        <b>Видеокарта ({videocard}):</b> {psu_info['videocard_tpd']}W<br>
        <b>Остальные компоненты:</b> ~100W<br>
        <br>
        <b>📈 Общее потребление:</b> {psu_info['total_consumption']}W

        <h3 style="color: #10b981;">🎯 Рекомендации:</h3>

        <b>Минимальный БП:</b> {psu_info['min_required']}W<br>
        <b>Рекомендуемый БП:</b> {psu_info['recommended']}W<br>
        <b>С запасом 20%:</b> {psu_info['recommended']}W<br>

        <h3 style="color: #f59e0b;">✅ Подходящие блоки питания:</h3>
        """

        for wattage in psu_info['suitable_options']:
            if wattage == 500:
                info_text += f"<b>• {wattage}W</b> (80+ Bronze) - минимальный вариант<br>"
            elif wattage == 650:
                info_text += f"<b>• {wattage}W</b> (80+ Bronze) - хороший выбор<br>"
            elif wattage == 750:
                info_text += f"<b>✨ {wattage}W</b> (80+ Gold) - рекомендуемый вариант<br>"
            elif wattage >= 850:
                info_text += f"<b>🔥 {wattage}W</b> (80+ Gold/Platinum) - с запасом для апгрейда<br>"

        info_text += """
        <h3 style="color: #ef4444;">⚠️ Важно знать:</h3>
        • Всегда берите БП с запасом 20-30%
        • Качество БП важнее мощности
        • Ищите сертификацию 80+ Bronze или выше
        • Известные бренды: Seasonic, Corsair, Be Quiet!, EVGA
        • Модульные БП удобнее для сборки
        """

        text.setHtml(info_text)
        layout.addWidget(text)

        close_btn = QtWidgets.QPushButton("Понятно")
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f59e0b, stop:1 #d97706);
                color: white;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
                min-height: 50px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fbbf24, stop:1 #f59e0b);
            }
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn, alignment=QtCore.Qt.AlignCenter)

        dialog.exec_()
