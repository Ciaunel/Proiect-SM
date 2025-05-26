import utime
import machine

from lcd import init_lcd, lcd_print
from buzzer import canta_melodie
from servoMotor import misca_servo
from senzor import determinaDistanta
from conectToNetwork import connect_wifi
from senzorTemperatura import masoaraTemperatura, masoaraUmiditate
import server as s
from modulOffline import modOffline, afiseaza_mesaj

verdeLed = machine.Pin(16, machine.Pin.OUT)
rosuLed = machine.Pin(22, machine.Pin.OUT)


def init_periferice():
    init_lcd()
    misca_servo(90)
    rosuLed.on()
    verdeLed.off()

if __name__ == "__main__":
    init_periferice()
    if (connect_wifi()):
        s.start_server()
    else:
        afiseaza_mesaj("Usa inchisa!")
        modOffline()

