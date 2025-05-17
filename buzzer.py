import machine, utime
buzzer = machine.PWM(machine.Pin(28))  # Pin 14 (GP14)

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