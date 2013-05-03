#!/bin/bash -e

touch seeds.txt
mkdir -p submissions
mkdir -p logs
python server.py
