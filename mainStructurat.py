import utime
import machine

from lcd import init_lcd, lcd_print
from buzzer import canta_melodie
from servoMotor import misca_servo
from senzor import determinaDistanta
from conectToNetwork import connect_wifi, trimite_update, preia_comanda

verdeLed = machine.Pin(16, machine.Pin.OUT)
rosuLed = machine.Pin(22, machine.Pin.OUT)

usaDeschisa = False
mesaj_curent = ""

def afiseaza_mesaj(text):
    global mesaj_curent
    if mesaj_curent != text:
        init_lcd()
        lcd_print(text)
        mesaj_curent = text

def deschide_usa(dist):
    global usaDeschisa
    if not usaDeschisa:
        usaDeschisa = True
        rosuLed.off()
        verdeLed.on()
        misca_servo(0)
        afiseaza_mesaj("Bine ati venit! :)")
        canta_melodie()
        trimite_update(dist, "deschisa")

def inchide_usa(dist):
    global usaDeschisa
    if usaDeschisa:
        usaDeschisa = False
        misca_servo(90)
        verdeLed.off()
        rosuLed.on()
        afiseaza_mesaj("Usa inchisa!")
        trimite_update(dist, "inchisa")

def init_periferice():
    init_lcd()
    misca_servo(90)
    rosuLed.on()
    verdeLed.off()
    afiseaza_mesaj("Usa inchisa!")

def main_loop():
    global usaDeschisa
    while True:
        dist = determinaDistanta()
        if dist == -1:
            print("Eroare: semnal timeout la senzor")
            afiseaza_mesaj("Eroare senzor!")
            utime.sleep(1)
            continue

        print(f"Distanta: {dist:.2f} cm")

        comanda = preia_comanda()
        print(f"Comanda primita: {comanda}")

        if comanda == "deschide" and not usaDeschisa:
            deschide_usa(dist)
        elif comanda == "inchide" and usaDeschisa:
            inchide_usa(dist)
        else:
            # Comanda 'none' sau starea nu s-a schimbat, doar trimite update
            trimite_update(dist, "deschisa" if usaDeschisa else "inchisa")

        utime.sleep(0.3)

if __name__ == "__main__":
    connect_wifi()
    init_periferice()
    main_loop()
