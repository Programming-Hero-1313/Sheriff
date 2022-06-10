import cv2
import dlib
import time
from datetime import datetime
import os
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from colorama import Fore, Back, Style
from colorama.ansi import code_to_chars
import colorama
import time

os.system('cls')

print(f"\n{Fore.CYAN}-------------------- Sheriff - Console --------------------{Fore.WHITE}")

carCascade = cv2.CascadeClassifier('data/HaarCascadeClassifier.xml')

root = Tk()

root.geometry('700x350')
root.title("Sheriff - Home")
root.iconbitmap("res/logo.ico")
root.configure(bg="black")

titlelabel = Label(root, text="SHERIFF",bg="black", fg="white", font=("Keep Calm Med",30))
titlelabel.pack()

l1 = Label(root, bg="black")
l1.pack()

l2 = Label(root, text="ENTER THE SPEED LIMIT",bg="black", fg="white", font=("Keep Calm Med",25))
l2.pack()

textVar = tk.IntVar()

inputbox = Entry(root, textvariable=textVar, bg='white',fg='black',font=('Keep Calm Med',30),justify=CENTER)
inputbox.pack()

WIDTH = 1280 #WIDTH OF VIDEO FRAME
HEIGHT = 720 #HEIGHT OF VIDEO FRAME
cropBegin = 240 #CROP VIDEO FRAME FROM THIS POINT
mark1 = 120 #MARK TO START TIMER
mark2 = 360 #MARK TO END TIMER
markGap = 15 #DISTANCE IN METRES BETWEEN THE MARKERS
fpsFactor = 3 #TO COMPENSATE FOR SLOW PROCESSING
startTracker = {} #STORE STARTING TIME OF CARS
endTracker = {} #STORE ENDING TIME OF CARS

#MAKE DIRCETORY TO STORE OVER-SPEEDING CAR IMAGES
if not os.path.exists('overspeeding/cars/'):
    os.makedirs('overspeeding/cars/')
    
try:
    reportFile = open('overspeeding/report.log','a')
except FileExistsError as e:
    os.remove('overspeeding/report.log')
    reportFile = open('overspeeding/report.log','a')


def blackout(image):
    xBlack = 360
    yBlack = 300
    triangle_cnt = np.array( [[0,0], [xBlack,0], [0,yBlack]] )
    triangle_cnt2 = np.array( [[WIDTH,0], [WIDTH-xBlack,0], [WIDTH,yBlack]] )
    cv2.drawContours(image, [triangle_cnt], 0, (0,0,0), -1)
    cv2.drawContours(image, [triangle_cnt2], 0, (0,0,0), -1)

    return image

def saveReport(speed,id,speedlimit):
    now = datetime.today().now()
    if speed > speedlimit:
        reportLine = now.strftime("%d/%m/%Y\t%H:%M:%S") + f"\tID-{id}\tSPEED-{speed}kmph OVERSPEED\n"
        reportFile.write(reportLine)
    if speed < speedlimit:
        reportLine = now.strftime("%d/%m/%Y\t%H:%M:%S") + f"\tID-{id}\tSPEED-{speed}kmph UNDERSPEED\n"
        reportFile.write(reportLine)

def saveCar(speed,image,id):
    now = datetime.today().now()
    nameCurTime = now.strftime("%d-%m-%Y-%H-%M-%S")
    finalName = nameCurTime + f"-{speed}-{id}"

    link = 'overspeeding/cars/'+finalName+'.jpeg'
    cv2.imwrite(link,image)

#FUNCTION TO CALCULATE SPEED----------------------------------------------------
def estimateSpeed(carID):
    timeDiff = endTracker[carID]-startTracker[carID]
    speed = round(markGap/timeDiff*fpsFactor*3.6,2)
    return speed

