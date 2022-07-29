#!/bin/bash

echo "Convert auth .ui to .py"
pyuic5.exe uCrewProjectUploader/plugins/ui.ui -o uCrewProjectUploader/plugins/ui.py
echo "Convert pcb .ui to .py"
pyuic5.exe uCrewProjectUploader/plugins/uiPcb.ui -o uCrewProjectUploader/plugins/uiPcb.py
echo "Build packages in repository"
python3 compile.py