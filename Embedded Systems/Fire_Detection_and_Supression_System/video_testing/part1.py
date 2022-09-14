from math import ceil
import requests
import cv2
import serial
import numpy as np


class FireDetection:
#value initialization label
    def __init__(self):
        self.subtractBackground = cv2.createBackgroundSubtractorMOG2(varThreshold=170, detectShadows=False)
       # self.sendSerial = serial.Serial('COM9', 9600)
        o_kern = ceil(3)
        c_kern = ceil(30)
        self.openKernel = np.ones((o_kern, o_kern), np.uint8)
        self.closeKernel = np.ones((c_kern, c_kern), np.uint8)
        self.xCentroid = None
        self.yCentroid = None
        self.prevRatio = None
        self.currRatio = None
        self.prevHist = None
        self.currHist = None
        self.prevVar = None
        self.currVar = None
        self.history = []
        self.countFireFrames = 0
        self.totalFrame = 0
        self.prevNoOfPixels = 1
        self.histogram_flag = False
        self.variance_flag = False

    def volume_analysis(self, threshold_image):
        gamma = 0.05
        flag = False
        no_of_pixels = cv2.compare(threshold_image, 0, cv2.CMP_GT).sum() / 255
        if self.prevNoOfPixels is not None:
            if abs(self.prevNoOfPixels - no_of_pixels) / self.prevNoOfPixels > gamma:
                flag = True
        self.prevNoOfPixels = no_of_pixels
        return flag

    def dimension_analysis(self, width, height):
        gamma = 0.1
        flag = False
        self.currRatio = width / height
        if self.prevRatio is not None:
            if abs(self.prevRatio - self.currRatio) > gamma:
                flag = True
        self.prevRatio = self.currRatio
        return flag

    def background_subtraction(self, capture_image):
        mask = self.subtractBackground.apply(capture_image)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.openKernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, self.closeKernel)
        
        threshold = cv2.medianBlur(closing, 5)
        foreground = cv2.bitwise_and(capture_image, cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR))
        return threshold, foreground

    def color_analysis_org(self, capture_image, threshold_image):
        div = 240
        mul = 1.3
        img_ycrcb = cv2.cvtColor(capture_image, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(img_ycrcb)
        
        y_mean = img_ycrcb[0].mean()*mul
        cr_mean = cr.mean()
        cb_mean = cb.mean()
        
        cr_mean = cr_mean if cr_mean > 150 else 150
        print("cr_mean", cr_mean)
        cb_mean = 120 if cb_mean > 120 else cb_mean
        print("cb_mean", cb_mean)
        if cb_mean == 120:
            print("No Fire Detected")
        else:
            print("Fire Detected")
        
        
        _, y_mat = cv2.threshold(y, div, 255, cv2.THRESH_TOZERO_INV)
        _, y_mat = cv2.threshold(y_mat, y_mean, 255, cv2.THRESH_TOZERO)
        
        y_mat = cv2.compare(y_mat, cb, cv2.CMP_GT)
        cr_mat = cv2.compare(cr, cb, cv2.CMP_GT)
        cb_mat = cv2.compare(cb, cb_mean, cv2.CMP_LT)
        
        light_fire = cv2.bitwise_and(y_mat, cr_mat)
        light_fire = cv2.bitwise_and(light_fire, cb_mat)
        
        y_mean = y_mean if div < y_mean else div
        
        y_mat = cv2.compare(y, y_mean, cv2.CMP_GT)
        cr_mat = cv2.compare(cr, cb, cv2.CMP_GT)
        
        heavy_fire = cv2.bitwise_and(y_mat, cr_mat)
        fire = cv2.bitwise_or(light_fire, heavy_fire)
        fire = cv2.bitwise_and(fire, threshold_image)
        
        opening = cv2.morphologyEx(fire, cv2.MORPH_OPEN, self.openKernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, self.closeKernel)
        
        closing = cv2.medianBlur(closing, 5)
        return_img = cv2.bitwise_and(capture_image, cv2.cvtColor(closing, cv2.COLOR_GRAY2BGR))
        
        return return_img



#main part
if __name__ == '__main__':
    Fire = FireDetection()
    #url = "http://192.168.0.100:8080/shot.jpg"
    cap = cv2.VideoCapture('C:\\Users\\nilen\\OneDrive\\Desktop\\JUproject\\FireDetection1\\test video\\min.mp4')
    #cap = cv2.VideoCapture(0)
    length = 406
    breadth = 720
    m = length / 2
    n = breadth / 2
    int_m = int(m)
    int_n = int(n)
    while True:
        grabbed, imBGR = cap.read()
        if not grabbed:
            break
        factor = 2
        zone1 = cv2.rectangle(imBGR,(0,0),(int_m,int_n),(0,0,255),3) # Quad 1 red
        zone2 = cv2.rectangle(imBGR,(0,int_n),(int_m,breadth),(0,255,255),3) # Quad 2 yellow
        zone3 = cv2.rectangle(imBGR,(int_m,0),(length,int_n),(255,255,255),3) # Quad 3 white
        zone4 = cv2.rectangle(imBGR,(int_m,int_n),(length,breadth),(255,255,0),3) # Quad 4 blue
        #imBGR = cv2.resize(imBGR, (ceil(imBGR.shape[1] / factor), ceil(imBGR.shape[0] / factor)))
        thresholdImage, foregroundImage = Fire.background_subtraction(imBGR)
        firePixelImage = Fire.color_analysis_org(imBGR, thresholdImage)
        print("Fresh Analysis")
        cv2.imshow('color_segment', firePixelImage)
        #fireBlob = Fire.fire_blob_detection(imBGR, firePixelImage, thresholdImage)
        #cv2.imshow('OUTPUT', fireBlob)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
