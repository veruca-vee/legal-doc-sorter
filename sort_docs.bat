@echo off
REM Windows wrapper. The real work is sort_docs.py (needs Python 3).
py -3 "%~dp0sort_docs.py" %*
if errorlevel 1 python "%~dp0sort_docs.py" %*
