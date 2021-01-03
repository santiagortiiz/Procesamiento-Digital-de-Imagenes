#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:02:15 2020

@author: jfochoa
"""


#Create a VideoWriter object. 
#We should specify the output file name (eg: output.avi). 
#Then we should specify the FourCC code. 
#Then number of frames per second (fps) and frame size should be passed.
#And last one is isColor flag. 
#If it is True, encoder expect color frame, otherwise it works with grayscale frame.
#FourCC is a 4-byte code used to specify the video codec. 
#The list of available codes can be found in fourcc.org. 
#It is platform dependent. Following codecs works fine for me.
#- In Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2. 
# (XVID is more preferable. MJPG results in high size video. X264 gives very small size video)
#- In Windows: DIVX (More to be tested and added)
#FourCC code is passed as cv2.VideoWriter_fourcc('M','J','P','G')
#VideoWriter_fourcc(*'MJPG) for MJPG.

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

# Define the codec and create VideoWriter object
codec = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('salida.mp4',codec, 20.0, (width,height))
while(True):
  # Capture frame-by-frame 
  ret, frame = cap.read()
  
  # write the flipped frame
  out.write(frame)
  
  # Our operations on the frame come here
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  # Display the resulting frame
  cv2.imshow('frame',gray)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()