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
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="nmeatoolkit",
    version="0.1.6",
    author="Davide Gessa",
    author_email="gessadavide@gmail.com",
    description="A comprensive software collection for nmea manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dakk/nmeatoolkit",
    packages=setuptools.find_packages(exclude=["tests", "examples", "docs"]),
    entry_points={
        "console_scripts": [
            "stalk2nmea = tools.stalk2nmea:main",
            "nmea2gpx = tools.nmea2gpx:main",
            "nmea2polar = tools.nmea2polar:main",
            "nmeatk = tools.nmeatk:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
    requires=open('requirements.txt').read().splitlines()
)