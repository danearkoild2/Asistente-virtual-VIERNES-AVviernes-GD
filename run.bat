@echo off
title MARK LV
py -3.12 main.py %*
if errorlevel 1 pause
