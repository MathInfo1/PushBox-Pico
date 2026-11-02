from machine import Pin, SPI
from time import sleep_ms
from math import sqrt

def hexToBit(hexString):
    intList = []
    for i in range(0, len(hexString), 2):
        intList.append(int(hexString[i:i+2], 16))
    return bytes(intList)

class Display():
    def __init__(self, sck, mosi, miso, cs, dc, rst, led, orientation="landscape"):
        if orientation == "landscape" or orientation == "horizontal":
            self.screenSize = (480, 320)
        else:
            self.screenSize = (320, 480)
        
        self.orientation = orientation
        self.spi = SPI(0, baudrate=30000000, polarity=0, phase=0, sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
        self.cs = Pin(cs, Pin.OUT, value=1)
        self.dc = Pin(dc, Pin.OUT, value=1)
        self.rst = Pin(rst, Pin.OUT, value=1)
        self.led = Pin(led, Pin.OUT, value=1)
        
        self.initDisplay()

    def resetDisplay(self):
        self.rst.value(1)
        sleep_ms(10)
        self.rst.value(0)
        sleep_ms(20)
        self.rst.value(1)
        sleep_ms(150)

    def command(self, cmd, data=None):
        self.cs.value(0)
        self.dc.value(0)
        if isinstance(cmd, int): self.spi.write(bytes([cmd]))
        else: self.spi.write(cmd)

        self.dc.value(1)
        if not data == None:
            if isinstance(data, int): self.spi.write(bytes([data]))
            else: self.spi.write(data)
        self.cs.value(1)

    def setWindow(self, x0, y0, x1, y1):
        self.command(0x2A, bytes([x0 // 256, x0 % 256, x1 // 256, x1 % 256]))
        self.command(0x2B, bytes([y0 // 256, y0 % 256, y1 // 256, y1 % 256]))

    def getColors(self, x0, y0, x1, y1):
        self.setWindow(int(x0), int(y0), int(x1), int(y1))
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(b'\x2E')

        self.dc.value(1)
        try: 
            self.spi.read(1, 0x00) # Dummy Bit
            colorList = []
            width = x1 - x0 + 1

            for y in range(y1 - y0 + 1):
                rowData = self.spi.read(width * 3, 0x00)
                # colorList.append([rowData[i] * 0x10000 + rowData[i+1] * 0x100 + rowData[i+2] for i in range(0, width * 3, 3)])
                colorList.append([((rowData[i] << 1) & 0xFC, (rowData[i+1] << 1) & 0xFC, (rowData[i+2] << 1) & 0xFC) for i in range(0, width * 3, 3)])
        except Exception as e:
            print("SPI ERROR:", repr(e))
        finally:
            self.cs.value(1)
        
        return colorList

    def debugPixel(self, x, y):
        self.setWindow(x, y, x, y)
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(b'\x2E')

        self.dc.value(1)
        try: 
            self.spi.read(1, 0x00) # Dummy Bit
            colorList = []

            data = self.spi.read(3, 0x00)
            print(data)
        except Exception as e:
            print("SPI ERROR:", repr(e))
        finally:
            self.cs.value(1)
        
        return colorList
        

    def initDisplay(self):
        self.resetDisplay()

        self.command(0x01) # Software Reset
        sleep_ms(120)
        self.command(0x11) # Sleep OUT
        sleep_ms(120)

        self.command(0x3A, 0x66) # Interface Pixel Format
        if self.orientation == "landscape" or self.orientation == "horizontal":
            self.command(0x36, 0xE8) # Memory Access Control
        else:
            self.command(0x36, 0x88)

        self.command(0xC2, 0x44) # Power Control 3
        self.command(0xC5, hexToBit('00000000')) # VCOM Control

        self.command(0xB1, hexToBit('B011')) # Frame Rate Control
        self.command(0xB4, 0x02) # Display Inversion Control
        self.command(0xB6, hexToBit('02023B')) # Display Function Control

        self.command(0xE0, hexToBit('0F241C0A0F084388320F10060F0700')) # Positive Gamma Control
        self.command(0xE1, hexToBit('0F3830090F0F4E773C071005231B00')) # Negative Gamma Control
        
        self.command(0x13) # Normal Display Mode ON
        self.command(0x29) # Display ON
        sleep_ms(100)

    def drawRect(self, tlx, tly, w, h, color, thickness=0):
        pixel = bytes([color[0] & 0xFC, color[1] & 0xFC, color[2] & 0xFC])

        if thickness == 0 or thickness * 2 >= min(w, h): 
            self.setWindow(tlx, tly, tlx + w - 1, tly + h - 1) 

            self.cs.value(0)
            self.dc.value(0)
            self.spi.write(b'\x2C')
            self.dc.value(1)

            pixelsPerChunk = 256
            total = w * h
            chunk = pixel * pixelsPerChunk
            while total >= pixelsPerChunk:
                self.spi.write(chunk)
                total -= pixelsPerChunk
            if total: self.spi.write(pixel * total)

            self.cs.value(1)
        else:
            self.drawRect(tlx, tly, w, thickness, color)
            self.drawRect(tlx, tly + h - thickness, w, thickness, color)
            self.drawRect(tlx, tly, thickness, h, color)
            self.drawRect(tlx + w - thickness, tly, thickness, h, color)

    def drawCircle(self, x, y, radius, color):
        lowerLimits = (int(max(0, x - radius)), int(max(0, y - radius)))
        upperLimits = (int(min(x + radius, self.screenSize[0])), int(min(y + radius, self.screenSize[1])))
        pixel = bytes([color[0] & 0xFC, color[1] & 0xFC, color[2] & 0xFC])

        for i in range(lowerLimits[0], upperLimits[0], 8):
            for j in range(lowerLimits[1], upperLimits[1], 8):
                oldColors = self.getColors(i, j, min(upperLimits[0], i + 7), min(upperLimits[1], j + 7))
                output = b''
                for a in range(len(oldColors)):
                    for b in range(len(oldColors[0])):
                        dx, dy = x - (i + b), y - (j + a)
                        if sqrt(dx ** 2 + dy ** 2) <= radius:
                            output += pixel
                        else:
                            output += bytes(oldColors[a][b])
                self.cs.value(0)
                self.dc.value(0)
                self.spi.write(b'\x2C')
                self.dc.value(1)
                self.spi.write(output)
                self.cs.value(1)

