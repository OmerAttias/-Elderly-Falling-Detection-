import cv2
import numpy as np
import matplotlib.pylab as plt
import math
import time
import RPi.GPIO as GPIO


class PID_Controll:
    def __init__(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.SystemOutput = 0.0
        self.PidOutput = 0.0
        self.PIDErrorSUM = 0.0
        self.previousError = 0.0

    def Process(self,midImage,dt):

        # def of the "wanted" target monitoring
        Error = midImage - self.SystemOutput
        #print('Err',Error)

        # Def PID values according to the traditional formula
        KpWork = self.Kp * Error
        #print('KpWork',KpWork)
        KiWork = self.Ki * self.PIDErrorSUM
        #print('KiWork',KiWork)
        KdWork = self.Kd * ((Error - self.previousError)/dt)
        #print('KdWork',KdWork)

        # PID general formula
        self.PidOutput = KpWork + KiWork + KdWork
        #print('PidOutput',self.PidOutput)

        # summing the error for the Ki part in the formula
        self.PIDErrorSUM += Error
        #piderraddcheck = self.PIDErrorSUM
        #print('piderraddcheck',PIDErrorSUM)

        # Def error current to be previous for the next calculate and for
        # the Kd part in the formula
        self.previousError = Error

        # Def the pid output as our system output.
        # just to clarify the system ouput.
        self.SystemOutput = self.PidOutput
        #print('SystemOutput',self.SystemOutput)



# import Yahboom libary for cotrolling the DC motors and the servo motor
import YB_Pcb_Car
car_servo = YB_Pcb_Car.YB_Pcb_Car()
# Def starting postion for the seroves motors horizontal and vertical
# it will start at 90 degrees
car_servo.Ctrl_Servo(1,90)
car_servo.Ctrl_Servo(2,90)

# define the buzzer sensor
# it tells which pin nunbering system
# i am going to use.
GPIO.setmode(GPIO.BOARD)
# define the buzzer channel as output
GPIO.setup(32, GPIO.OUT)
# define the the channel and the frequency.
p = GPIO.PWM(32, 600)


# Putting values Kp,Ki,Kd to the PID controll class i have just define
xservo_pid = PID_Controll(0.5 , 0.2, 0.009)
yservo_pid = PID_Controll(0.8, 0.17, 0.0135)

# get a video capture object for the camera
cap = cv2.VideoCapture(0, cv2.CAP_V4L)


# constant value, represents the real line distance from the camera in mm, used to detect the pixeld focallength
known_distance_in_mm = 200
# constant value, represents the real width of the line
real_width_in_mm = 190

# function which calculate focal length of the camera
def FocalLenght(known_distance_in_mm, real_width_in_mm, width_in_pixels):
    focallength = (width_in_pixels*known_distance_in_mm)/real_width_in_mm
    return focallength

# calling the focal length function for one time focal length calculation
focallength = FocalLenght(known_distance_in_mm = 200 , real_width_in_mm = 190, width_in_pixels = 670)
#print(focallength)


#HSV red values arrays
low_red = np.array([115, 50, 50])
high_red = np.array([130, 255, 255])

def filters(img,Lower_threshold,Upper_threshold):
    # change the image from RGB to HSV colors
    imgInhsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # first filter which filters the red in the image
    mask = cv2.inRange(imgInhsv, low_red, high_red)
    # second filter which erode the red objects
    mask = cv2.erode(mask, None, iterations=5)
    # third filter which dilate the red objects
    mask = cv2.dilate(mask, None, iterations=5)
    return mask



#Returns true if video capturing has been initialized already.
while(cap.isOpened()):
    #reads the data per frame. 'ret' refer to a any kind of boolean return and 'img' refer the the each img that returns
    ret, img = cap.read()
    #resize the image to smaller size because  defaults dimenstions are to big and its slowing the proccessing
    img = cv2.resize(img,(640,480))
    #define rows and cols on img dimensions
    rows, cols, _ = img.shape
    #puting cols into variable
    height = img.shape[0]
    #puting rows into variable
    width = img.shape[1]
    #print("height",height,"width",width)

    #define a variable for middle frame point
    #xC = int(rows/2)
    #yC = int(cols/2)

    x_centure = int(cols/2)
    y_centure = int(rows/2)

    # define a loop for a case when the read function dosent return any boolean at all.
    if ret:
        #this action resolves an NoneType errors while there is no red color in th frame
        assert not isinstance(img,type(None)),'frame not found'
    #define 2 variables for the current and the previous time(= for FPS value).
    pTime = 0
    cTime = 0


    while True:
        _, img = cap.read()
        img = cv2.resize(img,(640,480))
        # the frame default is in BGR. convert to BGR to show the image in "real" colors.
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #sending the image to a filter system that return the image "cleaner".
        Img_Filterd= filters(img,low_red,high_red)

        cTime = time.time()
        dt =cTime-pTime
        #print('dt',dt)
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, "FPS " + str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0), 3)

        # define a function that do the hough transform action in the frame and return lines.
        lines = cv2.HoughLinesP(Img_Filterd, 1, np.pi / 180, 200, np.array([]), minLineLength=50, maxLineGap=25)

        # marks on the frame that refer to the middel point and 2 lines that located lefter an righter from the middle.
        cv2.circle(img, (x_centure,y_centure), 2, (255,0,0), 15)
        lineRight = cv2.line(img, (x_centure + 200, y_centure + 120), (x_centure + 200, y_centure - 120), (255,255,0),2)
        lineleft = cv2.line(img, (x_centure - 200, y_centure +120), (x_centure - 200, y_centure - 120) ,(255,255,0),2)


        #a loop that solve the error of no lines detected on the frame.
        if lines is not None:
            # a loop for the hough transform function
            for line in lines:
                # define 4 variables that refer to the extreme points of the line
                for x1, y1, x2, y2 in line:
                    # find the middle point of the line
                    xC = int((x1+x2)/2)
                    yC = int((y1+y2)/2)
                    #print(yC)
                    # define the ratio between x and y that refers to the line width in pixels
                    linewidth = int(math.sqrt((y2-y1)**2 +(x2-x1)**2))
                    #print('linewidth',linewidth)
                    distance = int((((real_width_in_mm*focallength)/linewidth))/10)
                    print('distance',int(distance))
                    break

                if distance < 60:
                    cv2.line(img, (x1,y1), (x2,y2), (0,0,0),3)
                    # show the line on the frame
                    cv2.circle(img, (xC,yC), 2, (0,0,255), 15)
                    cv2.circle(img, (x1,y1), 2, (0,255,0), 3)
                    cv2.circle(img, (x2,y2), 2, (0,255,0),3)
                    # caculate the line angle postion
                    angle = abs(math.degrees(math.atan2(y2-y1,x2-x1)))
                    #print(angle)
                    if angle < 45:
                        # define buzzer's the duty cycle
                        p.start(50)
                    else:
                        p.stop()


                    cv2.putText(img,str(int(angle)),(xC-30,yC+80),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
                    break


            # for the horizontal servo motor
            # define the system wanted output which is the x middle point of the line
            xservo_pid.SystemOutput =  xC
            #print('xservo_pid.SystemOutput',xservo_pid.SystemOutput)
            # calling the function of the PID process with the varaibles of the mid width and the time Derivative
            xservo_pid.Process(width/2,dt)
            #print('xservo_pid.SystemOutput2',xservo_pid.SystemOutput)
            # normalization of the pid output to normal servo values output
            target_servox = int((1000 + xservo_pid.SystemOutput) / 10)
            #print('target_servox',target_servox)

            # because the servos motors have movements limitaions so i put two condtions that will limit
            # the servo target to his abilities
            if target_servox > 180:
                target_servox = 180
            if target_servox < 0:
                target_servox = 0

            # same process to the vertical servo motor
            yservo_pid.SystemOutput = yC
            yservo_pid.Process(height/2,dt)
            #print('yservo_pid.PIDErrADD',yservo_pid.PIDErrADD)
            #print('yservo_pid.ErrBack',yservo_pid.ErrBack)
            target_servoy = int((1000 - yservo_pid.SystemOutput) / 10)
            #print('yservo_pid.SystemOutput',yservo_pid.SystemOutput)

            #print('target_servoy',target_servoy)
            #print(yservo_pid.ErrBack)
            if target_servoy > 180:
                target_servoy = 180
            if target_servoy < 0:
                target_servoy = 0

            # the servo motor movement command across the PID changes
            car_servo.Ctrl_Servo(1, target_servoy)
            car_servo.Ctrl_Servo(2, target_servox)

            # Robotics part
            # just if the system recognize line with cetain ditance it continue to movment controll
            if  60 > distance > 25:

                # condition for turning right
                if  target_servox == 0:
                    car_servo.Car_Spin_Right(45,0)
                # condition to turning left
                if target_servox == 180:
                    car_servo.Car_Left(0,45)
                # condtion to movment and fixing on the borders range.
                if x_centure - 200 < xC < x_centure + 200:
                    if 90 < target_servox < 180:
                        car_servo.Car_Back(30,30)
                    elif 0 < target_servox < 70:
                        car_servo.Car_Run (30,30)
                    elif 70 < target_servox < 90:
                        car_servo.Car_Stop()
                # condtion to move Straight
                if xC >= x_centure + 200:
                    car_servo.Car_Run(30,30)
                # condtion to move backwards
                if  xC <= x_centure - 200 :
                    car_servo.Car_Back(30,30)


        # ploting the video
        cv2.imshow('frame',img)
        # ploting the video in the filter dimmenstion
        #cv2.imshow("mask", Img_Filterd)
        cv2.waitKey(1)
