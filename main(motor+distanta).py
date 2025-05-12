import machine
import utime

# HC-SR04
trig = machine.Pin(18, machine.Pin.OUT)
echo = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(25, machine.Pin.OUT)

# Servo motor pe pinul 15 (GP15)
servo = machine.PWM(machine.Pin(15))
servo.freq(50)  # frecvență PWM tipică pentru servo

def misca_servo(unghi):
    # conversie unghi în duty pentru semnal PWM la 50Hz
    duty = int(1638 + (unghi / 180) * (8192 - 1638))  # interval 0.5ms - 2.5ms
    servo.duty_u16(duty)

# Initializare
trig.value(0)
led.value(0)
misca_servo(90)  # pozitia initiala (fata)

while True:
    # Trimite semnal de trigger
    trig.value(1)
    utime.sleep(0.00001)
    trig.value(0)

    while echo() == 0:
        start_t = utime.ticks_us()
    while echo() == 1:
        stop_t = utime.ticks_us()

    durata = stop_t - start_t
    dist = durata * 342 / 2 / 10000  # în cm

    print("%.2f" % dist, "cm")

    if dist < 5:
        led.value(1)
        misca_servo(0)  # rotire la stânga cu 90° (0° față de poziția inițială)
        utime.sleep(5)
        misca_servo(90)  # revine la poziția inițială
    elif dist < 10:
        led.value(1)
    else:
        led.value(0)

    utime.sleep(0.4)
