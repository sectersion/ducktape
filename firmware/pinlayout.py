from machine import Pin

# display pin assignments
DISP_SDA = Pin(8)   # data
DISP_SCL = Pin(9)   # clock

#flash pins
FLASH_CS = Pin(10)
FLASH_MOSI = Pin(11)
FLASH_CLK = Pin(12)
FLASH_MISO = Pin(13)

#led
RGB_LED = Pin(48)

#arm header
ARM = Pin(3, Pin.IN, Pin.PULL_UP)