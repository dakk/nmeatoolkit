# -*- coding: utf-8 -*-
# Copyright (C) 2021 - 2025 Davide Gessa
"""
MIT License

Copyright (c) 2021 - 2025 Davide Gessa

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
"""
import datetime

import pynmea2

from .translator import ExtractorBaseTranslator, FileTranslator

GPX_HEADER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n<gpx xmlns="http:'
    + '//www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.gar'
    + 'min.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com'
    + '/xmlschemas/TrackPointExtension/v1" creator="Oregon 400t" version="1.1" '
    + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation'
    + '="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gp'
    + "x.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmi"
    + "n.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/Tr"
    + "ackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensio"
    + 'nv1.xsd">'
)


class GPXTranslator(FileTranslator, ExtractorBaseTranslator):
    def __init__(self, extensions=False):
        super().__init__()
        self.gpx = ""
        self.ft = None
        self.extensions = extensions

    def _gpx_header(self):
        gpx = GPX_HEADER
        gpx += (
            '<metadata><link href="https://github.com/dakk/nmeatoolkit"><text>NMEA Toolkit'
            + "</text></link><time>"
            + self.ft
            + "</time></metadata>"
        )
        gpx += "<trk>\n"
        gpx += "<trkseg>\n"
        return gpx

    def _gpx_footer(self):
        gpx = "</trkseg>\n"
        gpx += "</trk>\n"
        gpx += "</gpx>\n"
        return gpx

    def feed(self, s: pynmea2.NMEASentence):  # noqa: C901
        if not s:
            return

        self.extract(s)

        if (
            isinstance(s, pynmea2.types.LatLonFix)
            and s.latitude != 0
            and s.longitude != 0
            and self.datestamp is not None
        ):
            gpx = '<trkpt lat="%s" lon="%s">\n' % (s.latitude, s.longitude)
            # gpx += '<ele>%s</ele>\n' % (s.altitude)
            gpx += "<time>%s</time>\n" % (
                datetime.datetime.combine(self.datestamp, s.timestamp)
            )

            if self.ft is None:
                self.ft = datetime.datetime.combine(s.datestamp, s.timestamp).strftime(
                    "%Y-%m-%dT%H:%M:%S.%f%z"
                )

            if self.speed is not None:
                gpx += "<speed>%s</speed>\n" % (self.speed)

            # Add extensions
            if self.extensions:
                gpx += "<extensions>\n"
                gpx += "<gpxx:TrackPointExtension>\n"

                # if self.speed is not None:
                #     gpx += '<gpxx:speed>%s</gpxx:speed>\n' % (self.speed)
                if self.hdg is not None:
                    gpx += "<gpxx:heading>%s</gpxx:heading>\n" % (self.hdg)
                if self.twa is not None:
                    gpx += "<gpxx:twa>%s</gpxx:twa>\n" % (self.twa)
                if self.tws is not None:
                    gpx += "<gpxx:tws>%s</gpxx:tws>\n" % (self.tws)
                if self.awa is not None:
                    gpx += "<gpxx:awa>%s</gpxx:awa>\n" % (self.awa)
                if self.aws is not None:
                    gpx += "<gpxx:aws>%s</gpxx:aws>\n" % (self.aws)
                if self.watertemp is not None:
                    gpx += "<gpxx:wtemp>%s</gpxx:wtemp>\n" % (self.watertemp)
                if self.depth is not None:
                    gpx += "<gpxx:depth>%s</gpxx:depth>\n" % (self.depth)

                gpx += "</gpxx:TrackPointExtension>\n"
                gpx += "</extensions>\n"

            gpx += "</trkpt>\n"
            self.gpx += gpx

        return

    def result(self) -> str:
        return self._gpx_header() + self.gpx + self._gpx_footer()
