import network
import socket
from lcd import lcd_print, init_lcd
import urequests
import time

Server = "http://192.168.218.1:80"

def connect_wifi(timeout=15):
    # setari pentru wifi
    # conexiune by default
    ssid = 'madalinaHotspot'
    password = 'm9adalina2003'

    # ssidInput=input('Introduceti numele retelei: ')
    # passwordInput=input('Introduceti parola retelei la care va conectati:')

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # wlan.connect(ssidInput,passwordInput)
    wlan.connect(ssid, password)
    init_lcd()
    lcd_print("Se conecteaza...")

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            lcd_print("Timeout conexiune")
            print("Nu s-a putut conecta la Wi-Fi")
            return False
        time.sleep(0.5)

    ip = wlan.ifconfig()[0]
    print(f'Conectat. IP: {ip}')
    init_lcd()
    lcd_print("S-a conectat!")
    return True



