# -*- coding: utf-8 -*-
# Copyright (C) 2021 Davide Gessa
'''
MIT License

Copyright (c) 2021 Davide Gessa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import math
import pynmea2
from .translator import ExtractorBaseTranslator, FileTranslator

class PolarTranslator(FileTranslator, ExtractorBaseTranslator):
    def __init__(self):
        super().__init__()
        self.ttws = []
        self.ttwa = []
        self.speedTable = {}


    def feed(self, s: pynmea2.NMEASentence) -> None:
        if not s:
            return

        self.extract(s)

        if self.tws and self.twa and self.speed and self.hdg:
            tws = int(math.floor(self.tws / 2)) * 2
            twa = int(math.floor(self.twa / 5)) * 5

            speed = self.speed

            if twa > 180:
                twa = twa - 180

            if speed == 0 or twa > 180. or tws > 45 or twa < 30:
                return

            if not tws in self.ttws:
                self.ttws.append(tws)
            if not twa in self.ttwa:
                self.ttwa.append(twa)

            if (tws,twa) in self.speedTable:
                if self.speedTable[(tws,twa)] < speed:
                    self.speedTable[(tws,twa)] = speed
            else:
                self.speedTable[(tws, twa)] = speed 
        

    def result(self) -> str:
        self.ttws.sort()
        self.ttwa.sort()

        s = 'TWA\TWS'
        for x in self.ttws:
            s += '\t%d' % x
        s += '\n'

        prev = 0
        for y in self.ttwa:
            s += '%d' % y
            for x in self.ttws:
                if (x, y) in self.speedTable:
                    s += '\t{:.1f}'.format(self.speedTable[(x, y)])
                else:
                    s += '\t{:.1f}'.format(0)
            s += '\n'

        return s