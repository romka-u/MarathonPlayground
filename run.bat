@echo off
mkdir submissions 2> nul
mkdir logs 2> nul
if not exist seeds.txt echo 1 > seeds.txt
C:\Python27\python.exe server.py
