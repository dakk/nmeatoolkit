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
import datetime
from .translator import FileTranslator

class GPXTranslator(FileTranslator):
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
        self.gpx = ''

    def _gpx_header(self):
        gpx = '<?xml version="1.0" encoding="UTF-8"?>\n'
        gpx += '<gpx version="1.1" creator="nmea2gpx" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n'
        gpx += '<metadata>\n'
        # self.gpx += '<name>' + self.fname + '</name>\n'
        gpx += '</metadata>\n'
        gpx += '<trk>\n'
        gpx += '<trkseg>\n'
        return gpx
    
    def _gpx_footer(self):
        gpx = '</trkseg>\n'
        gpx += '</trk>\n'
        gpx += '</gpx>\n'
        return gpx

    def feed(self, s: pynmea2.NMEASentence) -> None:
        if not s:
            return

        # if s is HDG
        if s.sentence_type == 'HDT':
            self.hdg = float(s.heading)

        if s.sentence_type == 'MTW':
            self.watertemp = float(s.temperature)

        if s.sentence_type == 'DBT':
            self.depth = float(s.depth_meters)

        # if s contains wind information, store on variables twa and tws
        if s.sentence_type == 'MWV':
            if s.reference == 'R':
                self.awa = float(s.wind_angle)
                self.aws = float(s.wind_speed)
            elif s.reference == 'T':
                self.twa = float(s.wind_angle)
                self.tws = float(s.wind_speed)
        if s.sentence_type == 'MWD':
            self.twa = float(s.direction_true)
            self.tws = float(s.wind_speed_knots)

        if s.sentence_type == 'VTG':
            if s.spd_over_grnd_kts != None:
                self.speed = float(s.spd_over_grnd_kts)

        # if s contains coordinates
        if isinstance(s, pynmea2.types.LatLonFix) and isinstance(s, pynmea2.types.DatetimeFix) and s.latitude != 0 and s.longitude != 0:
            gpx = '<trkpt lat="%s" lon="%s">\n' % (s.latitude, s.longitude)
            # gpx += '<ele>%s</ele>\n' % (s.altitude)
            gpx += '<time>%s</time>\n' % (datetime.datetime.combine(s.datestamp, s.timestamp))

            # Add extensions
            gpx += '<extensions>\n'
            gpx += '<gpxx:TrackPointExtension>\n'

            if self.speed != None:
                gpx += '<gpxx:speed>%s</gpxx:speed>\n' % (self.speed)
            if self.hdg != None:
                gpx += '<gpxx:heading>%s</gpxx:heading>\n' % (self.hdg)
            if self.twa != None:
                gpx += '<gpxx:twa>%s</gpxx:twa>\n' % (self.twa)
            if self.tws != None:
                gpx += '<gpxx:tws>%s</gpxx:tws>\n' % (self.tws)
            if self.awa != None:
                gpx += '<gpxx:awa>%s</gpxx:awa>\n' % (self.awa)
            if self.aws != None:
                gpx += '<gpxx:aws>%s</gpxx:aws>\n' % (self.aws)
            if self.watertemp != None:
                gpx += '<gpxx:watertemp>%s</gpxx:watertemp>\n' % (self.watertemp)
            if self.depth != None:
                gpx += '<gpxx:depth>%s</gpxx:depth>\n' % (self.depth)

            gpx += '</gpxx:TrackPointExtension>\n'
            gpx += '</extensions>\n'
            
            gpx += '</trkpt>\n'     
            self.gpx += gpx

        return

    def result(self) -> str:
        return self._gpx_header() + self.gpx + self._gpx_footer()