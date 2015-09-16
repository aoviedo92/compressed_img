@echo off
set name=ImageCompresor
set icon=icon.ico
set script=compressed.pyw
pyinstaller -n %name% -w -F --hidden-import=atexit -i %icon% %script%
start dist
pause