#FUNCTION TO TRACK CARS---------------------------------------------------------
def trackMultipleObjects():
    filetypes = (
        ('MP4 files', '*.mp4'),
        ('MOV files', '*.mov'),
        ('WMV files', '*.wmv'),
        ('AVI files', '*.avi'),
        ('MKV files', '*.mkv'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(title='Sheriff - Select Video File',initialdir='/',filetypes=filetypes)
    if filename == '':
        messagebox.showerror("Sheriff - Error", "Please Select a Video File!")
        print(f"{Fore.RED}Please Select a File!{Fore.WHITE}")
        trackMultipleObjects()
    elif filename.endswith(".mp4") or filename.endswith(".mov") or filename.endswith(".wmv") or filename.endswith(".avi") or filename.endswith(".mkv"):
        print(f"\n{Fore.GREEN}Video File selected - {Fore.YELLOW}{filename}")
        video = cv2.VideoCapture(f'{filename}')
    else:
        messagebox.showerror("Sheriff - Error", "Invalid File Selected!")
        print(f"{Fore.RED}Invalid File Selected!{Fore.WHITE}")
        trackMultipleObjects()
    speedLimit =  textVar.get()
    print(f'\n{Fore.GREEN}Speed Limit Set at : {Fore.YELLOW}{speedLimit} Kmph\n{Fore.WHITE}')
    btn.destroy()
    inputbox.destroy()
    l2.destroy()
    root.geometry("1300x556")
    rectangleColor = (0, 255, 0)
    frameCounter = 0
    currentCarID = 0
    carTracker = {}

    while True:
        rc, image = video.read()
        if type(image) == type(None):
            break

        frameTime = time.time()
        image = cv2.resize(image, (WIDTH, HEIGHT))[cropBegin:720,0:1280]
        resultImage = blackout(image)
        cv2.line(resultImage,(0,mark1),(1280,mark1),(0,0,255),2)
        cv2.line(resultImage,(0,mark2),(1280,mark2),(0,0,255),2)

        frameCounter = frameCounter + 1

        #DELETE CARIDs NOT IN FRAME---------------------------------------------
        carIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:
            carTracker.pop(carID, None)

        #MAIN PROGRAM-----------------------------------------------------------
        if (frameCounter%60 == 0):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24)) #DETECT CARS IN FRAME

            for (_x, _y, _w, _h) in cars:
                #GET POSITION OF A CAR
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)

                xbar = x + 0.5*w
                ybar = y + 0.5*h

                matchCarID = None

                #IF CENTROID OF CURRENT CAR NEAR THE CENTROID OF ANOTHER CAR IN PREVIOUS FRAME THEN THEY ARE THE SAME
                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()

                    tx = int(trackedPosition.left())
                    ty = int(trackedPosition.top())
                    tw = int(trackedPosition.width())
                    th = int(trackedPosition.height())

                    txbar = tx + 0.5 * tw
                    tybar = ty + 0.5 * th

                    if ((tx <= xbar <= (tx + tw)) and (ty <= ybar <= (ty + th)) and (x <= txbar <= (x + w)) and (y <= tybar <= (y + h))):
                        matchCarID = carID


                if matchCarID is None:
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                    carTracker[currentCarID] = tracker

                    currentCarID = currentCarID + 1


        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()

            tx = int(trackedPosition.left())
            ty = int(trackedPosition.top())
            tw = int(trackedPosition.width())
            th = int(trackedPosition.height())

            #PUT BOUNDING BOXES-------------------------------------------------
            cv2.rectangle(resultImage, (tx, ty), (tx + tw, ty + th), rectangleColor, 2)
            cv2.putText(resultImage, str(carID), (tx,ty-5), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1)

            #ESTIMATE SPEED-----------------------------------------------------
            if carID not in startTracker and mark2 > ty+th > mark1 and ty < mark1:
                startTracker[carID] = frameTime

            elif carID in startTracker and carID not in endTracker and mark2 < ty+th:
                endTracker[carID] = frameTime
                speed = estimateSpeed(carID)
                if speed > speedLimit:
                    print(f'{Fore.BLUE}CAR-ID : {carID} - {Fore.YELLOW}{speed} kmph - {Fore.RED}OVERSPEED{Fore.RESET}\n')
                    saveCar(speed,image[ty:ty+th, tx:tx+tw],carID)
                    saveReport(speed, carID, speedLimit)
                else:
                    print(f'{Fore.BLUE}CAR-ID : {carID} - {Fore.YELLOW}{speed} kmph - {Fore.GREEN}UNDERSPEED{Fore.RESET}\n')
                    saveReport(speed, carID, speedLimit)
                    
        img = ImageTk.PhotoImage(Image.fromarray(image))

        l1['image'] = img
        root.title(f"Sheriff - {filename}")

        root.update()

btn = Button(root, text="START",bg='white',fg='black',font=('Keep Calm Med',30),justify=CENTER,command=trackMultipleObjects)
btn.place(x=250,y=200)

def cursor_on(e):
    btn["bg"] = "grey"
def cursor_off(e):
    btn["bg"] = "white"

btn.bind("<Enter>", cursor_on)
btn.bind("<Leave>", cursor_off)

root.mainloop()