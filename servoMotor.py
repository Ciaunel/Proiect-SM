# --- Servo motor Setup ---
import machine

servo = machine.PWM(machine.Pin(15))
servo.freq(50)

def misca_servo(unghi):
    duty = int(1638 + (unghi / 180) * (8192 - 1638))
    servo.duty_u16(duty)