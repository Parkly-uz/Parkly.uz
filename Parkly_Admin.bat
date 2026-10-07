@echo off
title Parkly.uz — Smart Parking Desktop Admin Panel
cd /d "%~dp0"
echo ========================================================
echo   Parkly.uz — Desktop Admin Panel ishga tushmoqda...
echo ========================================================
python desktop_admin\run_admin_app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Xatolik yuz berdi. Tugmani bosing...
    pause
)
