@echo off
cd /d %~dp0
call conda activate base

python api.py

pause
