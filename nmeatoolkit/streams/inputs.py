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
import socket
import sys
import pynmea2

class Input:
    def readSentence(self) -> pynmea2.NMEASentence:
        raise NotImplementedError()

    def end(self):
        return True

    def close(self):
        raise NotImplementedError()

class FileInput(Input):
    def __init__(self, filepath = '--'):
        self.filepath = filepath
        if self.filepath == '--':
            self.file = sys.stdin
        else:
            self.file = open(filepath, 'r')
        self.lastLine = 'NMEA'

    def readSentence(self) -> pynmea2.NMEASentence:
        self.lastLine = self.file.readline()
        
        try:
            return pynmea2.parse(self.lastLine.replace('\n', ''))
        except pynmea2.nmea.ParseError:
            return None

    def end(self):
        return self.lastLine == ''
        
    def close(self):
        self.file.close()

    def __del__(self):
        self.close()

class NetworkInput(Input):
    def __init__(self, host, port, protocol = 'tcp'):
        self.host = host
        self.port = port
        self.protocol = protocol

        if self.protocol == 'tcp':
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.socket.connect((host, port))

    def readSentence(self) -> pynmea2.NMEASentence:
        l = self.socket.recv(1024).decode('utf-8')
        try:
            return pynmea2.parse(l)
        except pynmea2.nmea.ParseError:
            return None

    def end(self):
        return self.socket.closed

    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()