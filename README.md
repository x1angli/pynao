# pynao

Nao ("now") is a programmable humanoid robot developed by Aldebaran Robotics. It supports programming based on its Python and C++ SDKs. Since Python has a much smoother deployment process, this repo is tied with Python. 

## Installation

Before you start with your first line of code, you need to do these things first:
1. Get a Nao robot, of course 
2. Install Python 2.7 (https://www.python.org/downloads/release/python-2710/) . Note: only 32-bit version is supported by Nao's SDK, so even if you have a 64-bit CPU or OS, you still need to download the Python 2.7 X86 version!
3. Install Nao's Python Naoqi SDK (https://community.aldebaran.com/en/resources/software/language/en-gb). Note: you need to set up an account on aldebaran.com, also you need to register at least one Nao with that account so as to download the SDK!
4. (Optional) Setup one or more Python IDE on your computer

## General Usage
Download one Python file or clone the entire Git repo. Change the hard-coded IP address in the .py files. And execute the file.

## Introduction (Module-by-module)

* almotion_basic.py

This one controls basic movements of Nao. Please note the information as output from motion.getSummary()

## Troubleshooting 

1. file '/home/nao/mp3/xxxxxxxxxx.mp3' not found

Sometimes I used locally generated MP3 files to replace the default TTS engine. Here, you can feel free to replace those MP3 files on your own.
