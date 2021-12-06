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

class InputFile(Input):
    def __init__(self, filepath = '--'):
        self.filepath = filepath
        if self.filepath == '--':
            self.file = sys.stdin
        else:
            self.file = open(filepath, 'r')

    def readSentence(self) -> pynmea2.NMEASentence:
        l = self.file.readline()
        try:
            return pynmea2.parse(l)
        except pynmea2.nmea.ParseError:
            return None

    def end(self):
        return self.file.iseof()
        
    def close(self):
        self.file.close()

    def __del__(self):
        self.close()

class InputNetwork(Input):
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