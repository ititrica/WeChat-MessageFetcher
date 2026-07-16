@echo off
chcp 65001 >nul
title WeChat Message Fetcher

cd /d "%~dp0"

echo ============================================
echo  WeChat Message Fetcher
echo  Grabs YOUR text messages from the CURRENT
echo  active chat window, scroll up to 1200 msgs.
echo ============================================
echo.

python -X utf8 "fetch_msgs.py"

echo.
if %errorlevel% equ 0 (
    echo ============================================
    echo  Done! Check output file in this folder.
    echo ============================================
) else (
    echo ============================================
    echo  Error. Make sure:
    echo  1. WeChat is running and logged in
    echo  2. The target chat window is open
    echo    and visible (not minimized)
    echo ============================================
)

echo.
pause
