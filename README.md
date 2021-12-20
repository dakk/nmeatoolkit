# nmeatoolkit

[![Build Status](https://travis-ci.com/dakk/nmeatoolkit.svg?branch=master)](https://travis-ci.com/dakk/nmeatoolkit.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/nmeatoolkit.svg)](https://badge.fury.io/py/nmeatoolkit)
![PyPI - License](https://img.shields.io/pypi/l/nmeatoolkit)

A comprensive software collection for nmea manipulation; it includes a library and a collections of command line tools.

## Library

- pipes: converts nmea sentence to other nmea sentences
- translators: converts nmea sentence stream to other format
- inputs: sources for nmea sentences
- output: output helpers

## Tools

- nmea2gpx: converts nmea sentences to gpx (with extensions)
- stalk2nmea: converts $STALK to native nmea sentences
- nmea2polar: extracts polars from nmea
- nmeatk: the raw toolkit 

All commands has the same input/output interface as follows:

```bash
cat *.nmea > stalk2nmea -i -- > mod.nmea

stalk2nmea -i tcp://localhost:1011 > mod.nmea

stalk2nmea -i udp://localhost:1011 > mod.nmea

stalk2nmea -i path/file.nmea > mod.nmea

stalk2nmea -i path/file.nmea -o mod.nmea

stalk2nmea -i tcp://localhost:1011 -o udp://localhost:1012
```

Every command can receive a list of pipes to run, in order:

```bash
# Convert seatalk $STALK to nmea and add true wind sentences
stalk2nmea -i test.nmea -p truewind -o output.nmea
```

A pipe can receive parameters as follow:

```bash
# Convert seatalk $STALK to nmea, add true wind sentences, get only wind info
stalk2nmea -i test.nmea -p truewind,filter[bytype:wind] -o output.nmea
```

Every dedicated command can be performed by nmeatk:

```bash
nmeatk -i data.nmea -p truewind -o output.gpx -f gpx
```


## Pipes

### Filter

### Crop

### Seatalk

### Truewind



## License

```
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
```