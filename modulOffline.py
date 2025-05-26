import utime
import machine

from lcd import init_lcd, lcd_print
from buzzer import canta_melodie
from servoMotor import misca_servo
from senzor import determinaDistanta
from senzorTemperatura import masoaraTemperatura, masoaraUmiditate

verdeLed = machine.Pin(16, machine.Pin.OUT)
rosuLed = machine.Pin(22, machine.Pin.OUT)
mesaj_curent = ""


def afiseaza_mesaj(text):
    global mesaj_curent
    if mesaj_curent != text:
        init_lcd()
        lcd_print(text)
        mesaj_curent = text


def deschide_usa_offline():
    misca_servo(0)
    verdeLed.on()
    rosuLed.off()
    afiseaza_mesaj("Usa deschisa!")
    canta_melodie()
    utime.sleep(5)


def inchide_usa_offline():
    misca_servo(90)
    verdeLed.off()
    rosuLed.on()
    afiseaza_mesaj("Usa inchisa!")


def modOffline():
    while True:
        dist = determinaDistanta()
        temp = masoaraTemperatura()
        hum = masoaraUmiditate()
        if dist == -1:
            utime.sleep(1)
            continue

        print(f"Distanta: {dist:.2f} cm")
        print(f"Temperatura:{temp}C")
        print(f"Umiditatea:{hum}%")

        if temp is None or hum is None:
            utime.sleep(1)
            continue
        if (dist < 5):
            deschide_usa_offline()
        inchide_usa_offline()

