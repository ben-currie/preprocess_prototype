import sys
import os
import string
from PIL import Image, ImageOps, ImageStat, ImageEnhance, ImageFilter, ImageChops
from imutils import paths
import argparse
import cv2
import numpy as np
import scipy 

def main():

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-m", "--manual", help="Help description of this flag")
    parser.add_argument("-a", "--auto", help="auto mode/demo mode")
    parser.add_argument("-o", "--output", help="Tester")

    argument = parser.parse_args()

    if argument.output:
        outpath = argument.output
    else:
        outpath = ""

    if argument.manual and argument.auto:
        print("cannot run both manual and auto modes simultaneously. please select only one when executing.")
        return
    if argument.manual: #manual operation mode - for processing a file passed in at the end of the line
        print("manual operation mode")
        preprocess(False,argument.manual,outpath)
    elif argument.auto: #automatic/demo operation mode - checks given path and picks a random demo file to process
        print("auto/demo mode")
        preprocess(True,argument.auto,outpath)

def preprocess(switch,filepath,outpath):

    MED_BRIGHTNESS = 160.00
    empty = ""
    if outpath == empty:
        save = str(os.path.dirname(filepath)) #get root of current file and make a test output folder there
        save = os.path.abspath(os.path.join(filepath,os.pardir))
        #print(save)
        #print (os.path.abspath(os.path.join(save, os.pardir)))
        s_folder = save + "/preprocess_output"
    else:
        s_folder = outpath

    if not os.path.exists(s_folder): #if the outpath directory doesn't already exist, then it will be created
        os.makedirs(s_folder,0o777)

    if switch is True: #if demo mode is selected
        random = np.random.random_integers(1,2432,1)
        print(random[0])
        randomPath = filepath+"/"+"eClaim_"+str(random[0])+".jpg"
        image = Image.open(randomPath)
        image.save(s_folder+"/original.png","png")
        filepath = randomPath
    elif switch is False: #if manual mode is selected
        image = Image.open(filepath)
        image.save(s_folder+"/original.png","png")
    
    outName = "/evaluation.txt"
    outFile = s_folder+outName

    textOut = open(outFile,'w')

    textOut.write("test\n")
    textOut.write("Import path: "+s_folder+"\n")
    brightness = calculate_brightness(image)
    print(brightness)
    textOut.writelines("Import brightness: "+str(brightness)+"\n")

    to_blur = np.asarray(image)
    blurriness = blur_detection(to_blur)
    textOut.write("Import blurriness: "+str(blurriness)+"\n")        
        
    textOut.write("Before process compatibility: ")
    convert = image
    enhancer = ImageEnhance.Brightness(convert)
    convert = ImageOps.autocontrast(convert)

    if brightness >= MED_BRIGHTNESS and brightness <= 170:
        textOut.write("HIGH\n")
        textOut.write("-- preprocessing not needed --\n")
    elif brightness < MED_BRIGHTNESS or brightness > 170 and brightness < 200:
        textOut.write("LOW\n")
        if brightness < MED_BRIGHTNESS:
            brightval = (170 - brightness)/brightness
            textOut.write("Brightness modifier: "+str(brightval)+"\n")
            convert = enhancer.enhance(brightval)
        else:
            brightval = 170/brightness
            textOut.write("Brightness modifier: "+str(brightval)+"\n")
            convert = enhancer.enhance(brightval)

    convert = convert.filter(ImageFilter.SHARPEN)

    convert.save(s_folder+"/processed.png","png")

    textOut.write("Export brightness: "+str(calculate_brightness(convert))+"\n")
    conv_blur = np.asarray(convert)
    textOut.write("Export blurriness: "+str(blur_detection(conv_blur))+"\n")

    binarize = convert
    gray = binarize.convert('L')

    # Let numpy do the heavy lifting for converting pixels to pure black or white
    bw = np.asarray(gray).copy()

    # Pixel range is 0...255, 256/2 = 128
    bw[bw < 126] = 0    # Black
    bw[bw >= 130] = 255 # White

    # numpy array is then converted back into an image and saved as "binarized.png"
    imfile = Image.fromarray(bw)
    imfile.save(s_folder+"/binarized.png")

    #Band isolators save each color band as a separate file      
    r = image
    r = np.array(r)
    r[:,:,1] *=0
    r[:,:,2] *=0
    r = Image.fromarray(r)
    r.save(s_folder+"/red.png")

    g = image
    g = np.array(g)
    g[:,:,0] *=0
    g[:,:,2] *=0
    g = Image.fromarray(g)
    g.save(s_folder+"/green.png")

    b = image
    b = np.array(b)
    b[:,:,0] *=0
    b[:,:,1] *=0
    b = Image.fromarray(b)
    b.save(s_folder+"/blue.png")

    c = image
    c = np.array(c)
    c[:,:,0] *=0
    c = Image.fromarray(c)
    c.save(s_folder+"/cyan.png")

    m = image
    m = np.array(m)
    m[:,:,1] *=0
    m = Image.fromarray(m)
    m.save(s_folder+"/magenta.png")

    y = image
    y = np.array(y)
    y[:,:,2] *=0
    y = Image.fromarray(y)
    y.save(s_folder+"/yellow.png")

    #scan for pure black or white image here:
    textOut.write("Binarization and/or preprocess status:")
    if not imfile.getbbox() or not ImageChops.invert(imfile).getbbox():
        textOut.write("FAIL"+"\n") #Image has failed scan if image is completely black or white
    else:
        textOut.write("PASS"+"\n")

    textOut.close

#helper methods go here
def calculate_brightness(image):
    grayscale = image.convert('L')
    stat = ImageStat.Stat(grayscale)
    return stat.mean[0]

def blur_detection(image): #blur is detected by way of a computer vision laplacian kernel run across the entirety of the image and is represented by an int value. The closer the value is to 0, the blurrier the image is
    return cv2.Laplacian(image, cv2.CV_64F).var()

if __name__ == '__main__':
    main()
    