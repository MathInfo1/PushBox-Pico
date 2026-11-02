from machine import Pin

class Input():
    def __init__(self, w, a, s, d):
        self.w = Pin(w, Pin.IN)
        self.a = Pin(a, Pin.IN)
        self.s = Pin(s, Pin.IN)
        self.d = Pin(d, Pin.IN)
        self.move = (0, 0)

    def getDirection(self):
        return (self.d.value() - self.a.value(), self.w.value() - self.s.value())
