import pcbnew, os, sys, json

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

    def showAthorization(self):
        pass