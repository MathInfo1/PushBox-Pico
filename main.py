from machine import Pin, SPI
from time import sleep_ms

screenSize = (480, 320)

spi = SPI(0, baudrate=30000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))

cs = Pin(17, Pin.OUT, value=1)
dc = Pin(22, Pin.OUT, value=1)
rst = Pin(21, Pin.OUT, value=1)
led = Pin(13, Pin.OUT, value=1)

def hexToBit(hexString):
    intList = []
    for i in range(0, len(hexString), 2):
        intList.append(int(hexString[i:i+2], 16))
    return bytes(intList)

def resetDisplay():
    rst.value(1)
    sleep_ms(10)
    rst.value(0)
    sleep_ms(20)
    rst.value(1)
    sleep_ms(150)

def command(cmd, data=None):
    cs.value(0)
    dc.value(0)
    if isinstance(cmd, int): spi.write(bytes([cmd]))
    else: spi.write(cmd)

    if not data == None:
        dc.value(1)
        if isinstance(data, int): spi.write(bytes([data]))
        else: spi.write(data)

    cs.value(1)

def initDisplay(orientation):
    global screenSize
    resetDisplay()

    command(0x01) # Software Reset
    sleep_ms(120)
    command(0x11) # Sleep OUT
    sleep_ms(120)

    command(0x3A, 0x66) # Interface Pixel Format
    if orientation == "landscape" or orientation == "horizontal":
        command(0x36, 0xE8) # Memory Access Control
        screenSize = (480, 320)
    else:
        command(0x36, 0x88)
        screenSize = (320, 480)

    command(0xC2, 0x44) # Power Control 3
    command(0xC5, hexToBit('00000000')) # VCOM Control

    command(0xB1, hexToBit('B011')) # Frame Rate Control
    command(0xB4, 0x02) # Display Inversion Control
    command(0xB6, hexToBit('02023B')) # Display Function Control

    command(0xE0, hexToBit('0F241C0A0F084388320F10060F0700')) # Positive Gamma Control
    command(0xE1, hexToBit('0F3830090F0F4E773C071005231B00')) # Negative Gamma Control
    
    command(0x13) # Normal Display Mode ON
    command(0x29) # Display ON
    sleep_ms(100)

def setWindow(x0, y0, x1, y1):
    command(0x2A, bytes([x0 // 256, x0 % 256, x1 // 256, x1 % 256]))
    command(0x2B, bytes([y0 // 256, y0 % 256, y1 // 256, y1 % 256]))

def drawRect(tlx, tly, w, h, color, thickness=0):
    setWindow(tlx, tly, tlx + w - 1, tly + h - 1)
    pixel = bytes([color[0] & 0xFC, color[1] & 0xFC, color[2] & 0xFC])

    cs.value(0)
    dc.value(0)
    spi.write(b'\x2C')
    dc.value(1)

    if thickness == 0:
        pixelsPerChunk = 256
        total = w * h
        chunk = pixel * pixelsPerChunk
        while total >= pixelsPerChunk:
            spi.write(chunk)
            total -= pixelsPerChunk
        if total: spi.write(pixel * total)
    else:
        pass

    cs.value(1)

initDisplay("landscape")
drawRect(0, 0, screenSize[0] // 2, screenSize[1], (255, 0, 0))
drawRect(screenSize[0] // 2, 0, screenSize[0] // 2, screenSize[1], (0, 255, 0))