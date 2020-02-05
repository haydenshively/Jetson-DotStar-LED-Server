import math
import requests
from datetime import datetime
from dateutil import tz

class Sun:

    LA_LAT = '34.066710'
    LA_LONG = '-118.284330'
    LA_ZONE = tz.gettz('America/Los_Angeles')

    def __init__(self, latitude = None, longitude = None, tz = None):
        if latitude is None: latitude = LA_LAT
        if longitude is None: longitude = LA_LONG
        if tz is None: tz = LA_ZONE

        self.api_link = 'https://api.sunrise-sunset.org/json?lat=' + latitude + '&lng=' + longitude + '&date=today'
        self.tz = tz

    @property
    def api_json(self):
        return requests.get(self.api_link).json()

    @property
    def sunrise_time_utc(self):
        return self.api_json['results']['sunrise']

    @property
    def sunset_time_utc(self):
        return self.api_json['results']['sunset']

    @property
    def time_utc(self):
        time = datetime.now()
        time = time.replace(tzinfo = self.tz)
        return time.astimezone(tz.gettz('UTC'))

    @property
    def time_utc_name(self):
        time = self.time_utc
        h = time.hour
        suffix = ' AM' if h < 12 else ' PM'
        m = time.minute
        m = '0{}'.format(m) if m < 10 else m
        s = time.second
        s = '0{}'.format(s) if s < 10 else s
        return '{}:{}:{}'.format(h, m, s) + suffix

    def is_it_sunrise(self):
        time = self.time_utc_name
        sunrise = self.sunrise_time_utc
        return (time[:5] == sunrise[:5]) and (time[-2:] == sunrise[-2:])

    def is_it_sunset(self):
        time = self.time_utc_name
        sunset = self.sunset_time_utc
        return (time[:5] == sunset[:5]) and (time[-2:] == sunset[-2:])

    @staticmethod
    def kelvin_to_rgb(temperature):
        """
        Converts from K to RGB
        http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
        """
        temperature = max(min(temperature, 40000), 1000)/100.0

        #red
        if temperature <= 66:
            red = 255
        else:
            red = 329.698727446*math.pow(temperature - 60, -0.1332047592)
            red = max(min(red, 255), 0)

        #green
        green = 99.4708025861*math.log(temperature) - 161.1195681661 if temperature <= 66 else 288.1221695283*math.pow(temperature - 60, -0.0755148492)
        green = max(min(green, 255), 0)

        #blue
        if temperature >= 66:
            blue = 255
        elif temperature <= 19:
            blue = 0
        else:
            blue = 138.5177312231*math.log(temperature - 10) - 305.0447927307
            blue = max(min(blue, 255), 0)

        return red, green, blue
