@echo off
REM This uses the folder of the batch file (%~dp0) as the base for sfs.py.
python "%~dp0..\sfs.py" %*
