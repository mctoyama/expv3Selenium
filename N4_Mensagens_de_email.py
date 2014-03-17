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
# N4 - Mensagens de email
# 

import couchdb
import datetime

import configDB
import aux
import composeMail

#############################################################
# all tests for this module
def allTests(logger):
    CTV3_7(logger)
    CTV3_8(logger)
    CTV3_18(logger)
    CTV3_20(logger)
    CTV3_31(logger)
    CTV3_522(logger)

#############################################################
#CTV3-7:Enviar Mensagens da pasta "Drafts"

def CTV3_7(logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver()

        server = couchdb.Server()
        db = server[configDB.dbname()]
        doc = db[configDB.configDoc()]
        
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])

        msg = db['CTV3_7_param']


        # clica no botão compor msg e espera a janela abrir
        composeMail.clickCompose(driver,'CTV3_7_param')

        # preenche campo Subject
        subjectConstant = composeMail.fillSubject(driver,'CTV3_7_param')

        # preenche campo body
        composeMail.fillBody(driver,'CTV3_7_param')
        
        # click salvar rascunho
        composeMail.clickSaveDraft(driver,'CTV3_7_param')

        # checar mensagem por assunto na pasta draft
        msgEl = composeMail.checkDraftFolderForMessageSubject(driver,'CTV3_7_param',subjectConstant)

        action = selenium.webdriver.common.action_chains.ActionChains(driver)
        action.double_click( msgEl )
        action.perform()

        # switch to compose window
        windowCompose = None

        WebDriverWait(driver, doc['timeout']).until( lambda driver: len(driver.window_handles) == 2 )

        windowCompose = driver.window_handles[-1]
        driver.switch_to_window(windowCompose)
        WebDriverWait(driver, doc['timeout']).until(EC.title_contains('Compor mensagem:'))
            
        # filling TO field
        composeMail.fillTo(driver,'CTV3_7_param')

        # clicking send
        composeMail.clickSend(driver,'CTV3_7_param',windowCompose)

        logger.save('CTV3_7','True')        

    except Exception as err:
        logger.save('CTV3_7',str(type(err))+str(err))        

    finally:
        driver.quit()


#############################################################
# CTV3-8:Criar Mensagem apenas com To
def CTV3_8(logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver()

        server = couchdb.Server()
        db = server[configDB.dbname()]
        doc = db[configDB.configDoc()]
        
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])

        window = composeMail.clickCompose(driver,'CTV3_8_param')
        composeMail.fillTo(driver,'CTV3_8_param')
        composeMail.fillSubject(driver,'CTV3_8_param')
        composeMail.fillBody(driver,'CTV3_8_param')
        composeMail.clickSend(driver,'CTV3_8_param',window)

        logger.save('CTV3_8','True')        

    except Exception as err:
        logger.save('CTV3_8',str(type(err))+str(err))        

    finally:
        driver.quit()
#############################################################
# CTV3-18:Excluir mensagem selecionada
def CTV3_18(logger):
    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver()

        server = couchdb.Server()
        db = server[configDB.dbname()]
        doc = db[configDB.configDoc()]

        msg = db['CTV3_18_param']

        # login
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])

        # compose mail
        window = composeMail.clickCompose(driver,'CTV3_18_param')
        composeMail.fillTo(driver,'CTV3_18_param')
        subjectConstant = composeMail.fillSubject(driver,'CTV3_18_param')
        composeMail.fillBody(driver,'CTV3_18_param')
        composeMail.clickSend(driver,'CTV3_18_param',window)

        # delete mail
        msgSubjectList = composeMail.listInboxMessagesSubject(driver)

        if subjectConstant in msgSubjectList:

            if composeMail.inboxSelectMessage(driver,subjectConstant):
                if not composeMail.clickDelete(driver,subjectConstant):
                    raise Exception('Could not delete message: '+msg['SUBJECT'])
            else:
                raise Exception('Could not select the message: '+msg['SUBJECT'])

        else:
            raise Exception('subject '+msg['SUBJECT']+' is not present in INBOX')

        logger.save('CTV3_18','True')

    except Exception as err:
        logger.save('CTV3_18',str(type(err))+str(err))        

    finally:
        driver.quit()


#############################################################
# CTV3-20:Excluir mensagem aberta

def CTV3_20(logger):

    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver()

        server = couchdb.Server()
        db = server[configDB.dbname()]
        doc = db[configDB.configDoc()]

        msg = db['CTV3_20_param']

        # login
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])

        # compose mail
        window = composeMail.clickCompose(driver,'CTV3_20_param')
        composeMail.fillTo(driver,'CTV3_20_param')
        subjectConstant = composeMail.fillSubject(driver,'CTV3_20_param')
        composeMail.fillBody(driver,'CTV3_20_param')
        composeMail.clickSend(driver,'CTV3_20_param',window)

        # delete mail
        msgSubjectList = composeMail.listInboxMessagesSubject(driver)

        if subjectConstant in msgSubjectList:

            # open msg in new window
            window = composeMail.openMessageFromInbox(driver,subjectConstant)

            if window is None:
                raise Exception('Could not open message: '+msg['SUBJECT'])
            else:
                # click delete in opened message
                composeMail.clickDeleteInOpenedMessage(driver,window)

        logger.save('CTV3_20','True')


    except Exception as err:
        logger.save('CTV3_20',str(type(err))+str(err))        

    finally:
        driver.quit()

#############################################################
# CTV3-31:Enviar Mensagens
def CTV3_31(logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver()

        server = couchdb.Server()
        db = server[configDB.dbname()]
        doc = db[configDB.configDoc()]
        
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])

        window = composeMail.clickCompose(driver,'CTV3_31_param')
        composeMail.fillTo(driver,'CTV3_31_param')
        composeMail.fillSubject(driver,'CTV3_31_param')
        composeMail.fillBody(driver,'CTV3_31_param')
        composeMail.clickSend(driver,'CTV3_31_param',window)

        logger.save('CTV3_31','True')        

    except Exception as err:
        logger.save('CTV3_31',str(type(err))+str(err))        

    finally:
        driver.quit()

#############################################################
#CTV3-522:Salvar MENSAGEM rascunho sem destinatário

def CTV3_522(logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver()

        server = couchdb.Server()
        db = server[configDB.dbname()]
        doc = db[configDB.configDoc()]

        msg = db['CTV3_522_param']
        
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])

        # click compose msg
        composeMail.clickCompose(driver,'CTV3_522_param')

        # filling subject field
        subjectConstant = composeMail.fillSubject(driver,'CTV3_522_param')

        # filling email body
        composeMail.fillBody(driver,'CTV3_522_param')

        # click salvar rascunho
        composeMail.clickSaveDraft(driver,'CTV3_522_param')

        # checando se a mensagem foi salva na pasta draft
        composeMail.checkDraftFolderForMessageSubject(driver,'CTV3_522_param',subjectConstant)

        logger.save('CTV3_522','True')

    except Exception as err:
        logger.save('CTV3_522',str(type(err))+str(err))        

    finally:
        driver.quit()    

#############################################################
