import sys

class Output:
    def write(self, data):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class FileOutput(Output):
    def __init__(self, filepath = '--'):
        self.filepath = filepath
        if self.filepath == '--':
            self.file = sys.stdout
        else:
            self.file = open(self.filepath, 'w')

    def write(self, data):
        self.file.write(data)

    def close(self):
        self.file.close()