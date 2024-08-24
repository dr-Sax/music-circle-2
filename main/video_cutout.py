from math import sin, cos, pi, trunc
import numpy as np
import cv2
from shapely.geometry import Polygon
from moviepy.editor import *

FILEPATH = "media/dreams_that_money_can_buy.mp4"

def get_subclip(filepath, t_start, t_end):
    t_start_secs = t_start[0] * 60 + t_start[1] 
    t_end_secs = t_end[0] * 60 + t_end[1] 
    clip = VideoFileClip(filepath)
    clip = clip.subclip(t_start_secs, t_end_secs)


def get_perimeter_coords(img_file):
    image = cv2.imread(img_file, cv2.IMREAD_UNCHANGED) 
    
    if image.shape[2] == 4:
        print("Image has an alpha channel") 
    else:
        print('none')

    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    # alpha = np.full((image.shape[0],image.shape[1]), 255, dtype=np.uint8)
    # alpha_image = np.dstack((image, alpha))  # dstack still didn't work...

    if image.shape[2] == 4:
        print("Image has an alpha channel") 
    else:
        print('none')



    edged = cv2.Canny(image, 30, 10) 


    canvas = np.zeros(image.shape, np.uint8)
    canvas.fill(255)

    

    contours_draw, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(canvas, contours_draw, -1, (0, 0, 0), 3)
    #image[:, :, 2] = cv2.bitwise_and(image, canvas)
    cv2.imshow('img', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

count = 199
get_perimeter_coords(f"media/mannequinn_frames/{count}.png")

# ts_min = 24
# ts_sec = 0

# te_min = 24
# te_sec = 8
# get_subclip(FILEPATH, [ts_min, ts_sec], [te_min, te_sec])