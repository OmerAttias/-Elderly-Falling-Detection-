# "Elderly Falling Detection"

A concept project for elderly safety walking.

## "Description"

Tracking and angle detecting of a Walking stick.

The project split to two main parts:

- Image Proccesing - using hough transform and other CV's technics, I created a line detecting in space. The system will track a specific line and calculates it's current angle position.

- Robotics - using PID controll technic, I programmed a robot to track the line. 

## " Before we start... "

I used a "Yahboom Raspbot AI Vision Robot Car".

Raspbot is specially designed for AI beginners to learn AI at the lowest cost and include all you need for this project.

Link to the purchase page -

https://category.yahboom.net/products/raspbot?_pos=1&_sid=b0c180d95&_ss=r

## " installation packages "

```python

import cv2

import YB_Pcb_Car

import numpy as np

import matplotlib.pylab as plt

import math

import time

import RPi.GPIO as GPIO
```


