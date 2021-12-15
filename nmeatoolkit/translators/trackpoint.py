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
import datetime
import pynmea2
from .translator import FileTranslator, StreamTranslator

class TrackPoint:
    def __init__ (self, lat, lon, time, speed = None, hdg = None, twa = None, tws = None, awa = None, aws = None, watertemp = None, depth = None):
        self.lat = lat
        self.lon = lon
        self.time = time
        self.hdg = hdg
        self.twa = twa
        self.tws = tws
        self.awa = awa
        self.aws = aws
        self.watertemp = watertemp
        self.depth = depth
        self.speed = speed

    def __str__(self) -> str:
        return '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (self.lat, self.lon, self.time, self.speed, self.hdg, self.twa, self.tws, self.awa, self.aws, self.watertemp, self.depth)


class TrackPointTranslator(FileTranslator, StreamTranslator):
    def __init__(self):
        super().__init__()
        self.hdg = None
        self.twa = None
        self.tws = None
        self.awa = None
        self.aws = None
        self.watertemp = None
        self.depth = None 
        self.speed = None
        self.datestamp = None

        self.track = []

    def feed(self, s: pynmea2.NMEASentence) -> TrackPoint:
        if not s:
            return

        # if s is HDG
        if s.sentence_type == 'HDT' or s.sentence_type == 'HDM':
            try:
                self.hdg = float(s.heading)
            except:
                pass

        if s.sentence_type == 'MTW':
            try:
                self.watertemp = float(s.temperature)
            except:
                pass

        if s.sentence_type == 'DBT':
            try:
                self.depth = float(s.depth_meters)
            except:
                pass

        # if s contains wind information, store on variables twa and tws
        if s.sentence_type == 'MWV':
            if s.reference == 'R':
                try:
                    self.awa = float(s.wind_angle)
                    self.aws = float(s.wind_speed)
                except:
                    pass
            elif s.reference == 'T':
                try:
                    self.twa = float(s.wind_angle)
                    self.tws = float(s.wind_speed)
                except:
                    pass
        if s.sentence_type == 'MWD':
            try:
                self.twa = float(s.direction_true)
                self.tws = float(s.wind_speed_knots)
            except:
                pass

        if s.sentence_type == 'VTG':
            if s.spd_over_grnd_kts != None:
                self.speed = float(s.spd_over_grnd_kts)

        if isinstance(s, pynmea2.types.DatetimeFix) or s.sentence_type == 'ZDA':
            self.datestamp = s.datestamp

        # if s contains coordinates
        if isinstance(s, pynmea2.types.LatLonFix) and s.latitude != 0 and s.longitude != 0:
            tp = TrackPoint(s.latitude, s.longitude, datetime.datetime.combine(self.datestamp, s.timestamp), self.speed, self.hdg, self.twa, self.tws, self.awa, self.aws, self.watertemp, self.depth)
            self.track.append (tp)
            return tp

        return

    def result(self) -> str:
        return self.track
