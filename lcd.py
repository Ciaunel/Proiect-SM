import machine
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