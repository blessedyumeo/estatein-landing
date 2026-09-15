@echo off
chcp 65001 >nul
title Estatein -> GitHub Pages
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy.ps1"
echo.
pause
