import socket
import ujson
import utime
import network
import machine

from lcd import init_lcd, lcd_print
from buzzer import canta_melodie
from servoMotor import misca_servo
from senzor import determinaDistanta
from senzorTemperatura import masoaraTemperatura, masoaraUmiditate

usaDeschisa = False
comanda = "none"
distanta = 0
temperatura = 0
umiditate = 0
mesaj_curent = ""

verdeLed = machine.Pin(16, machine.Pin.OUT)
rosuLed = machine.Pin(22, machine.Pin.OUT)

def afiseaza_mesaj(text):
    global mesaj_curent
    if mesaj_curent != text:
        init_lcd()
        lcd_print(text)
        mesaj_curent = text

def deschide_usa():
    global usaDeschisa
    if not usaDeschisa:
        usaDeschisa = True
        verdeLed.on()
        rosuLed.off()
        misca_servo(0)
        afiseaza_mesaj("Bine ati venit! :)")
        canta_melodie()

def inchide_usa():
    global usaDeschisa
    if usaDeschisa:
        usaDeschisa = False
        verdeLed.off()
        rosuLed.on()
        misca_servo(90)
        afiseaza_mesaj("Usa inchisa!")

def loadHTML():
    with open("templates/PicoServer.html","r") as f:
        return f.read()

def status_json():
    global distanta, temperatura, umiditate, comanda, usaDeschisa
    return ujson.dumps({
        "distanta": distanta,
        "status": "deschisa" if usaDeschisa else "inchisa",
        "temperatura": temperatura,
        "umiditate": umiditate,
        "comanda": comanda
    })

def start_server():
    global comanda, distanta, temperatura, umiditate
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    #ip=network.WLAN(network.STA_IF).ifconfig()[0]
    #print("Server pornit pe http://{}".format(ip))

    while True:
        cl, addr = s.accept()
        request = cl.recv(1024).decode()
        print("Request:", request)

        if "GET /status" in request:
            d = determinaDistanta()
            distanta = d if d != -1 else 0
            try:
                temperatura = masoaraTemperatura()
                umiditate = masoaraUmiditate()
            except:
                temperatura = 0
                umiditate = 0

            response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + status_json()
            cl.send(response.encode())

        elif "POST /comanda" in request:
            try:
                body = request.split("\r\n\r\n")[1]
                data = ujson.loads(body)
                comanda = data.get("act", "none")
                if comanda == "deschide":
                    deschide_usa()
                elif comanda == "inchide":
                    inchide_usa()
                resp = ujson.dumps({"status": "ok", "comanda": comanda})
                response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + resp
                cl.send(response.encode())
            except Exception as e:
                print("Eroare la parsarea POST:", e)
                cl.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())

        else:
            html = loadHTML()
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html
            cl.send(response.encode())

        cl.close()

