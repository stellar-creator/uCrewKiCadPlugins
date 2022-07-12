import pcbnew, os, sys, json, traceback, logging
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from .ui import Ui_MainWindow 
from urllib.request import urlopen

logFile = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename=logFile + '/debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('ucp_uploader.py')

logging.debug("Logger enabled")

class Configuration():
    def __init__(self):
        super(Configuration, self).__init__()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.configurationFile = self.path + '/config.json'

    def checkAuth(self):
        return True
        

class GUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.btnAuth.clicked.connect(self.btnAuthClick)
        self.log = logging.getLogger('ucp_uploader.py')
        self.server = ""
        self.user = ""
        self.password = ""
        self.api = ""
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.configurationFile = self.path + '/config.json'
        logging.debug("GUI Class Inited")

    def btnAuthClick(self):
        self.log.debug('btnAuth was Clicked')
        self.server = self.txtServer.text()
        self.user = self.txtLogin.text()
        self.password = self.txtPassword.text()
        self.api = 'http://' + self.server + '/?page=uCrewProjectsUploader/api&login=' + self.user + '&password' = self.password
        self.auth()

    def auth(self):
        try:
            self.log.debug('Try to connecting to server ' + self.api)
            response = urlopen(self.api)
            if response.status != 200:
                QMessageBox.about(self, "Response error", "Server not answer")
            data = json.loads(response.read().decode())

            with open(self.configurationFile, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            config = Configuration()
            
            if config.checkAuth():
                QMessageBox.about(self, "Авторизация", "Вы успешно авторизованы!")
            else:
                QMessageBox.about(self, "Авторизация", "Ошибка, неверный логин или пароль")
        except Exception as e:
            self.log.debug('Error while do auth')
            self.log.debug(e, exc_info=True)
            QMessageBox.about(self, "Error", "Cant get data")



class uCrewProjectsUploader(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "uCrewProjects Uploader"
        self.category = "Tools"
        self.description = "This plugin allows you to upload your project to the uCrewProject server"
        self.show_toolbar_button = False # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'ucp_uploader.png') # Optional, defaults to ""

    def Run(self):
        self.showAthorization()

    def showAthorization(self):
        app = QtWidgets.QApplication(sys.argv) 
        window = GUI()
        window.show()
        app.exec_()