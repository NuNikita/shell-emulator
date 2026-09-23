@echo off
cd /d "%~dp0.."

python main.py ^
    --vfs "src" ^
    --prompt "error> " ^
    --script "scripts\startup_error.txt"