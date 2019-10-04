import argparse
import cv2
import numpy as np
import os, sys
import time 
import imutils
from imutils.video import VideoStream

refPt = []
cropping = False
calibrate = True
saved = False
autodataset = False
i = 0
firstFrame = None
sdThresh = 15

def search_min(roi):
    min_v = [255, 255, 255]
    max_v = [0, 0, 0]
    for each in roi:
        for each2 in each:
            x = 0
            while (x < 3):
                if (each2[x] < min_v[x]):
                    min_v[x] = each2[x]
                elif (each2[0] > max_v[x]):
                    max_v[x] = each2[0]
                x= x+ 1
    print (min_v, max_v)
    
    
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, calibrate, text
 
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if calibrate == True:
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True
    
        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt.append((x, y))
            cropping = False
            calibrate = False
            text = "ROI setted up"
            printtext(frame, text)
            cv2.imshow("frame",frame)

def printtext(frame, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    allign = (10, 20)
    fontScale = 1
    fontColor = (255,0,0)
    lineType = 2
    cv2.putText(frame,text, 
        allign, 
        font, 
        fontScale,
        fontColor,
        lineType)

def distMap(frame1, frame2):
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
 
# if the video argument is None, then we are reading from webcam
#if args.get("video", None) is None:
#    cap = VideoStream(src=0).start()
#    time.sleep(2.0)
 
# otherwise, we are reading from a video file
#else:
#    cap = cv2.VideoCapture(args["video"])
#NEED TO ANALYZE GREATEST NUMBER IN THE FOLDER
a = 0
mass = []
for filename in os.listdir("images"):
    basename, extension = os.path.splitext(filename)
    project, number = basename.split('_')
    mass.append(int(number))
if mass:
    a = max(mass) + 1
text = "ROI is not setted"
while(True):
    # Capture frame-by-frame
#    frame = cap.read()
    frame = cv2.imread("shell_scripts/images/ROI_6.jpg")
    clone = frame.copy()
    printtext(frame, text)
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", click_and_crop)
    key = cv2.waitKey(1) & 0xFF
    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        frame = clone.copy()
        cv2.imshow("frame", frame)
        refPt = []
        calibrate = True
        text = "ROI is not setted"
        cv2.destroyWindow("ROI")
        saved = False
        autodataset = False
        firstFrame = None
    # if the 'c' key is pressed, break from the loop
    elif key == ord("a") and saved == True:
        autodataset = True
        text = "AUTODATASET COLLECTION"
    elif key == ord("q"):
        break
    elif key == ord("s") and calibrate == False:
        try:
            cv2.imwrite( "shell_scripts/images/ROI_" + str(a) +".jpg", roi)
            a = a + 1
            text = "ROI SAVED"
            saved = True
        except Exception as e:
                print(e)

    elif key == ord("d"):
        folder = 'images'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                a = 0
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    if len(refPt) == 2:
            if autodataset:
                cv2.rectangle(frame, refPt[0], refPt[1], (255, 0, 0), 2)
            else:
                cv2.rectangle(frame, refPt[0], refPt[1], (255, 255, 0), 2)
    if key == ord("w"):
        if len(refPt) == 2:
            roi = clone[min(refPt[0][1], refPt[1][1]):max(refPt[1][1], refPt[0][1]), min(refPt[0][0], refPt[1][0]):max(refPt[0][0], refPt[1][0])]
            if autodataset:
                cv2.rectangle(frame, refPt[0], refPt[1], (255, 0, 0), 2)
            else:
                cv2.rectangle(frame, refPt[0], refPt[1], (255, 255, 0), 2)
            cv2.imshow("ROI", roi)
            search_min(roi)
    cv2.imshow("frame", frame)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
