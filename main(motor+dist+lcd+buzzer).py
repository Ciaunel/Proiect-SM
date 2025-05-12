import machine
import utime
from time import sleep

# --- LCD Setup ---
RS = machine.Pin(2, machine.Pin.OUT)
E = machine.Pin(3, machine.Pin.OUT)
D4 = machine.Pin(4, machine.Pin.OUT)
D5 = machine.Pin(5, machine.Pin.OUT)
D6 = machine.Pin(6, machine.Pin.OUT)
D7 = machine.Pin(7, machine.Pin.OUT)

def send_nibble(n):
    D4.value((n >> 0) & 1)
    D5.value((n >> 1) & 1)
    D6.value((n >> 2) & 1)
    D7.value((n >> 3) & 1)
    E.value(1)
    sleep(0.001)
    E.value(0)
    sleep(0.001)

def send_byte(value, is_data):
    RS.value(is_data)
    send_nibble(value >> 4)
    send_nibble(value & 0x0F)
    sleep(0.001)

def init_lcd():
    sleep(0.05)
    RS.value(0)
    for _ in range(3):
        send_nibble(0x03)
        sleep(0.005)
    send_nibble(0x02)
    send_byte(0x28, 0)  # 4-bit, 2 lines
    send_byte(0x0C, 0)  # display ON, cursor OFF
    send_byte(0x06, 0)  # cursor move right
    send_byte(0x01, 0)  # clear screen
    sleep(0.01)

def lcd_print(text):
    for char in text:
        send_byte(ord(char), 1)

# --- HC-SR04 Setup ---
trig = machine.Pin(18, machine.Pin.OUT)
echo = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(25, machine.Pin.OUT)

# --- Servo motor Setup ---
servo = machine.PWM(machine.Pin(15))
servo.freq(50)

def misca_servo(unghi):
    duty = int(1638 + (unghi / 180) * (8192 - 1638))
    servo.duty_u16(duty)

# --- Buzzer Setup (Pin GPIO14) ---
buzzer = machine.PWM(machine.Pin(14))  # Pin 14 (GP14)

# Melodie pentru buzzer (frecvențele în Hz și durata notelor în secunde)
melodie = [
    (262, 0.3),  # Do
    (294, 0.3),  # Re
    (330, 0.3),  # Mi
    (349, 0.3),  # Fa
    (392, 0.3),  # Sol
    (330, 0.3),  # Mi
    (294, 0.3),  # Re
    (262, 0.3),  # Do
    (0, 0.2),    # Pauză
    (440, 0.3),  # La
    (494, 0.3),  # Si
    (262, 0.3),  # Do
    (262, 0.3),  # Do (repetare finală)
]

def canta_melodie():
    for frecventa, durata in melodie:
        buzzer.freq(frecventa)
        buzzer.duty_u16(32768)  # Apasă buzzer-ul la 50% din intensitate
        utime.sleep(durata)
        buzzer.duty_u16(0)  # Oprește buzzer-ul între note

# --- Initializare ---
init_lcd()
trig.value(0)
led.value(0)
misca_servo(90)  # pozitia initiala (fata)

while True:
    trig.value(1)
    utime.sleep(0.00001)
    trig.value(0)

    while echo() == 0:
        start_t = utime.ticks_us()
    while echo() == 1:
        stop_t = utime.ticks_us()

    durata = stop_t - start_t
    dist = durata * 342 / 2 / 10000  # în cm

    print(f"Distanta: {dist:.2f} cm")
    if dist < 5:
        print("Distanta mai mica de 5 cm, misca servo")
        led.value(1)
        misca_servo(0)  # rotire la stânga
        send_byte(0x01, 0)  # clear LCD
        lcd_print("Bine ati venit!")
        canta_melodie()  # Buzzer cântă melodie
        utime.sleep(5)
        misca_servo(90)  # revine la poziția inițială
        send_byte(0x01, 0)  # clear LCD


    utime.sleep(0.4)
