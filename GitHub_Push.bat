@echo off
title Parkly.uz — GitHub Push
cd /d "%~dp0"
echo ========================================================
echo   Parkly.uz — GitHub-ga avtomatik yuklash
echo ========================================================
echo.
echo 1. Ozgarishlar tekshirilmoqda...
git status
echo.
echo 2. Barcha fayllar qoshilmoqda (git add)...
git add .
echo.
echo 3. Tasdiqlanmoqda (git commit)...
git commit -m "feat: avtomatik yangilanish va sinxronizatsiya"
echo.
echo 4. GitHub-ga yuklanmoqda (main branch)...
git push origin main
echo.
echo 5. GitHub-ga yuklanmoqda (Mirhamid branch)...
git push origin main:Mirhamid
echo.
echo ========================================================
echo   Muvaffaqiyatli yakunlandi!
echo ========================================================
pause
