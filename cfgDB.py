#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

import xml.etree.ElementTree as ET

import platform
import sys

#############################################################
# returns an dictonary from file

def getDict(regName):

    path = ''

    if platform.system() == 'Linux':
        path = './cfg/'
    elif platform.system() == 'Windows':
        path = '.\\cfg\\'
    else:
        raise Exception('Unsuported operational system: '+platform.system())

    tree = ET.parse(path+regName)
    root = tree.getroot()

    ret = {}

    for child in root:
        try:
            if child.attrib['type'] == "int":
                ret[child.tag] = int(child.text)
            elif child.attrib['type'] == "float":
                ret[child.tag] = float(child.text)
            else:
                raise Exception("Unsupported data type in XML file")
        except KeyError as err:
            ret[child.tag] = child.text
        
    return ret

#############################################################


