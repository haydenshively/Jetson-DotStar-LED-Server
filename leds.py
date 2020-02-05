import board
import adafruit_dotstar as dotstar

class LEDS:
    strip = None

    def __init__(self, brightness = 0.0):
        LEDS.deinit()
        LEDS.strip = dotstar.DotStar(board.SCK, board.MOSI, 144, brightness = brightness)
        self.r, self.g, self.b = (0.0, 0.0, 0.0)

    @classmethod
    def deinit(cls):
        if cls.strip is not None:
            cls.strip.deinit()

    def fill(self, r, g, b):
        self.r, self.g, self.b = (int(r), int(g), int(b))
        self.strip.fill((self.r, self.g, self.b))

    def duotone(self, rgb1, rgb2, segment_size=12):
        state = False
        for i in range(144):
            if i%segment_size is 0: state = not state
            rgb = rgb1 if state else rgb2
            self.strip[i] = [int(val) for val in rgb]

    def set_r(self, r):
        self.fill(r, self.g, self.b)

    def set_g(self, g):
        self.fill(self.r, g, self.b)

    def set_b(self, b):
        self.fill(self.r, self.g, b)

    def set_brightness(self, brightness):
        self.strip.brightness = brightness
