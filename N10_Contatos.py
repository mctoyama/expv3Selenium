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
import collections


#############################################################
# all tests for this module
def allTests(mainCfg,logger):
    CTV3_179(mainCfg,logger)
    CTV3_178(mainCfg,logger)
    CTV3_180(mainCfg,logger)
    CTV3_192(mainCfg,logger)


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


#############################################################
# View contact information
def CTV3_180(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        timeout =  mainCfg['timeout']

        selectedModuleText = 'Catálogos de Endereços'

        aux.accessModule(mainCfg,driver,selectedModuleText)

        # select a contact, returning the selected contact row path
        contactInfoRowPath = addressbookModule.selectContact(driver,timeout)

        # compare the contact info with the info displayed in the bottom section
        addressbookModule.compareContactInfoSections(driver,timeout,contactInfoRowPath)

        logger.save('CTV3_180',u'Visualizar informações do contato','True')

    except Exception as err:
        logger.save('CTV3_180',u'Visualizar informações do contato',str(type(err))+str(err))        

    finally:
        driver.quit()

#############################################################
# Edit contact information
def CTV3_192(mainCfg,logger):
    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        timeout =  mainCfg['timeout']

        selectedModuleText = 'Catálogos de Endereços'

        aux.accessModule(mainCfg,driver,selectedModuleText)

        # select a contact, returning the selected contact row path
        contactInfoRowPath = addressbookModule.selectContact(driver,timeout)

        # get the contact information
        oldContactInfoReg = addressbookModule.getContactInfo(driver,timeout,contactInfoRowPath)

        contactInfoReg = collections.namedtuple('contactInfoReg',['nameText','lastNameText','companyText','companyUnitText','phoneNumberText','cellPhoneNumberText','faxText','privatePhoneNumberText','privCellPhoneNumberText','privateFaxText','emailText','privateEmailText','websiteText','streetCompanyText','regionCompanyText','postalCodeCompanyText','cityCompanyText','countryCompanyText','streetPrivText','regionPrivText','postalCodePrivText','cityPrivText','countryPrivText'])

        newContactInfoReg = contactInfoReg(oldContactInfoReg.nameText+'new', oldContactInfoReg.lastNameText+'new', oldContactInfoReg.companyText+'new', oldContactInfoReg.companyUnitText, oldContactInfoReg.phoneNumberText, oldContactInfoReg.cellPhoneNumberText, oldContactInfoReg.faxText, oldContactInfoReg.privatePhoneNumberText, oldContactInfoReg.privCellPhoneNumberText, oldContactInfoReg.privateFaxText, oldContactInfoReg.emailText, oldContactInfoReg.privateEmailText, oldContactInfoReg.websiteText, oldContactInfoReg.streetCompanyText, oldContactInfoReg.regionCompanyText, oldContactInfoReg.postalCodeCompanyText, oldContactInfoReg.cityCompanyText+'new', oldContactInfoReg.countryCompanyText, oldContactInfoReg.streetPrivText, oldContactInfoReg.regionPrivText, oldContactInfoReg.postalCodePrivText, oldContactInfoReg.cityPrivText, oldContactInfoReg.countryPrivText)

        # set the contact info with new info
        addressbookModule.setContactInfo(driver,timeout,contactInfoRowPath,newContactInfoReg)

        contactInfoRow = driver.find_element_by_xpath(contactInfoRowPath)

        if ((oldContactInfoReg.nameText + ' ' +  oldContactInfoReg.lastNameText) == contactInfoRow.find_element_by_xpath("//div[contains(@class,'x-grid3-cell-inner') and contains(@class,'x-grid3-col-n_fileas')]").text):
            raise Exception(u"Nome não atualizado")

        if (oldContactInfoReg.companyText == contactInfoRow.find_element_by_xpath("//div[contains(@class,'x-grid3-cell-inner') and contains(@class,'x-grid3-col-org_name')]").text):
            raise Exception(u"Empresa não atualizada")

        if (oldContactInfoReg.cityCompanyText == contactInfoRow.find_element_by_xpath("//div[contains(@class,'x-grid3-cell-inner') and contains(@class,'x-grid3-col-adr_one_locality')]").text):
            raise Exception(u"Localidade da empresa não atualizada")

        logger.save('CTV3_192',u'Editar informações do contato','True')

    except Exception as err:
        logger.save('CTV3_192',u'Editar informações do contato',str(type(err))+str(err))        

    finally:
        driver.quit()


