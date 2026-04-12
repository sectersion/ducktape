import usb_hid

class Keyboard:
    def __init__(self):
        self.dev = usb_hid.devices[0]  # keyboard interface

    def send(self, text):
        for ch in text:
            self.dev.send_str(ch)

    def press(self, modifier, key):
        # modifier: bitmask 0x01 ctrl, 0x02 shift, 0x04 alt, 0x08 gui
        # key: a single character, or pre-mapped special char
        self.dev.send_mod(modifier, key)