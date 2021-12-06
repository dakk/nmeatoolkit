import pynmea2 


class Translator:
    def __init__(self):
        raise NotImplementedError()


class StreamTranslator(Translator):
    def feed(self, sentence: pynmea2.NMEASentence) -> str:
        raise NotImplementedError()


class FileTranslator(Translator):
    def feed(self, sentence: pynmea2.NMEASentence) -> None:
        raise NotImplementedError() 

    def result(self) -> str:
        raise NotImplementedError()


class ToStringTranslator(StreamTranslator):
    def __init__(self):
        pass 

    def feed(self, sentence: pynmea2.NMEASentence) -> str:
        return str(sentence)
