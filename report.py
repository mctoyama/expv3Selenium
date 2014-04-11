#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

from datetime import datetime, date, time

# logger to html file
class Logger:
    def __init__(self):

        start = str(datetime.now()).encode('utf8')

        self.reportName = 'report - '+start+'.html'

        self.fd = open(self.reportName,'w+')

        txt = u"""<html>
                     <meta charset="utf-8"> 
                     <head>
                       <title>Report</title>
                     </head>
                     <style>
                       table,th,td
                       {
                         border:1px solid black;
                         border-collapse:collapse;
                         text-align: left;
                       }
                     </style>
                     <body>
                       <table>
                         <thead>
                           <tr><th>start</th><th>"""+start+u"""</th></tr>
                         </thead>
                         <tbody>"""
        txt = txt.encode('utf8')
        self.fd.write(txt)

    def save(self,header,desc,msg):

        header = header.replace("<","").replace(">","")
        desc = desc.replace("<","").replace(">","")
        msg = msg.replace("<","").replace(">","")

        txt = u"""<tr><td>"""+header+u"""</td><td>"""+desc+u"""</td><td>"""+msg+u"""</td><tr>"""+u'\n'
        txt = txt.encode('utf8')
        self.fd.write(txt)
        
    def close(self):
    
        txt = u"""</tbody>
                       <tfoot>
                         <tr><th>end</th><th>"""+str(datetime.now()).encode('utf8')+u"""</th></tr>
                       </tfoot>
                       </table>
                     </body>
                   </html>"""
        txt = txt.encode('utf8')

        self.fd.write(txt)
        self.fd.close()


