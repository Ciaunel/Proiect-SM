class LcdApi:
    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0

    def clear(self):
        self.hal_write_command(0x01)  # Clear display
        self.move_to(0, 0)

    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x + 0x40 * cursor_y
        self.hal_write_command(0x80 | addr)

    def putchar(self, char):
        self.hal_write_data(ord(char))

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.cursor_y += 1
                self.cursor_x = 0
                self.move_to(self.cursor_x, self.cursor_y)
            else:
                self.putchar(char)
                self.cursor_x += 1
                if self.cursor_x >= self.num_columns:
                    self.cursor_x = 0
                    self.cursor_y += 1
                    if self.cursor_y >= self.num_lines:
                        self.cursor_y = 0
                    self.move_to(self.cursor_x, self.cursor_y)
