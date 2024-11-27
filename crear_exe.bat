@echo off
echo Reinstalando dependencias...
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y
pip install PyQt6==6.4.2
pip install pandas
pip install openpyxl

echo Limpiando archivos anteriores...
rmdir /s /q dist
rmdir /s /q build
del *.spec

echo Creando ejecutable...
python -m PyInstaller --name="Inventario_LAB" --windowed --icon=logo.jpg --add-data="logo.jpg;." --hidden-import=PyQt6 --hidden-import=PyQt6.QtCore --hidden-import=PyQt6.QtGui --hidden-import=PyQt6.QtWidgets --collect-all PyQt6 --onefile inventario.py

echo Proceso completado!
pause
