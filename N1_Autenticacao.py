#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

#
# N1 - Autenticação
# 

import couchdb
import aux

# CTV3-1:Logar no sistema com sucesso
def CTV3_1(driver):

    server = couchdb.Server()
    db = server['test']
    doc = db['config']

    aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])



