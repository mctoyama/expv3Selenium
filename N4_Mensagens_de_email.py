#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

# auxiliary functions for selenium CTs

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import selenium.common.exceptions

#
# N4 - Mensagens de email
# 

import couchdb
import aux

# all tests for this module
def allTests(logger):
    CTV3_31(logger)

# CTV3-31:Enviar Mensagens
def CTV3_31(logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver()

        server = couchdb.Server()
        db = server['test']
        doc = db['config']
        
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])
        aux.openComposeMailWindow(driver,'CTV3_31_MAIL')
        logger.save('CTV3_31','True')        

    except Exception as err:
        logger.save('CTV3_31',str(type(err))+str(err))        

    finally:
        driver.quit()

