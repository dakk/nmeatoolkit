# nmeatoolkit

A comprensive software collection for nmea manipulation; it includes a library and a collections of command line tools.

## Library

- pipes: converts nmea sentence to other nmea sentences
- translators: converts nmea sentence stream to other format
- inputs: sources for nmea sentences
- output: output helpers

## Tools

- nmea2gpx: converts nmea sentences to gpx (with extensions)
- nmea_addtw: add true wind direction / speed even if it is not available
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
stalk2nmea -i test.nmea -p truewind,filter[bytype=wind] -o output.nmea
```

Every dedicated command can be performed by nmeatk:

```bash
nmeatk -i data.nmea -p truewind -o output.gpx -f gpx
```