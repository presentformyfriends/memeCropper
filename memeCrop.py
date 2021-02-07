#! python 3

import os, sys, pyautogui
from PIL import Image, ImageChops

def blkSidesCrop(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def instaCrop(im):
    file = im
    filename = os.path.splitext(file)[0]
    ext = os.path.splitext(file)[1]
    # Convert PNG to RGB, open JPG as is, if any other file extension then exit
    if ext.lower() == '.png':
        im = Image.open(file).convert('RGB')
    elif ext.lower() == '.jpg':
        im = Image.open(file)
    else:
        print('Invalid file extension')
        sys.exit()
    # Assign width and height to im.size tuple, assign topGreyLine and bottomWhiteLine
    width, height = im.size
    topGreyLine = 0
    bottomWhiteLine = height
    # Start at top of photo and search top half of photo for horizontal grey line
    # Conditions are 168 OR 179 or 219 RGB value AND 5 pixels down from line = 255 (white)
    for y in range(0, height//2):
        if im.getpixel((width//2, y+1)) == (255, 255, 255) and (im.getpixel((width//2, y)) == (168, 168, 168) or im.getpixel((1, y)) == (179, 179, 179) or im.getpixel((1, y)) == (219, 219, 219)):
            topGreyLine = y
            print("Top grey line on Y-axis at {}".format(topGreyLine))
            break
    # Start from dead center of photo and search bottom half of photo for horizontal white line (255 RGB value)
    for y in range((height//2)-1, height):
        if im.getpixel(((width//2), y)) == (255, 255, 255):
            bottomWhiteLine = y
            print("Bottom white line on Y-axis at {}".format(bottomWhiteLine))
            break
    # Mititgate for if top grey line or bottom white line not found   
    if topGreyLine == 0:
        print("Top grey line not found on Y-axis")
    elif bottomWhiteLine == height:
        print("Bottom white line not found on Y-axis")
    # Crop image, set cutoff to top grey line and bottom white line            
    left = 0
    top = topGreyLine
    right = width
    bottom = bottomWhiteLine
    imCrop = im.crop((left, top, right, bottom))
    # Search for black side bars and pass to blkSidesCrop function if necessary
    for y in range(0, bottom//2):
        if imCrop.getpixel((1, y)) == (0, 0, 0) and imCrop.getpixel(((right-1), y)) == (0, 0, 0):
            imCrop = blkSidesCrop(imCrop)
            break
##    imCrop.show() # Uncomment this line if you want, but I find ".show" is buggy on Windows 10, only shows half the image
    # Save file with new filename
    imCrop.save(os.path.join(filename + "_CROPPED" + ext))    


### MAIN ###

# Assign right-clicked file as image # Must run registry script first for this to work!
selection = (str(sys.argv[1]))

if os.path.isfile(selection):
    im = os.path.basename(selection)
    instaCrop(im)
else:
    pyautogui.alert('Please select files only')
    sys.exit()

### CROP SINGLE IMAGE
##instaCrop("IMG.png")

### BATCH CROP
### Define working directory
##os.chdir(r"PATH")
##imgs = next(os.walk(os.getcwd()))[2]
##for im in imgs:
##    print(im)
##    instaCrop(im)
