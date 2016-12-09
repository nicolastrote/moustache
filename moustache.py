#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program is demonstration of OpenCV library.
Python implementation by: Nicolas TROTE
"""
import sys
import cv2.cv as cv
from optparse import OptionParser


# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size


min_size = (20, 20)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0


def detect_and_draw(img, cascade, mask):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)


    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)


    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)


    cv.EqualizeHist(small_img, small_img)


    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            for ((x, y, w, h), n) in faces:
                
                # Affichage du carré de recherche
                xmoustache = int((x * image_scale)+w * 0.5)
                ymoustache = int((y * image_scale)+ h * 1.25)
                wmoustache = int(w * 0.5 * image_scale)
                hmoustache = int(h * 0.19 * image_scale)
                img_mask = cv.CreateImage((wmoustache,hmoustache),mask.depth,mask.nChannels)
                cv.SetImageROI(img,(xmoustache, ymoustache, wmoustache ,hmoustache))
                cv.Resize(mask,img_mask,cv.CV_INTER_LINEAR)
                
                # Affichage du carré de recherche
                cv.Sub(img,img_mask,img)
                cv.ResetImageROI(img)
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                #cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)


    cv.ShowImage("result", img)


if __name__ == '__main__':


    parser = OptionParser(usage = "usage: %prog [options] [camera_index]")
    parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
    (options, args) = parser.parse_args()
    mask = cv.LoadImage("moustache-383-129.png")
    
    cascade = cv.Load(options.cascade)
    capture = cv.CreateCameraCapture(0)
    cv.NamedWindow("result", 1)


    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
            
            detect_and_draw(frame_copy, cascade, mask)            


            if cv.WaitKey(10) != -1:
                break


    cv.DestroyWindow("result")
