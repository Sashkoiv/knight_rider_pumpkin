import machine

from kitt import KITT

def run():
    print('executing')
    kitt_pimpkin = KITT()
    try:
        kitt_pimpkin.run()
    except KeyboardInterrupt:
        kitt_pimpkin.stop()


button_showtime = machine.Pin(0, machine.Pin.IN)
button_showtime.irq(trigger=machine.Pin.IRQ_FALLING, handler=run)
