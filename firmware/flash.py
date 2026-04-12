from machine import Pin, SPI
import struct

FLASH_CS   = Pin(10, Pin.OUT)
FLASH_MOSI = Pin(11)
FLASH_CLK  = Pin(12)
FLASH_MISO = Pin(13)

spi = SPI(
    0,
    baudrate=20_000_000,
    polarity=0,
    phase=0,
    sck=FLASH_CLK,
    mosi=FLASH_MOSI,
    miso=FLASH_MISO
)

CMD_READ       = 0x03
CMD_WREN       = 0x06
CMD_PP         = 0x02
CMD_SECTOR_ERASE = 0x20      # 4KB
CMD_CHIP_ERASE = 0xC7
CMD_READ_STATUS = 0x05

PAGE_SIZE = 256
FLASH_SIZE = 2 * 1024 * 1024   # 16Mbit = 2MB


KEY = b"ifyoureadthisgoaway!7813!@*&^"  # must be same for read/write

def _crypt(data: bytes) -> bytes:
    out = bytearray(len(data))
    k = KEY
    for i in range(len(data)):
        out[i] = data[i] ^ k[i % len(k)]
    return bytes(out)


def _cs(low):
    FLASH_CS.value(0 if low else 1)

def _wait_ready():
    while True:
        _cs(True)
        spi.write(bytes([CMD_READ_STATUS]))
        status = spi.read(1)[0]
        _cs(False)
        if (status & 0x01) == 0:
            break

def _write_enable():
    _cs(True)
    spi.write(bytes([CMD_WREN]))
    _cs(False)

def _page_program(addr, data):
    _write_enable()
    _cs(True)
    spi.write(bytes([CMD_PP]) + addr.to_bytes(3, 'big'))
    spi.write(data)
    _cs(False)
    _wait_ready()

def _read(addr, length):
    _cs(True)
    spi.write(bytes([CMD_READ]) + addr.to_bytes(3, 'big'))
    buf = spi.read(length)
    _cs(False)
    return buf

def _erase_chip():
    _write_enable()
    _cs(True)
    spi.write(bytes([CMD_CHIP_ERASE]))
    _cs(False)
    _wait_ready()


def clear_chip():

    _erase_chip()

def write_all(text: str):

    data = text.encode("utf-8")
    enc = _crypt(data)

    if len(enc) > FLASH_SIZE:
        raise ValueError("Text too large for flash")

    clear_chip()

    addr = 0
    i = 0
    while i < len(enc):
        chunk = enc[i:i+PAGE_SIZE]
        _page_program(addr, chunk)
        addr += len(chunk)
        i += len(chunk)

def read_all() -> str:

    raw = _read(0, FLASH_SIZE)
    

    raw = raw.rstrip(b"\xFF")

    if not raw:
        return ""

    dec = _crypt(raw)
    return dec.decode("utf-8", errors="ignore")