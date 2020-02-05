import requests
from datetime import datetime
from dateutil import tz

import os.path
if os.path.exists('running.txt'):
    exit()

response = requests.get('https://api.sunrise-sunset.org/json?lat=34.066710&lng=-118.284330&date=today')

sunrise = response.json()['results']['sunrise']

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/Los_Angeles')


time = datetime.now()
time = time.replace(tzinfo = to_zone)
time = time.astimezone(from_zone)
h = time.hour
suffix = ' AM' if h < 12 else ' PM'
m = time.minute
m = '0{}'.format(m) if m < 10 else m
s = time.second
s = '0{}'.format(s) if s < 10 else s
time = '{}:{}:{}'.format(h, m, s) + suffix

print("It's currently {} and sunrise is at {}".format(time, sunrise))
if time != sunrise:
    exit()

open('running.txt', 'a').close()

import os
os.system('xset -display :0.0 dpms force on')

import cv2
import numpy as np
from time import time
import math

def kelvin_to_rgb(temp):
    """
    Converts from K to RGB, algorithm courtesy of
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    temp = max(min(temp, 40000), 1000)/100.0

    # red
    if temp <= 66:
        red = 255
    else:
        red = 329.698727446*math.pow(temp - 60, -0.1332047592)
        red = max(min(red, 255), 0)

    # green
    if temp <= 66:
        green = 99.4708025861*math.log(temp) - 161.1195681661
    else:
        green = 288.1221695283*math.pow(temp - 60, -0.0755148492)
    green = max(min(green, 255), 0)

    # blue
    if temp >= 66:
        blue = 255
    elif temp <= 19:
        blue = 0
    else:
        blue = 138.5177312231*math.log(temp - 10) - 305.0447927307
        blue = max(min(blue, 255), 0)

    return red, green, blue


cv2.namedWindow("Hue", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Hue", cv2.WND_PROP_FULLSCREEN, 1)


duration = 30# minutes
start = time()
elapsed = time() - start

while elapsed < duration*60.0:
    progress = elapsed/(duration*60.0)
    temperature = 1700 + progress*(15000 - 1700)

    r,g,b = kelvin_to_rgb(temperature)
    solid_color = np.full((1080, 1920, 3), np.array([b, g, r]), dtype = 'uint8')

    cv2.imshow("Hue", solid_color)
    cv2.waitKey(1)

    elapsed = time() - start

cv2.destroyAllWindows()
os.system('xset -display :0.0 dpms force off')

os.remove('running.txt')
