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
import pynmea2
from .pipe import Pipe
import math
from decimal import Decimal, getcontext


class TrueWindPipe(Pipe):
    """ Append new sentences for twa and tws if only apparent data is available """

    def __init__(self):
        self.speed = None
        self.hdg = None

    def transform(self, s: pynmea2.NMEASentence) -> list[pynmea2.NMEASentence]:
        sl = [s]

        if s.sentence_type == 'HDT' or s.sentence_type == 'HDM':
            try:
                self.hdg = float(s.heading)
            except:
                pass

        elif s.sentence_type == 'MWV' and self.hdg:
            # R stands to relative to bow?
            if s.reference == 'R':
                # transform s.wind_angle relative to bow, to real wind angle (relative to north)
                # and then to relative to north
                awa = float(s.wind_angle)
                aws = float(s.wind_speed)
                awd = awa + self.hdg

                # Calculate twa and tws
                # https://en.wikipedia.org/wiki/Apparent_wind#Calculating_apparent_velocity_and_angle
                if self.speed != None and self.speed > 0 and aws > 0:     
                    try:
                        twa = math.degrees(math.atan2(aws * math.sin(math.radians(awd)), self.speed * math.cos(math.radians(awa))))
                        tws = math.sqrt(aws ** 2 + self.speed ** 2 - 2 * aws * self.speed * math.cos(math.radians(awa - twa)))                    

                        awar = math.radians(awa)
                        if awa > 180:
                            twa = 360 - math.degrees(math.acos((aws * math.cos(awar) - self.speed) / tws))
                        else:
                            twa = math.degrees(math.acos((aws * math.cos(awar) - self.speed) / tws))
                    
                        sl.append(pynmea2.MWV('II', 'MWV', ("{:.2f}".format(twa), 'T', "{:.2f}".format(tws), 'k', 'A')))
                    except:
                        pass

        elif s.sentence_type == 'VTG':
            if s.spd_over_grnd_kts != None:
                self.speed = float(s.spd_over_grnd_kts)

        return sl
