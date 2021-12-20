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
import argparse

from nmeatoolkit.pipeline import Pipeline
from nmeatoolkit.pipes.crop import CropPipe
from nmeatoolkit.pipes.filter import FilterPipe

from .streams.inputs import FileInput
from .streams.outputs import FileOutput
from .translators.tostring import ToStringTranslator
from .translators.gpx import GPXTranslator
from .translators.polar import PolarTranslator
from .pipes.seatalk import SeatalkPipe
from .pipes.truewind import TrueWindPipe

def getDefaultParser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        help="Input file",
        required=False,
        type=str,
        default='--'
    )
    
    parser.add_argument(
        "-o",
        "--output",
        help="Output file",
        required=False,
        default='--',
        type=str,
    )

    parser.add_argument(
        "-f",
        "--format",
        help="Output format",
        required=False,
        type=str,
        default="nmea",
    )

    parser.add_argument(
        "-p",
        "--pipes",
        help="Pipes",
        required=False,
        type=str,
        default=None
    )

    return parser

def processArguments(args):
    input = None 
    output = None 
    translator = None
    pipes = []

    if args.input == '--' or args.input == None:
        input = FileInput()
    elif args.input.startswith('tcp://'):
        raise Exception('Not implemented')
    elif args.input.startswith('udp://'):
        raise Exception('Not implemented')
    else:
        input = FileInput(args.input)

    
    if args.output == '--' or args.output == None:
        output = FileOutput()
    elif args.output.startswith('tcp://'):
        raise Exception('Not implemented')
    elif args.output.startswith('udp://'):
        raise Exception('Not implemented')
    else:
        output = FileOutput(args.output)


    if args.format == 'nmea':
        translator = ToStringTranslator()
    elif args.format == 'pol':
        translator = PolarTranslator()
    elif args.format == 'gpx':
        translator = GPXTranslator()

    for p in args.pipes.split(','):
        pargs = p.split('[')
        ppipe = pargs[0]
        if len(pargs) == 2:
            pargs = pargs[2].split(']')
        pargs = dict(list(map(lambda x: x.split('='), pargs)))


        if ppipe == 'crop':
            fr = pargs['from'] if 'from' in pargs else None
            to = pargs['to'] if 'to' in pargs else None
            pipes.append(CropPipe(fr, to))
        elif ppipe == 'filter':
            exclude = pargs['exclude'] if 'exclude' in pargs else None
            include = pargs['include'] if 'include' in pargs else None
            pipes.append(FilterPipe(exclude, include))
        elif ppipe == 'seatalk':
            pipes.append(SeatalkPipe())
        elif ppipe == 'truewind':
            pipes.append(TrueWindPipe())

    return Pipeline(input, output, translator, pipes)
