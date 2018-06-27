import os
import string
import sys
from tkinter import filedialog
from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QApplication, QMessageBox)
from PIL import Image, ImageOps, ImageStat, ImageEnhance, ImageFilter
from imutils import paths
import argparse
import cv2
import numpy
import scipy

class Example(QMainWindow):
    
    MED_BRIGHTNESS = 100.00

    def __init__(self):
        super().__init__()
        
        self.initUI()

    def calculate_brightness(self,image):
        grayscale = image.convert('L')
        stat = ImageStat.Stat(grayscale)
        return stat.mean[0]
    
    def blur_detection(self,image):
        return cv2.Laplacian(image, cv2.CV_64F).var()

    def initUI(self):

        file = QFileDialog.getOpenFileName(self,'choose file to import','')
        print(file)
        save = QFileDialog.getExistingDirectory(self,'choose save directory','')
        print(save)
        
        image = Image.open(file[0])
        image.save(save+"/original.png","png") #eventually change to dynamically select same type as import

        outName = "/test.txt"
        outFile = save+outName

        textOut = open(outFile,'w')

        textOut.write("test\n")
        textOut.write("Import path: "+file[0]+"\n")
        brightness = self.calculate_brightness(image)
        print(brightness)
        textOut.writelines("Import brightness: "+str(brightness)+"\n")

        to_blur = numpy.asarray(image)
        blurriness = self.blur_detection(to_blur)
        textOut.write("Import blurriness: "+str(blurriness)+"\n")        
        
        textOut.write("Before process compatibility: ")
        convert = image
        enhancer = ImageEnhance.Brightness(convert)

        if brightness >= Example.MED_BRIGHTNESS and brightness <= 150: #(ImgIn.getBrightness()>=50&&ImgIn.getBrightness()<=70)
            textOut.write("HIGH\n")
            textOut.write("-- preprocessing not needed --\n")
        elif brightness < Example.MED_BRIGHTNESS or brightness > 150 and brightness < 200: #(ImgIn.getBrightness()<50 || ImgIn.getBrightness()>70)
            textOut.write("LOW\n")
            if brightness < Example.MED_BRIGHTNESS:
                brightval = (150 - brightness)/brightness
                textOut.write("Brightness modifier: "+str(brightval)+"\n")
                convert = enhancer.enhance(brightval)
            else:
                brightval = 150/brightness
                textOut.write("Brightness modifier: "+str(brightval)+"\n")
                convert = enhancer.enhance(brightval)

        #im1 = im.filter(ImageFilter.SHARPEN)
        convert = convert.filter(ImageFilter.SHARPEN)

        convert.save(save+"/processed.png","png")

        textOut.write("Export brightness: "+str(self.calculate_brightness(convert))+"\n")
        conv_blur = numpy.asarray(convert)
        textOut.write("Export blurriness: "+str(self.blur_detection(conv_blur))+"\n")

        self.success_prompt()

        textOut.close
        sys.exit()

        #0x56525455414C

    def success_prompt(self):
    
        msg = QMessageBox()
        QMessageBox.question(self, 'Success', 'preprocess completed successfully', QMessageBox.Ok, QMessageBox.Ok)
        self.show()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())