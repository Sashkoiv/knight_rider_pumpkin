import time
import machine
import neopixel
import config
from dfplayer import Player
from hcsr04 import HCSR04


class KITT():
    def __init__(self):
        self.hcsr = HCSR04(config.PIN_HCRS_TRIG, config.PIN_HCRS_ECHO)
        self.eyes_led = neopixel.NeoPixel(machine.Pin(config.PIN_EYES),
                                          config.EYES_DIODS_NUMBER)
        self.maw_led = neopixel.NeoPixel(machine.Pin(config.PIN_MAW),
                                         config.MAW_DIODS_NUMBER)
        self.player = Player(busy_pin=machine.Pin(config.PIN_AUDIO_BUSY))
        self.is_reversed = False
        self.is_killer_mode = False


    #TODO: implement killer mode eyes
    def draw_killer_eyes(self, ):
        for j in range(config.EYES_DIODS_NUMBER):
            self.eyes_led[j] = (0,16,0)
        if not self.is_reversed:
            pass
        else:
            pass


    def draw_marker(self, led_idx):
        #set field with BASE red color
        for i in range(config.EYES_DIODS_NUMBER):
            self.eyes_led[i] = (config.BASE, 0, 0)

        if not self.is_reversed:
            for i in range(config.MARKER_SIZE):
                color = int(config.BRIGHTEST  * (config.MARKER_SIZE - i) / config.MARKER_SIZE)
                self.eyes_led[led_idx-i] = (color, 0, 0)
        else:
            reversed_i = config.EYES_DIODS_NUMBER - 1 - led_idx
            for i in range(config.MARKER_SIZE):
                color = int(config.BRIGHTEST  * (config.MARKER_SIZE - i) / config.MARKER_SIZE)
                self.eyes_led[reversed_i+i] = (color, 0, 0)


    def draw_maw(self, led_idx):
        for i in range(config.MAW_DIODS_NUMBER):
            if not self.is_reversed:
                color = int(config.BRIGHTEST  * led_idx / config.EYES_DIODS_NUMBER)
            else:
                reversed_i = config.EYES_DIODS_NUMBER - led_idx
                color = int(config.BRIGHTEST  * reversed_i / config.EYES_DIODS_NUMBER)
            self.maw_led[i] = (color, 0, 0)


    def run(self):
        while True:
            for i in range(config.MARKER_SIZE - 1, config.EYES_DIODS_NUMBER):
                if not self.is_killer_mode:
                    self.draw_marker(i)
                else: #TODO: add more features to killer mode (sound effects, physical actions etc.)
                    self.draw_killer_eyes()
                
                self.draw_maw(i)

                self.eyes_led.write()
                self.maw_led.write()

                distance_to_hoe = self.hcsr.distance_cm()
                delay = config.IDLE_DELAY
                if distance_to_hoe <= config.KILLER_RANGE and distance_to_hoe >= 0:
                    self.player.play(1, config.TAUNT)
                    self.is_killer_mode = True
                    delay = 1
                else:
                    self.is_killer_mode = False
                    if distance_to_hoe <= config.SAFE_RANGE and distance_to_hoe >= 0:
                        self.player.play(1, config.GUARD_DOG)
                        delay = int(config.IDLE_DELAY * distance_to_hoe / config.SAFE_RANGE)

                time.sleep_ms(delay)

            self.is_reversed = not self.is_reversed


    def stop(self):
        for i in range(config.EYES_DIODS_NUMBER):
            self.eyes_led[i] = (0, 0, 0)

        for i in range(config.MAW_DIODS_NUMBER):
            self.maw_led[i] = (0, 0, 0)

        self.eyes_led.write()
        self.maw_led.write()

        