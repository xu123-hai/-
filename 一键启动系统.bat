@echo off
chcp 65001
title 刀具磨损预测系统启动器

echo ==============================================
echo    刀具磨损状态识别与RUL预测系统
echo ==============================================
echo.
echo 正在启动系统，请稍候...
echo 启动成功后会自动打开浏览器
echo.

cd /d "%~dp0src"

start "" http://127.0.0.1:5000
python app.py

pause
