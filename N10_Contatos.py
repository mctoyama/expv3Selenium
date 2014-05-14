#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
# N10 - Catálogo de Endereços - Contatos ExpressoV3
# 

import datetime

import cfgDB
import aux

import addressbookModule


#############################################################
# all tests for this module
def allTests(mainCfg,logger):
    CTV3_179(mainCfg,logger)
    CTV3_178(mainCfg,logger)


#############################################################
# testing the access to the Addressbook Module
def CTV3_179(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        selectedModuleText = 'Catálogos de Endereços'

        aux.accessModule(mainCfg,driver,selectedModuleText)

        logger.save('CTV3_179',u'Acessar o Módulo de Contatos','True')

    except Exception as err:
        logger.save('CTV3_179',u'Acessar o Módulo de Contatos',unicode(type(err))+unicode(err))        

    finally:
        driver.quit()


#############################################################
# Add a contact
def CTV3_178(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        msg = cfgDB.getDict('CTV3_178_param.xml')
        timeout =  mainCfg['timeout']

        selectedModuleText = 'Catálogos de Endereços'

        aux.accessModule(mainCfg,driver,selectedModuleText)

        # add a contact
        addContactWindow = addressbookModule.clickAddContact(driver,timeout)

        addressbookModule.fillLastName(driver,timeout,msg['SOBRENOME'])
        addressbookModule.fillCompany(driver,timeout,msg['EMPRESA'])
        addressbookModule.clickOk(driver,addContactWindow,timeout)

        # waiting for closing compose window
        # selecting main window
        WebDriverWait(driver, timeout).until( lambda driver: addContactWindow not in driver.window_handles)
        driver.switch_to_window(driver.window_handles[0])

        logger.save('CTV3_178','Adicionar um contato','True')

    except Exception as err:
        logger.save('CTV3_178','Adicionar um contato',unicode(type(err))+unicode(err))        

    finally:
        driver.quit()

