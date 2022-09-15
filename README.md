# "Elderly Falling Detection"

A concept project for elderly safety walking.

Many of the 

## "Description"

Tracking and angle detecting of a Walking stick.

The project split to two main parts:

- Image Proccesing - using hough transform and other CV's technics, I created a line detecting in space. The system will track a specific line and calculates it's current angle position.

- Robotics - using PID controll technics, I programmed a robot to track a specific line in space. 

## " Before we start... "

I used a "Yahboom Raspbot AI Vision Robot Car".

Raspbot is specially designed for AI beginners to learn AI at the lowest cost and include all you need for this project.

 - It has a Customized package (YB_Pcb_Car) that does the integration between the overall components and the raspberry pi.

 - The easy access to the components programming saves a lot of technical job and makes it easier to focus on the image processing.

Link to purchase page:

https://category.yahboom.net/products/raspbot?_pos=1&_sid=b0c180d95&_ss=r


<img src="https://user-images.githubusercontent.com/101269937/190184712-ad14d2e9-e70a-43a0-9437-20c94b0c1d50.jpg" width="250" height="200">

### "Note"

**for those who pass the purchase, it's available to use only the image processing part where only required a camera component**

## " Installation Packages "

```python

import cv2

import YB_Pcb_Car

import numpy as np

import matplotlib.pylab as plt

import math

import time

import RPi.GPIO as GPIO
```

## "Image processing - line detection"

For this part i had to filtering a lot of noise.
The main mission was to detect your walking stick line as "clean" as possible.

Algorithm summary:

- Before i worked on a video, I wanted to have a success on image dimension.
I took a random photos of the line (uploaded on "Image for IP") 

- I converted the image to binary (easy to work on) with using HSV scale.

![before filtering](https://user-images.githubusercontent.com/101269937/190336605-379e1eb5-3874-4007-9e9e-59a923d46ae5.png)

- used to successive filters "Erode" and "Dilate" that are very usefull on small noise cleaning and emphasize the wanted line.

![after filtering](https://user-images.githubusercontent.com/101269937/190337076-cfba1ef7-ca40-4d9a-8545-b46114f79e8d.png)

- Because the line detecting rely on color, I had to build more defences in case of line detecting. 
Using simple optics theory and camera data sheet, I succesd to guess , with minimal error, the line 
 
  distance.
  
  ![distance detectt](https://user-images.githubusercontent.com/101269937/190341882-1c0ddfb0-9224-4b0d-94ee-43b593a6dc29.png)

  
  As result The noise which goes behind and befor the measured distance, will be filterd.
  
 - Until this point, the line was note even detected. 
 **reminder:The main goal of the previous actions was the maximize the chances chances to detect the correct line in the cleanest way**
  
  ![after filtering](https://user-images.githubusercontent.com/101269937/190339959-4824ae24-f2ab-4c6e-abf3-3a87c7ef600a.png)


 - To detect the line i used the "Hough transform" function. (**it's emposibiile to detect a single line only with this funcion**).
 
 - After i detected a single line, It's time to detect the line's angle that will be the falling decision line.
 
 
![optics](https://user-images.githubusercontent.com/101269937/190341685-aad37d25-9d5d-4655-be9c-3078120975ff.jpg)

### final result:

![imageprocssingfinal reslt](https://user-images.githubusercontent.com/101269937/190341797-ae2a3fb8-ee3e-4889-bd5f-c0756e14b1a6.png)

![line tracked](https://user-images.githubusercontent.com/101269937/190342221-c742caff-76f6-499e-b82c-46cb36d39939.jpg)


