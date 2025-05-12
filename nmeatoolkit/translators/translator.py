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
import pynmea2


class Translator:
    pass


class StreamTranslator(Translator):
    def feed(self, sentence: pynmea2.NMEASentence):
        raise NotImplementedError()


class FileTranslator(Translator):
    def feed(self, sentence: pynmea2.NMEASentence):
        raise NotImplementedError()

    def result(self) -> str:
        raise NotImplementedError()


class ExtractorBaseTranslator:
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

    def extract(self, s: pynmea2.NMEASentence):  # noqa: C901
        if not s:
            return

        # if s is HDG
        if s.sentence_type == "HDT" or s.sentence_type == "HDM":
            try:
                self.hdg = float(s.heading)
            except:
                pass

        if s.sentence_type == "MTW":
            try:
                self.watertemp = float(s.temperature)
            except:
                pass

        if s.sentence_type == "DBT":
            try:
                self.depth = float(s.depth_meters)
            except:
                pass

        # if s contains wind information, store on variables twa and tws
        if s.sentence_type == "MWV":
            if s.reference == "R":
                try:
                    self.awa = float(s.wind_angle)
                    self.aws = float(s.wind_speed)
                except:
                    pass
            elif s.reference == "T":
                try:
                    self.twa = float(s.wind_angle)
                    self.tws = float(s.wind_speed)
                except:
                    pass
        if s.sentence_type == "MWD":
            try:
                self.twa = float(s.direction_true)
                self.tws = float(s.wind_speed_knots)
            except:
                pass

        if s.sentence_type == "VTG":
            if s.spd_over_grnd_kts is not None:
                self.speed = float(s.spd_over_grnd_kts)

        if isinstance(s, pynmea2.types.DatetimeFix) or s.sentence_type == "ZDA":
            self.datestamp = s.datestamp
