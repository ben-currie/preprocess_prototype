# preprocess_prototype

## preprocess_shell README

### -=REQUIREMENTS=-
================

The following python libraries must be installed to run this script:
- Python Image Library (or 'PIL')
- python imutils
- argparse
- computer vision 2 (or 'cv2')
- numpy and scipy

================

### -=EXECUTING=-

when running, preprocess_shell requires 2 parameters in order to execute:
1. execution flag

'-m' for manual/standard operation. This mode will accept an image and output processed variants of said image.

'-a' for automatic/demo mode. This mode is for TESTING PURPOSES ONLY and requires an image bank where all image files are titled using a specific syntax. For more information, see "running DEMO MODE".

2. Filepath
-if running in DEMO MODE, a directory is required in place of a specific file
(see "running DEMO MODE" for more details)

OPTIONALLY, a third argument can be used to specify a custom output path:

3. Outpath

'-o' to specify that a custom output path is given after the flag. If left uncalled, the outpath is in the filepath root folder by default.

================
### -=FUNCTIONS=-
the preprocess algorithm is comprised of several functions:

#### main()
instantiates the available command line arguments and sets up inevitable cases for their use (whether manual or auto/demo mode is selected, if an outpath is given)

#### preprocess(switch,filepath,outpath)
arguments:
- switch (boolean) dictates whether the preprocess suite is running manual or demo mode
- filepath (string) is where an input path is passed in
- outpath (string) is passed an empty string if no output path is specified

**MED_BRIGHTNESS** is used to control the threshold with which the median brightness of a given filepath image is compared against. This value can be changed to make the algorithm for brightness adjustment more or less sensitive (bigger adjustments in brightness). The default value is 160.00

The preprocess function creates an output folder based on input (whether or not an outpath is provided) and analyzes images using the other included functions.

#### calculate_brightness(image)


#### blur_detection(image)
