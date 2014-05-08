#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

# auxiliary functions for selenium CTs

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import selenium.webdriver.common.action_chains
import selenium.common.exceptions

#
# N9 - Agenda
# 

import datetime

import cfgDB
import aux
import expressomailModule

#############################################################
# all tests for this module
def allTests(mainCfg,logger):
    CTV3_189(mainCfg,logger)

#############################################################
#CTV3-189:F13-Permitir criação de agendamento por tipo pessoal

def CTV3_189(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        msg = cfgDB.getDict('CTV3_7_param')

        # access calendar module
        aux.accessModule(mainCfg,driver,u"Calendário")

        logger.save('CTV3_189',u'Permitir criação de agendamento por tipo pessoal','True')        

    except Exception as err:
        logger.save('CTV3_189',u'Permitir criação de agendamento por tipo pessoal',str(type(err))+str(err))

    finally:
        driver.quit()


#############################################################
