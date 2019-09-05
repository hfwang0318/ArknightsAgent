import ctypes
import sys


class ColorOutput():
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    FOREGROUND_BLACK = 0x00 # black.
    FOREGROUND_DARKBLUE = 0x01 # dark blue.
    FOREGROUND_DARKGREEN = 0x02 # dark green.
    FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
    FOREGROUND_DARKRED = 0x04 # dark red.
    FOREGROUND_DARKPINK = 0x05 # dark pink.
    FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
    FOREGROUND_DARKWHITE = 0x07 # dark white.
    FOREGROUND_DARKGRAY = 0x08 # dark gray.
    FOREGROUND_BLUE = 0x09 # blue.
    FOREGROUND_GREEN = 0x0a # green.
    FOREGROUND_SKYBLUE = 0x0b # skyblue.
    FOREGROUND_RED = 0x0c # red.
    FOREGROUND_PINK = 0x0d # pink.
    FOREGROUND_YELLOW = 0x0e # yellow.
    FOREGROUND_WHITE = 0x0f # white.

    BACKGROUND_BLUE = 0x10 # dark blue.
    BACKGROUND_GREEN = 0x20 # dark green.
    BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
    BACKGROUND_DARKRED = 0x40 # dark red.
    BACKGROUND_DARKPINK = 0x50 # dark pink.
    BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
    BACKGROUND_DARKWHITE = 0x70 # dark white.
    BACKGROUND_DARKGRAY = 0x80 # dark gray.
    BACKGROUND_BLUE = 0x90 # blue.
    BACKGROUND_GREEN = 0xa0 # green.
    BACKGROUND_SKYBLUE = 0xb0 # skyblue.
    BACKGROUND_RED = 0xc0 # red.
    BACKGROUND_PINK = 0xd0 # pink.
    BACKGROUND_YELLOW = 0xe0 # yellow.
    BACKGROUND_WHITE = 0xf0 # white.


    def __init__(self):
        self.__std_out_handle = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)


    def __call__(self, msg):
        if '@' not in msg:
            self._print(msg, None)
        else:
            msg, color = msg.split('@')
            color = color.strip()
            self._print(msg, color)


    def _set_cmd_text_color(self, color):
        result = ctypes.windll.kernel32.SetConsoleTextAttribute(self.__std_out_handle, color)
        return result


    # 重置颜色
    def _reset_color(self):
        self._set_cmd_text_color(self.FOREGROUND_RED | self.FOREGROUND_GREEN | self.FOREGROUND_BLUE)

    def _print(self, msg, color=None):
        if color is None:
            print(msg)

        elif color == 'red':
            self._set_cmd_text_color(self.FOREGROUND_RED)
            # sys.stdout.write(msg)
            print(msg)
            self._reset_color()

        elif color == 'yellow':
            self._set_cmd_text_color(self.FOREGROUND_DARKYELLOW)
            print(msg)
            self._reset_color()

        elif color == 'green':
            self._set_cmd_text_color(self.FOREGROUND_GREEN)
            print(msg)
            self._reset_color()

        elif color == 'blue':
            self._set_cmd_text_color(self.FOREGROUND_SKYBLUE)
            print(msg)
            self._reset_color()

