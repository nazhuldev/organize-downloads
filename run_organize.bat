@echo off
REM ============================================
REM  run_organize.bat
REM  Chay script organize_downloads.py voi --run
REM  Dat file .bat nay CHUNG THU MUC voi file
REM  organize_downloads.py
REM ============================================

cd /d "%~dp0"
python organize_downloads.py --run

REM Ghi lai thoi diem chay lan cuoi (de kiem tra Task Scheduler co chay khong)
echo Lan chay cuoi: %date% %time% >> last_run.txt
