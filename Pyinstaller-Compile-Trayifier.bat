@echo off
call activate trayify
PyInstaller PyInstallerEntry.py --version-file=Trayifier_info.txt --clean --add-data "src/trayifier/config.toml;trayifier" --name Trayify --onefile --noconsole --noconfirm
call conda deactivate
pause