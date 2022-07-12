#!/bin/bash

echo "Converte .ui to .py"
pyuic5.exe uCrewProjectUploader/plugins/ui.ui -o uCrewProjectUploader/plugins/ui.py
echo "Build packages in repository"
python3 compile.py