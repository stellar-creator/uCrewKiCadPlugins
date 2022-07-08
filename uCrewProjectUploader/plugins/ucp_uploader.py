import pcbnew, os, sys, json
from PyQt5 import QtWidgets
from .ui import Ui_MainWindow

class GUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

class uCrewProjectsUploader(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "uCrewProjects Uploader"
        self.category = "Tools"
        self.description = "This plugin allows you to upload your project to the uCrewProject server"
        self.show_toolbar_button = False # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'ucp_uploader.png') # Optional, defaults to ""

    def Run(self):
        # The entry function of the plugin that is executed on user action
        print("Hello World")
        self.showAthorization()

    def showAthorization(self):
        app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
        window = GUI()  # Создаём объект класса ExampleApp
        window.show()  # Показываем окно
        app.exec_()  # и запускаем приложение