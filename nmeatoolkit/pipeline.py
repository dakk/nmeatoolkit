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
from typing import List

from .translators.translator import FileTranslator, StreamTranslator


class Pipeline:
    def __init__(self, input, output, translator, pipes):
        self.input = input
        self.output = output
        self.translator = translator
        self.pipes = pipes

    def run_partial(self) -> List[str]:
        sen_l = []
        while not self.input.end():
            s = self.input.read_sentence()

            if s is None:
                continue

            spiped = [s]
            for p in self.pipes:
                spiped = p.bulk_transform(spiped)

            if self.translator:
                for x in spiped:
                    f = self.translator.feed(x)

                    if isinstance(self.translator, StreamTranslator) and f:
                        sen_l.append(f)
            else:
                sen_l += spiped

        if self.translator and isinstance(self.translator, FileTranslator):
            sen_l = self.translator.result()

        return sen_l

    def run_once(self):
        if self.input.end():
            return False

        s = self.input.read_sentence()

        if s is None:
            return True

        spiped = [s]
        for p in self.pipes:
            spiped = p.bulk_transform(spiped)

        for x in spiped:
            f = self.translator.feed(x)
            if isinstance(self.translator, StreamTranslator) and f:
                self.output.write(f)

        return True

    def run(self):
        while not self.input.end():
            r = self.run_once()
            if not r:
                break

        if isinstance(self.translator, FileTranslator):
            self.output.write(self.translator.result())

        self.input.close()
        self.output.close()
