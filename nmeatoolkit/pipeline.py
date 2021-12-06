from nmeatoolkit.translators.translator import FileTranslator, StreamTranslator


class Pipeline:
    def __init__(self):
        self.pipes = []

    def setInput(self, input):
        self.input = input

    def setOutput(self, output):
        self.output = output

    def setTranslator(self, translator):
        self.translator = translator

    def addPipe(self, pipe):
        self.pipes.append(pipe)

    def run(self):
        while not self.input.end():
            s = self.input.read()

            spiped = [s]
            for pipe in self.pipes:
                spiped = pipe.bulkTransform(spiped)
            
            f = self.translator.feed(spiped)
            if isinstance(self.translator, StreamTranslator) and f:
                self.output.write(f)
            
        if isinstance(self.translator, FileTranslator):
            self.output.write(self.translator.result())