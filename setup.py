import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Raspi UPS HAT Monitor",
    version = "0.0.1",
    author = "Michele Pinassi",
    author_email = "o-zone@zerozone.it",
    description = ("Monitor for Raspi UPS Hat"),
    keywords = "raspberry, hat, ups",
    scripts=['raspiupsmonitor.py'],
    packages=['RaspiUpsMonitor'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
	"Environment :: Console",
	"Intended Audience :: Information Technology",
	"Programming Language :: Python",
    ],
)
