import pynmea2
from .translator import FileTranslator

class GPXTranslator(FileTranslator):
    def __init__(self):
        super().__init__()
        self.hdg = None
        self.twa = None
        self.tws = None
        self.watertemp = None
        self.depth = None

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
        if not s.isValid():
            return

        # if s is HDG
        if s.sentence_type == 'HDT':
            self.hdg = s.heading

        if s.sentence_type == 'MTW':
            self.watertemp = s.temperature

        if s.sentence_type == 'DBT':
            self.depth = s.depth_meters

        # if s contains wind information, store on variables twa and tws
        if s.sentence_type == 'MWV':
            # TODO: check if this is apparent or real wind, save both
            self.twa = s.wind_angle
            self.tws = s.wind_speed
        if s.sentence_type == 'MWD':
            self.twa = s.direction_true
            self.tws = s.wind_speed_knots


        # if s contains coordinates
        if isinstance(s, pynmea2.types.LatLonFix):
            gpx = '<trkpt lat="' + s.latitude + '" lon="' + s.longitude + '">\n'
            gpx += '<ele>' + s.altitude + '</ele>\n'
            gpx += '<time>' + s.timestamp + '</time>\n'

            # Add extensions
            gpx += '<extensions>\n'
            gpx += '<gpxx:TrackPointExtension>\n'

            if self.hdg != None:
                gpx += '<gpxx:heading>' + self.hdg + '</gpxx:heading>\n'
            if self.twa != None:
                gpx += '<gpxx:twa>' + self.twa + '</gpxx:twa>\n'
            if self.tws != None:
                gpx += '<gpxx:tws>' + self.tws + '</gpxx:tws>\n'
            if self.watertemp != None:
                gpx += '<gpxx:watertemp>' + self.watertemp + '</gpxx:watertemp>\n'
            if self.depth != None:
                gpx += '<gpxx:depth>' + self.depth + '</gpxx:depth>\n'

            gpx += '</gpxx:TrackPointExtension>\n'
            gpx += '</extensions>\n'
            
            gpx += '</trkpt>\n'     
            self.gpx += gpx

        return

    def result(self) -> str:
        return self._gpx_header() + self.gpx + self._gpx_footer()