@echo off
REM This uses the folder of the batch file (%~dp0) as the base for rbs.py.
python "%~dp0..\rbs.py" %*
