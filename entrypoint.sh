#!/bin/bash
# Start Xvfb in the background
Xvfb :99 -screen 0 1280x1024x16 &
export DISPLAY=:99

# Run the Python script that uses Selenium
python app.py
