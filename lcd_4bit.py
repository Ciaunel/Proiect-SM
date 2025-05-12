from machine import Pin
from time import sleep_ms
from lcd_api import LcdApi

class GpioLcd(LcdApi):
    def __init__(self, rs, enable, d4, d5, d6, d7, num_lines=2, num_columns=16):
        self.rs = rs
        self.enable = enable
        self.data_pins = [d4, d5, d6, d7]

        self.rs.init(Pin.OUT)
        self.enable.init(Pin.OUT)

        for pin in self.data_pins:
            pin.init(Pin.OUT)

        sleep_ms(20)
        self._write_nibble(0x03)
        sleep_ms(5)
        self._write_nibble(0x03)
        sleep_ms(1)
        self._write_nibble(0x03)
        sleep_ms(1)
        self._write_nibble(0x02)  # 4-bit mode

        self.hal_write_command(0x28)  # Function set: 4-bit, 2 line, 5x8 dots
        self.hal_write_command(0x0C)  # Display ON
        self.hal_write_command(0x06)  # Entry mode
        self.clear()

        super().__init__(num_lines, num_columns)

    def _pulse_enable(self):
        self.enable.value(0)
        sleep_ms(1)
        self.enable.value(1)
        sleep_ms(1)
        self.enable.value(0)
        sleep_ms(1)

    def _write_nibble(self, nibble):
        for i in range(4):
            self.data_pins[i].value((nibble >> i) & 1)
        self._pulse_enable()

    def hal_write_command(self, cmd):
        self.rs.value(0)
        self._write_nibble(cmd >> 4)
        self._write_nibble(cmd & 0x0F)

    def hal_write_data(self, data):
        self.rs.value(1)
        self._write_nibble(data >> 4)
        self._write_nibble(data & 0x0F)
