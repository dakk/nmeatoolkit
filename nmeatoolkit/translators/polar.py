import pynmea2
from .translator import FileTranslator

class PolarTranslator(FileTranslator):
    def __init__(self):
        super().__init__()

    def feed(self, s: pynmea2.NMEASentence) -> None:
        if not s.isValid():
            return None

    def result(self) -> str:
        return ''