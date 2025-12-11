from PyQt5 import QtWidgets, QtCore, QtGui
from database import Database
from logic import ConfigLogic

class ConfigurationDialog:
    @staticmethod
    def show_ready_builds(parent, budget, user_id):
        configurations = ConfigLogic.get_configurations(budget)
        if configurations:
            dialog = QtWidgets.QDialog(parent)
            dialog.setWindowTitle("Выбор готовой сборки")
            dialog.setGeometry(100, 100, 800, 600)
            dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)

            layout = QtWidgets.QVBoxLayout(dialog)

            # Список готовых конфигураций
            config_list = QtWidgets.QListWidget()
            for cfg in configurations:
                config_list.addItem(f"{cfg['processor']} - {cfg['videocard']} - {cfg['memory']} - {cfg['motherboard']} ({cfg['price']}$)\n"
                                   f"Плюсы: {cfg['pros']}\n"
                                   f"Минусы: {cfg['cons']}\n")
            layout.addWidget(config_list)

            # Кнопка для сохранения выбранной конфигурации
            save_button = QtWidgets.QPushButton("Сохранить", dialog)
            save_button.setMinimumWidth(390)  # Увеличиваем ширину кнопки
            save_button.setMinimumHeight(80)  # Увеличиваем высоту кнопки
            save_button.clicked.connect(lambda: ConfigurationDialog.save_selected_configuration(parent, config_list, user_id))
            layout.addWidget(save_button)

            # Кнопка "Назад"
            back_button = QtWidgets.QPushButton("Назад", dialog)
            back_button.clicked.connect(dialog.close)  # Закрываем текущее окно
            layout.addWidget(back_button)

            dialog.exec_()
        else:
            QtWidgets.QMessageBox.information(parent, "Информация", "Нет доступных готовых конфигураций для выбранного бюджета.")

    @staticmethod
    def save_selected_configuration(parent, config_list, user_id):
        selected_item = config_list.currentItem()
        if selected_item:
            try:
                selected_config = selected_item.text()
                # Разбираем выбранную конфигурацию
                parts = selected_config.split(" - ")
                if len(parts) < 4:
                    raise ValueError("Неверный формат конфигурации")

                configuration = {
                    "processor": parts[0],
                    "videocard": parts[1],
                    "memory": parts[2],
                    "motherboard": parts[3].split(" (")[0],
                    "price": parts[3].split(" (")[1].split("$)")[0],
                    "power_supply": ConfigLogic.get_power_supply(parts[1])  # Добавляем блок питания
                }
                # Сохраняем конфигурацию в базу данных
                parent.db.save_configuration(user_id, str(configuration))
                QtWidgets.QMessageBox.information(parent, "Успех",
                                                  "Готовая конфигурация сохранена:\n" + str(configuration))

                # Вывод всех комплектующих
                ConfigurationDialog.show_all_components(parent, configuration)
            except Exception as e:
                QtWidgets.QMessageBox.warning(parent, "Ошибка", f"Ошибка при сохранении конфигурации: {e}")
        else:
            QtWidgets.QMessageBox.warning(parent, "Ошибка", "Выберите конфигурацию для сохранения.")

    @staticmethod
    def show_all_components(parent, configuration):
        # Вывод всех комплектующих в диалоговом окне
        dialog = QtWidgets.QDialog(parent)
        dialog.setWindowTitle("Ваша конфигурация")
        dialog.setGeometry(100, 100, 600, 400)
        dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)

        layout = QtWidgets.QVBoxLayout(dialog)

        # Добавляем текстовое поле с комплектующими
        components_text = f"Процессор: {configuration['processor']}\n" \
                          f"Материнская плата: {configuration['motherboard']}\n" \
                          f"Оперативная память: {configuration['memory']}\n" \
                          f"Видеокарта: {configuration['videocard']}\n" \
                          f"Блок питания: {configuration['power_supply']}"

        components_label = QtWidgets.QLabel(components_text, dialog)
        components_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(components_label)

        # Кнопка "Закрыть"
        close_button = QtWidgets.QPushButton("Закрыть", dialog)
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.exec_()

    @staticmethod
    def view_saved_configurations(parent, user_id):
        configurations = parent.db.view_saved_configurations(user_id)
        if configurations:
            dialog = QtWidgets.QDialog(parent)
            dialog.setWindowTitle("Сохраненные конфигурации")
            dialog.setGeometry(100, 100, 800, 600)
            dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint)

            layout = QtWidgets.QVBoxLayout(dialog)

            # Список сохраненных конфигураций
            config_list = QtWidgets.QListWidget()
            for config in configurations:
                config_list.addItem(config[0])  # Отображаем только текст конфигурации
            layout.addWidget(config_list)

            # Кнопка "Назад"
            back_button = QtWidgets.QPushButton("Назад", dialog)
            back_button.clicked.connect(dialog.close)  # Закрываем текущее окно
            layout.addWidget(back_button)

            dialog.exec_()
        else:
            QtWidgets.QMessageBox.information(parent, "Информация", "Нет сохраненных конфигураций.")