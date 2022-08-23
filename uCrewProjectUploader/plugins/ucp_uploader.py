import pcbnew, os, sys, json, traceback, logging
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from .ui import Ui_MainWindow 
from .uiPcb import Ui_uiPcb 
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
    def __init__(self, data = None):
        super(Configuration, self).__init__()
        self.log = logging.getLogger('ucp_uploader.py')
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.configurationFile = self.path + '/config.json'
        self.data = data

    def readConfigurationFile(self):
        self.log.debug("Read " + self.configurationFile)
        try:
            with open(self.configurationFile) as f:
                self.data = data = json.load(f)
        except Exception as e:
            self.log.debug('Error while reading configuration file')
            self.log.debug(e, exc_info=True)

    def checkAuth(self):
        print(self.data)
        if self.data == None:
            self.log.debug('Error while checking auth, data not found')
            return False
        else:
            if not 'error' in self.data:
                self.log.debug('No errors and file exists, auth accepted')
                return True
            else:
                self.log.debug('Error while checking auth, user has errors')
                return False
        

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
        self.api = 'http://' + self.server + '/?page=uCrewProjectsUploader/api&key=ucpu&login=' + self.user + '&password=' + self.password
        self.auth()

    def auth(self):
        try:
            self.log.debug('Try to connecting to server ' + self.api)
            response = urlopen(self.api)
            if response.status != 200:
                QMessageBox.about(self, "Response error", "Server not answer")

            self.log.debug('Data from server: ') 
            request = response.read().decode()
            self.log.debug(request)    
            
            data = json.loads(request)
            
            with open(self.configurationFile, 'w', encoding='utf-8') as f:
                f.write(request)
            f.close()
            
            config = Configuration(data)
            
            if config.checkAuth():
                QMessageBox.about(self, "Авторизация", "Вы успешно авторизованы!")
            else:
                QMessageBox.about(self, "Авторизация", "Ошибка, неверный логин или пароль")

        except Exception as e:
            self.log.debug('Error while do auth')
            self.log.debug(e, exc_info=True)
            QMessageBox.about(self, "Ошибка", "Не верные данные")

class GUIProject(QtWidgets.QMainWindow, Ui_uiPcb):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.log = logging.getLogger('ucp_uploader.py')
        logging.debug("GUIProject Class Inited")
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.configurationFile = self.path + '/config.json'
        self.server = ""
        self.user = ""
        self.password = ""
        self.api = 'http://' + self.server + '/?page=uCrewProjectsUploader/api&key=ucpu'
        self.pcbs = []
       

    def getPcbsList(self):
        url = self.api + '&param=getPcbs' 
        self.log.debug('Try to connecting to server ' + url)
        response = urlopen(url)
        if response.status != 200:
            QMessageBox.about(self, "Response error", "Server not answer")
        self.log.debug('Data from server: ') 
        request = response.read().decode()
        self.log.debug(request)  
        data = json.loads(request)
        self.cmbPcbs.clear()
        for pcb in data:
            self.cmbPcbs.addItem(pcb)
        
class uCrewProjectsUploader(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "uCrewProjects Uploader"
        self.category = "Tools"
        self.description = "This plugin allows you to upload your project to the uCrewProject server"
        self.show_toolbar_button = False # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'ucp_uploader.png') # Optional, defaults to ""

    def Run(self):
        log = logging.getLogger('ucp_uploader.py')
        # Init configuration
        config = Configuration()
        # Read configuration
        config.readConfigurationFile();
        
        if config.checkAuth():
            log.debug('Success, get configuration file, check project')
            self.showProject()
        else:
            log.debug('Cant get configuration file, auth')
            self.showAthorization()
        
    def showAthorization(self):
        app = QtWidgets.QApplication(sys.argv) 
        window = GUI()
        window.show()
        app.exec_()

    def showProject(self):
        app = QtWidgets.QApplication(sys.argv) 
        window = GUIProject()
        window.show()
        app.exec_()