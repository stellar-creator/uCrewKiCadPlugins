import pcbnew, os, sys

from .ucp_uploader import uCrewProjectsUploader
from .ui import Ui_MainWindow

uCrewProjectsUploader().register()