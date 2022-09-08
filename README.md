# Sheriff : An AI enabled program to detect car speed

![Python](https://img.shields.io/badge/python-3.10-blue)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
![License](https://img.shields.io/badge/license-MIT-red)

## What is it?

Road accidents, A very common problem, but still nobody is using Al technology to solve it,
so I decided to make a program to solve it, Sheriff - An Al enabled program to detect car speed and to prevent road accidents, 
it will detect which car is overspeeding the speed limit and we can fine some charge to the driver, 
if the car is overspeeding, with Sheriff we can check which car was in overspeed or underspeed by checking the report.log file generated by the program, 
and it will also save the images of cars which were in overspeed, in a folder, to detect the speed, 
you have to select the video file and then it will start doing the process.

## Main Features

Here are just a few of the things that Sheriff does well:

 - Detect car speed using **speed=distance/time** formula.
 - You can detect car speed from any video file.
 - UI made with [PyQt5](https://www.qt.io/).

 ` We know these features are not enough to make a change, but we are trying to improve Sheriff, and hopefully we will reach our goal soon`

## Where to get it?

The source code is currently hosted on GitHub at:
https://github.com/Programming-Hero-1313/Sheriff

## Package

#### Links
 - [PyPi](https://pypi.org/project/sheriff/0.1/)
 - [Source code](https://github.com/Programming-Hero-1313/Sheriff)

#### Package Installation
    pip install sheriff

#### Package Features
 - Check version
 - Run the GUI
```
from sheriff import *
import sheriff

# Check Sheriff version -
print(sheriff.version())

# Run the GUI -
gui.run()
```


## Dependencies

- [OpenCV - OpenCV is a library of programming functions mainly aimed at real-time computer vision](https://opencv.org/)
- [NumPy - Adds support for large, multi-dimensional arrays, matrices and high-level mathematical functions to operate on these arrays](https://www.numpy.org)
- [PyQt5 - Qt is the fastest and smartest way to produce industry-leading software that users love](https://www.qt.io/) 
- [dlib - A toolkit for making real world machine learning and data analysis applications](http://dlib.net/)

## Installation

You can install the all requirements from requirements.txt by using pip.

    pip install -r requirements.txt

## Usage

    python scripts/main.py

[Video Tutorial for Sheriff Usage](https://streamable.com/29yprj)

**Enter the speed Limit**
- Enter the *Speed Limit* in the input box you want to set

**Click On Start Button**
 - Click on *Start* Button and select the video file

    Now Sheriff should Start detecting car speed from the provided video
    Do the following steps when the detection is complete
    If you are facing any errors feel free to contact me.

**Navigate to overspeeding directory**
 - Navigate to *Overspeeding* directory to see the report

**Navigate to overspeeding/cars directory**
 - Navigate to cars directory located in overspeeding directory to see the *images of cars* which were overspeeding
 
## Contact

- `Email` - ggambhir1919@gmail.com
- `Discord` - PROGRAMMING HERO#9829
- `YouTube` - https://www.youtube.com/c/PROGRAMMINGHERO1010
- `Instagram` - https://www.instagram.com/programming.hero/
