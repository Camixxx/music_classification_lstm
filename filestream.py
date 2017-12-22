import os
from music21 import *
import sys
import xml.etree.ElementTree as ET
sys.path.insert(0, "../../python/")


current_directory = os.path.dirname(os.path.realpath(__file__))

class midi_data():
    def __init__(self, measure_notes=None, measure_chords = None, time_signature=None):
        self.measure_notes = measure_notes
        self.measure_chords = measure_chords
        self.time_signature = time_signature

class xml_data():
    def __init__(self, measure_notes=None, time_signature=None):
        self.measure_notes = measure_notes
        self.time_signature = time_signature

class xml_music():
    def __init__(self ,measure_notes=None, time_signature=None):
        self.measure_notes = measure_notes
        self.time_signature = time_signature


def getStream(filename):
    return converter.parse(current_directory+'/data/' + filename)


def getFlatStream(filename):
    s = converter.parse(current_directory+'/data/' + filename)
    return s.flat

def getXML(filename):
    f = open(current_directory+'/data/' + filename, 'r')
    return f.read()

def getXmlMusic(filename):
    path  = current_directory+'/data/' + filename
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        print("get root", root)
        return root
    except:
        print("Error,can't open xml at" + path)
        return False
