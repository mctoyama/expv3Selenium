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

import datetime

import cfgDB
import aux
import composeMail

#############################################################
# all tests for this module
def allTests(mainCfg,logger):
    CTV3_7(mainCfg,logger)
    CTV3_8(mainCfg,logger)
    CTV3_11(mainCfg,logger)
    CTV3_18(mainCfg,logger)
    CTV3_20(mainCfg,logger)
    CTV3_31(mainCfg,logger)
    CTV3_506(mainCfg,logger)
    CTV3_522(mainCfg,logger)

#############################################################
#CTV3-7:Enviar Mensagens da pasta "Drafts"

def CTV3_7(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        msg = cfgDB.getDict('CTV3_7_param')

        # clica no botão compor msg e espera a janela abrir
        composeMail.clickCompose(mainCfg,driver,'CTV3_7_param')

        # preenche campo Subject
        subjectConstant = composeMail.fillSubject(mainCfg,driver,'CTV3_7_param')

        # preenche campo body
        composeMail.fillBody(mainCfg,driver,'CTV3_7_param')
        
        # click salvar rascunho
        composeMail.clickSaveDraft(mainCfg,driver,'CTV3_7_param')

        # checar mensagem por assunto na pasta draft
        msgEl = composeMail.checkDraftFolderForMessageSubject(mainCfg,driver,'CTV3_7_param',subjectConstant)

        action = selenium.webdriver.common.action_chains.ActionChains(driver)
        action.double_click( msgEl )
        action.perform()

        # switch to compose window
        windowCompose = None

        WebDriverWait(driver, mainCfg['timeout']).until( lambda driver: len(driver.window_handles) == 2 )

        windowCompose = driver.window_handles[-1]
        driver.switch_to_window(windowCompose)
        WebDriverWait(driver, mainCfg['timeout']).until(EC.title_contains('Compor mensagem:'))
            
        # filling TO field
        composeMail.fillToOption(mainCfg,driver,'CTV3_7_param','TO')

        # clicking send
        composeMail.clickSend(mainCfg,driver,'CTV3_7_param',windowCompose)

        logger.save('CTV3_7','Enviar Mensagens da pasta "Drafts"','True')        

    except Exception as err:
        logger.save('CTV3_7','Enviar Mensagens da pasta "Drafts"',str(type(err))+str(err))

    finally:
        driver.quit()


#############################################################
# CTV3-8:Criar Mensagem apenas com To
def CTV3_8(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        window = composeMail.clickCompose(mainCfg,driver,'CTV3_8_param')
        composeMail.fillToOption(mainCfg,driver,'CTV3_8_param',"TO")
        composeMail.fillSubject(mainCfg,driver,'CTV3_8_param')
        composeMail.fillBody(mainCfg,driver,'CTV3_8_param')
        composeMail.clickSend(mainCfg,driver,'CTV3_8_param',window)

        logger.save('CTV3_8','Criar Mensagem apenas com To','True')        

    except Exception as err:
        logger.save('CTV3_8','Criar Mensagem apenas com To',str(type(err))+str(err))

    finally:
        driver.quit()

#############################################################
# CTV3-11:Criar Mensagem apenas com Cc
def CTV3_11(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)
        aux.login(mainCfg,driver)
        window = composeMail.clickCompose(mainCfg,driver,'CTV3_11_param')
        composeMail.fillToOption(mainCfg,driver,'CTV3_11_param','Cc')
        composeMail.fillSubject(mainCfg,driver,'CTV3_11_param')
        composeMail.fillBody(mainCfg,driver,'CTV3_11_param')
        composeMail.clickSend(mainCfg,driver,'CTV3_11_param',window)

        logger.save('CTV3_11','Criar Mensagem apenas com Cc','True') 

    except Exception as err:
        logger.save('CTV3_11','Criar Mensagem apenas com Cc',str(type(err))+str(err))        

    finally:
        driver.quit()

#############################################################
# CTV3-18:Excluir mensagem selecionada
def CTV3_18(mainCfg,logger):
    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        msg = cfgDB.getDict('CTV3_18_param')

        # login
        aux.login(mainCfg,driver)

        # compose mail
        window = composeMail.clickCompose(mainCfg,driver,'CTV3_18_param')
        composeMail.fillToOption(mainCfg,driver,'CTV3_18_param',"TO")
        subjectConstant = composeMail.fillSubject(mainCfg,driver,'CTV3_18_param')
        composeMail.fillBody(mainCfg,driver,'CTV3_18_param')
        composeMail.clickSend(mainCfg,driver,'CTV3_18_param',window)

        # delete mail
        composeMail.clickFolder(mainCfg,driver,"Entrada")
        msgSubjectList = composeMail.listFolderMessagesSubject(mainCfg,driver)

        if subjectConstant in msgSubjectList:

            if composeMail.inboxSelectMessage(mainCfg,driver,subjectConstant):
                if not composeMail.clickDelete(mainCfg,driver,subjectConstant):
                    raise Exception('Could not delete message: '+msg['SUBJECT'])
            else:
                raise Exception('Could not select the message: '+msg['SUBJECT'])

        else:
            raise Exception('subject '+msg['SUBJECT']+' is not present in INBOX')

        logger.save('CTV3_18','Excluir mensagem selecionada','True')

    except Exception as err:
        logger.save('CTV3_18','Excluir mensagem selecionada',str(type(err))+str(err))

    finally:
        driver.quit()


#############################################################
# CTV3-20:Excluir mensagem aberta

def CTV3_20(mainCfg,logger):

    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        msg = cfgDB.getDict('CTV3_20_param')

        # login
        aux.login(mainCfg,driver)

        # compose mail
        window = composeMail.clickCompose(mainCfg,driver,'CTV3_20_param')
        composeMail.fillToOption(mainCfg,driver,'CTV3_20_param',"TO")
        subjectConstant = composeMail.fillSubject(mainCfg,driver,'CTV3_20_param')
        composeMail.fillBody(mainCfg,driver,'CTV3_20_param')
        composeMail.clickSend(mainCfg,driver,'CTV3_20_param',window)

        # delete mail
        composeMail.clickFolder(mainCfg,driver,"Entrada")
        msgSubjectList = composeMail.listFolderMessagesSubject(mainCfg,driver)

        if subjectConstant in msgSubjectList:

            # open msg in new window
            window = composeMail.openMessageFromInbox(mainCfg,driver,subjectConstant)

            if window is None:
                raise Exception('Could not open message: '+msg['SUBJECT'])
            else:
                # click delete in opened message
                composeMail.clickDeleteInOpenedMessage(mainCfg,driver,window)

        logger.save('CTV3_20','Excluir mensagem aberta','True')


    except Exception as err:
        logger.save('CTV3_20','Excluir mensagem aberta',str(type(err))+str(err))        

    finally:
        driver.quit()

#############################################################
# CTV3-31:Enviar Mensagens
def CTV3_31(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        window = composeMail.clickCompose(mainCfg,driver,'CTV3_31_param')
        composeMail.fillToOption(mainCfg,driver,'CTV3_31_param',"TO")
        composeMail.fillSubject(mainCfg,driver,'CTV3_31_param')
        composeMail.fillBody(mainCfg,driver,'CTV3_31_param')
        composeMail.clickSend(mainCfg,driver,'CTV3_31_param',window)

        logger.save('CTV3_31','Enviar Mensagens','True')        

    except Exception as err:
        logger.save('CTV3_31','Enviar Mensagens',str(type(err))+str(err))

    finally:
        driver.quit()
#############################################################
#CTV3-506:Excluir todas as mensagens de uma pasta
def CTV3_506(mainCfg,logger):
    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        msg = cfgDB.getDict('CTV3_506_param')
        
        aux.login(mainCfg,driver)

        # opening folder
        composeMail.clickFolder(mainCfg,driver,msg['folderName'])

        # the accont must hae at least one message for deletion
        if len(composeMail.listFolderMessagesSubject(mainCfg,driver)) == 0:
            raise Exception('Must have at least one message for deletion!')

        # selecting all from page
        composeMail.selectAllFromPage(mainCfg,driver)

        if not composeMail.clickDelete(mainCfg,driver,None):
            raise Exception('Could not delete page')

        logger.save(u'CTV3_506',u'Excluir todas as mensagens de uma pasta',u'True')

    except Exception as err:
        logger.save('CTV3_506','Excluir todas as mensagens de uma pasta',str(type(err))+str(err))        
    finally:
        driver.quit()

#############################################################
#CTV3-522:Salvar MENSAGEM rascunho sem destinatário

def CTV3_522(mainCfg,logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        msg = cfgDB.getDict('CTV3_522_param')
        
        aux.login(mainCfg,driver)

        # click compose msg
        composeMail.clickCompose(mainCfg,driver,'CTV3_522_param')

        # filling subject field
        subjectConstant = composeMail.fillSubject(mainCfg,driver,'CTV3_522_param')

        # filling email body
        composeMail.fillBody(mainCfg,driver,'CTV3_522_param')

        # click salvar rascunho
        composeMail.clickSaveDraft(mainCfg,driver,'CTV3_522_param')

        # checando se a mensagem foi salva na pasta draft
        composeMail.checkDraftFolderForMessageSubject(mainCfg,driver,'CTV3_522_param',subjectConstant)

        logger.save(u'CTV3_522',u'Salvar MENSAGEM rascunho sem destinatário',u'True')

    except Exception as err:
        logger.save(u'CTV3_522',u'Salvar MENSAGEM rascunho sem destinatário',str(type(err))+str(err))

    finally:
        driver.quit()    

#############################################################
