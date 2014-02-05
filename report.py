#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

from datetime import datetime, date, time

import couchdb

# logger to couchdb
class Logger:
    def __init__(self):

        now = datetime.now()

        self.reportName = 'report - '+str(now)

        self.server = couchdb.Server()
        self.db = self.server['test']
        self.db[self.reportName] = {}
        self.doc = self.db[self.reportName]

        self.doc['start'] = str(now)
        self.db.update([self.doc])

    def save(self,header,msg):
        self.doc[header] = msg
        self.db.update([self.doc])        
        
    def close(self):
    
        self.doc['end'] = str(datetime.now())
        self.db.update([self.doc])

