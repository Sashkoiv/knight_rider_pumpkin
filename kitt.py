import time
import machine
import neopixel
import config
from hcsr04 import HCSR04


class KITT():
    def __init__(self):
        self.hcsr = HCSR04(config.PIN_HCRS_TRIG, config.PIN_HCRS_ECHO)
        self.np = neopixel.NeoPixel(machine.Pin(config.PIN_NP), config.DIODS_NUMBER)
        self.is_reversed = False
        self.is_killer_mode = False


    #TODO: implement killer mode eyes
    def draw_killer_eyes(self, ):
        for j in range(config.DIODS_NUMBER):
            self.np[j] = (0,16,0)
        if not self.is_reversed:
            pass
        else:
            pass


    def draw_marker(self, led_idx):
        #set field with BASE red color
        for i in range(config.DIODS_NUMBER):
            self.np[i] = (config.BASE, 0, 0)

        if not self.is_reversed:
            for i in range(config.MARKER_SIZE):
                color = int(config.BRIGHTEST  * (config.MARKER_SIZE - i) / config.MARKER_SIZE)
                self.np[led_idx-i] = (color, 0, 0)
        else:
            reversed_i = config.DIODS_NUMBER - 1 - led_idx
            for i in range(config.MARKER_SIZE):
                color = int(config.BRIGHTEST  * (config.MARKER_SIZE - i) / config.MARKER_SIZE)
                self.np[reversed_i+i] = (color, 0, 0)


    def run(self):
        while True:
            for i in range(config.MARKER_SIZE - 1, config.DIODS_NUMBER):
                if not self.is_killer_mode:
                    self.draw_marker(i)
                else: #TODO: add more features to killer mode (sound effects, physical actions etc.)
                    self.draw_killer_eyes()

                self.np.write()

                distance_to_hoe = self.hcsr.distance_cm()
                delay = config.IDLE_DELAY
                if distance_to_hoe <= config.KILLER_RANGE and distance_to_hoe >= 0:
                    self.is_killer_mode = True
                    delay = 1
                else:
                    self.is_killer_mode = False
                    if distance_to_hoe <= config.SAFE_RANGE and distance_to_hoe >= 0:
                       delay = int(config.IDLE_DELAY * distance_to_hoe / config.SAFE_RANGE)

                time.sleep_ms(delay)

            self.is_reversed = not self.is_reversed


    def stop(self):
        for i in range(config.DIODS_NUMBER):
            self.np[i] = (0, 0, 0)
        self.np.write()
