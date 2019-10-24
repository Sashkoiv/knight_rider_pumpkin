import time
import machine
import neopixel

def demo(np):
    n = np.n
    colors = [
        (255, 0,   0),
        (255, 255, 0),
        (0,   255, 0),
        (0,   255, 255),
        (0,   0,   255),
        (255, 0,   255),
        (255, 255, 255),
    ]
    # knight rider mode
    for color in colors:
        for i in range(2 * n):
            for j in range(n):
                np[j] = (0, 0, 0)
            if (i // n) % 2 == 0:
                np[i % n] = color
            else:
                np[n - 1 - (i % n)] = color
            np.write()
            time.sleep_ms(20)


    # # cycle
    # for i in range(4 * n):
    #     for j in range(n):
    #         np[j] = (0, 0, 0)
    #     np[i % n] = (255, 255, 255)
    #     np.write()
    #     time.sleep_ms(25)

    # # bounce
    # for i in range(4 * n):
    #     for j in range(n):
    #         np[j] = (0, 0, 128)
    #     if (i // n) % 2 == 0:
    #         np[i % n] = (0, 0, 0)
    #     else:
    #         np[n - 1 - (i % n)] = (0, 0, 0)
    #     np.write()
    #     time.sleep_ms(60)

    # # fade in/out
    # for i in range(0, 4 * 256, 8):
    #     for j in range(n):
    #         if (i // 256) % 2 == 0:
    #             val = i & 0xff
    #         else:
    #             val = 255 - (i & 0xff)
    #         np[j] = (val, 0, 0)
    #     np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

def showtime(qty = 24, pin = 12):
    np = neopixel.NeoPixel(machine.Pin(pin), qty)
    demo(np)

def run(self):
    print('executing')
    showtime()

button_showtime = machine.Pin(0, machine.Pin.IN)
button_showtime.irq(trigger=machine.Pin.IRQ_FALLING, handler=run)
