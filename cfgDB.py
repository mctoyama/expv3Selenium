#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

import platform
import pickle
import sys

#############################################################
# returns an dictonary from file

def getDict(regName):
    return Record(regName).reg

#############################################################
# class record - phisical record of an dict
class Record:
    def __init__(self,regName):

        self.path = ''

        if platform.system() == 'Linux':
            self.path = './cfg/'
        elif platform.system() == 'Windows':
            self.path = '.\\cfg\\'
        else:
            raise Exception('Unsuported operational system: '+platform.system())

        self.fileName = regName
        self.reg = {}
        
        try:
            fd = open(self.path+self.fileName, 'r+')
            self.reg = pickle.load(fd)

        except IOError as err:
            fd = open(self.path+self.fileName, 'w+')
            pickle.dump(self.reg,fd)

        fd.close()
        
    def update(self):
        
        fd = open(self.path+self.fileName, 'w+')

        pickle.dump(self.reg,fd)

        fd.close()

    def __str__(self):

        ret = ""

        for k in self.reg:
            if type(self.reg[k]) == unicode:
                txt = k + ': ' + str(self.reg[k].encode('utf8')) + '\n'
            else:
                txt = k + ': ' + str(self.reg[k]) + '\n'
                
            ret = ret + txt

        return ret

#############################################################

def main():

    record = None

    fname = ""

    if len(sys.argv) > 1:
        fname = sys.argv[1]

    print '################'
    print '-- Welcome do cfg record manager -- ' + fname
    print '################'

    if len(sys.argv) == 2:
        record = Record(sys.argv[1].decode(sys.stdin.encoding))
        print record

    while(True):

        print '################'
        print 'q - quit'
        print 'o - open record'
        print 'p - print record'
        print '+ add /update field'
        print '- delete field'
        print ''
        print 'waiting command: '

        cmd = raw_input().decode(sys.stdin.encoding)

        if cmd == 'q':

            break

        elif cmd == 'o':

            print 'filename: '

            record = Record(raw_input().decode(sys.stdin.encoding))

        elif cmd == 'p':

            if record is None:
                print 'open record first!'
            else:

                print '=========+++++========='
                print record
                print '=========+++++========='

        elif cmd == '+':

            if record is None:
                print 'open record first!'
            else:
                print 'field name:'
                tag = raw_input().decode(sys.stdin.encoding)
                print 'value:'
                value = raw_input().decode(sys.stdin.encoding)

                if value[0] == '#':
                    try:
                        value = int(value[1:len(value)])
                    except ValueError as err:
                        try:
                            value = float(value[1:len(value)])
                        except ValueError as err:
                            pass

                record.reg[tag] = value
                record.update()

        elif cmd == '-' or cmd == '-':

            if record is None:
                print 'open record first!'
            else:
                print 'field name:'
                tag = raw_input().decode(sys.stdin.encoding)
                try:
                    del record.reg[tag]
                    record.update()
                except KeyError as err:
                    pass
        else:
            print 'Invalid comand'

#############################################################

# executs the main script
if __name__ == "__main__":
    main()

