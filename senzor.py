import machine, utime

# --- HC-SR04 Setup ---
trig = machine.Pin(18, machine.Pin.OUT)
echo = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(25, machine.Pin.OUT)


def determinaDistanta(timeout_us=30000):
    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)

    start_wait = utime.ticks_us()
    while echo() == 0:
        if utime.ticks_diff(utime.ticks_us(), start_wait) > timeout_us:
            return -1

    start_t = utime.ticks_us()

    while echo() == 1:
        if utime.ticks_diff(utime.ticks_us(), start_t) > timeout_us:
            return -1
    stop_t = utime.ticks_us()
    durata = stop_t - start_t
    dist = durata * 342 / 2 / 10000
    return dist


