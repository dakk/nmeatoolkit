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
from .pipe import Pipe	
from dateutil import parser

class CropPipe(Pipe):
	"""  """
	def __init__(self, fr=None, to=None):
		if fr == None and to == None:
			raise Exception("You must specify at least one between fr and to")


		self.fr = parser.parse(fr) if isinstance(fr, str) else fr
		self.to = parser.parse(to) if isinstance(to, str) else to

		self.datestamp = None
		self.timestamp = None 
		self.datetime = None


	def transform(self, s: pynmea2.NMEASentence) -> list[pynmea2.NMEASentence]:
		if isinstance(s, pynmea2.types.DatetimeFix) or s.sentence_type == 'ZDA':
			self.datestamp = s.datestamp

		if isinstance(s, pynmea2.types.LatLonFix):
			self.timestamp = s.timestamp

		if self.datestamp and self.timestamp:
			self.datetime = datetime.datetime.combine(self.datestamp, self.timestamp)

		if self.datetime and self.to and self.datetime > self.to:
				return []
		
		if self.datetime and self.fr and self.datetime < self.fr:
				return []
		
		return [s]
