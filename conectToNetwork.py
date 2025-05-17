import network
import socket
from lcd import lcd_print, init_lcd
import urequests

Server="http://192.168.249.1:8000"

def connect_wifi():
#setari pentru wifi
#conexiune by default
        ssid='madalinaHotspot'
        password='m9adalina2003'

#daca vrem sa ne conectam la reteaua proprie
        #ssidInput=input('Introduceti numele retelei: ')
        #passwordInput=input('Introduceti parola retelei la care va conectati:')

        wlan=network.WLAN(network.STA_IF)
        wlan.active(True)

        #wlan.connect(ssidInput,passwordInput)
        wlan.connect(ssid,password)
        init_lcd()
        lcd_print("Se conecteaza...")
        while not wlan.isconnected():
                pass

        ip=wlan.ifconfig()[0]
        print(f'Conectat. IP: {ip}')
        init_lcd()
        lcd_print("S-a conectat la WiFi!")

def trimite_update(distanta,status):
        try:
                r=urequests.post(Server +"/update",json={"distanta" : round(distanta,2), "status":status})
                r.close()
        except Exception as e:
                print("Eroare POST:", e)

def preia_comanda():
        try:
                r=urequests.get(Server+'/preia_comanda')
                comanda=r.json().get("comanda")
                r.close()
                return comanda
        except Exception as e:
                print("Eroare GET: ", e)
                return "none"