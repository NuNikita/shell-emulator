@echo off
cd /d "%~dp0.."

python main.py ^
    --vfs "." ^
    --prompt "success> " ^
    --script "scripts\startup_success.txt"