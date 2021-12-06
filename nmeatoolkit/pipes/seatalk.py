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

class SeatalkPipe(Pipe):
	""" Transform $STALK sentences to native NMEA sentences """
	def __init__(self):
		self.angle = 0
		self.speed = 0

	def transform(self, sentence: pynmea2.NMEASentence) -> list[pynmea2.NMEASentence]:
		s = str(sentence)

		if not s.startswith('$STALK'):
			return [sentence]

		s = s.split(',')[1::]
		nmea = None 
		
		try:
			# AWA Corresponding NMEA sentence: MWV
			if len(s) >= 4 and s[0] == '10' and s[1] == '01':
				angle = (int('0x'+s[3], 16) + int('0x'+s[2], 16) * 0xff) / 2
				#print ('awa', angle)
				#nmea = pynmea2.MWV(True, 'R', angle, 'N', 'A')
				# Create nmea string mwv for wind angle
				self.angle = "{:.1f}".format(angle)
				nmea = '$IIMWV,%s,R,%s,k,A' % (self.angle, self.speed)

			# AWS Corresponding NMEA sentence: MWV
			elif len(s) >= 4 and s[0] == '11' and s[1] == '01':
				speed = (int('0x' + s[2], 16) & 0x7f) + int('0x' + s[3][1], 16) / 10
				#print('aws', speed)
				#nmea = pynmea2.MWV(True, 'R', speed, 'N', 'A')
				# Create nmea string mwv for wind speed
				self.speed = "{:.1f}".format(speed)
				nmea = '$IIMWV,%s,R,%s,k,A' % (self.angle, self.speed)
				
			# DEPTH NMEA sentences: DPT, DBT
			elif len(s) >= 5 and s[0] == '00' and s[1] == '02':
				depth = (int('0x'+s[3], 16) + int('0x'+s[4], 16) * 0xff ) / 10 * 0.3048
				#print ('depth', depth)
				#nmea = pynmea2.DPT('IN', 'DPT', (str(depth)))
				
				# Create nmea string dpt for depth
				depth = "{:.1f}".format(depth)
				nmea = '$IIDBT,,f,%s,M,,F' % (depth)

			# Water temp Corresponding NMEA sentence: MTW
			elif len(s) >= 4 and s[0] == '27' and s[1] == '01':
				temp = ((int('0x'+s[2], 16) + int('0x'+s[3], 16) * 0xff ) - 100.)/10.
				#print ('temp', temp)
				#nmea = pynmea2.MTW(temp, 'celsius')

				# Create nmea string mtw for water temp
				temp = "{:.1f}".format(temp)
				#nmea = '$IIMTW,%s,C,%s,C,%s,C' % (temp, temp, temp)
				nmea = '$IIMDA,,I,,B,,C,%s,C,,,,C,,T,,M,,N,,M' % (temp)

			# Compass
			elif len(s) >= 4 and s[0] == '9c':
				U = int('0x' + s[1][0], 16)
				VW = int('0x' + s[2], 16)
				hdg = (U & 0x3) * 90 + (VW & 0x3F) * 2 + ((U & (2 if 0xC == 0xC else 1)) if (U & 0xC) else 0)
				# print('heading', hdg)
				hdg = "{:.0f}".format(hdg)
				nmea = 'IIHDM,%s,M' % (hdg)
				
			# SOG Corresponding NMEA sentence: VHW
			elif len(s) >= 4 and s[0] == '20' and s[1] == '01':
				sog = ((int('0x'+s[2], 16) + int('0x'+s[3], 16) * 0xff ))/10.
				#print ('sog', sog)
				#nmea = pynmea2.VHW(sog, 'T', 'M', 'N')

				# Create nmea string vhw for speed over ground
				#nmea = '$IIVHW,%s,T,M,N,N' % (sog)
		except:
			pass 
		
		if nmea is not None:
			return [pynmea2.parse(nmea)]
		return [sentence]