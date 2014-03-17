#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

# auxiliary functions for composeMail

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import selenium.common.exceptions

import couchdb
import datetime

import configDB

#############################################################
# clica no botão compor msg e espera a janela abrir
# retorna o window id para a nova janela

def clickCompose(driver,sendMailDoc):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    msg = db[sendMailDoc]

    try:
        # waiting for loading list of inbox messages
        subjectPath = '//tbody/tr/td[5]/div'
        WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,subjectPath)))

    except selenium.common.exceptions.TimeoutException as err:

        # if there is no message in the list search for "no messages" message
        subjectPath = '//div/div/div[2]/div/div/div/div/div/div[2]/div/div'
        WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,subjectPath)))

    # selecting compor
    selectPath = '//div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,selectPath)))
    selectBtn = driver.find_element_by_xpath(selectPath)
    selectBtn.click()

    # wait for compor email window
    WebDriverWait(driver, doc['timeout']).until( lambda driver: len(driver.window_handles) == 2 )

    windowCompose = driver.window_handles[-1]

    driver.switch_to_window(windowCompose)
    WebDriverWait(driver, doc['timeout']).until(EC.title_contains('Compor mensagem:'))
    
    return windowCompose

#############################################################
# preenche campo To

def fillTo(driver,sendMailDoc):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    msg = db[sendMailDoc]

    # filling TO field
    toPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/input'
    WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,toPath)))
    toElement = driver.find_element_by_xpath(toPath)
    toElement.send_keys(msg['TO'])

    # checking if search button is clickable
    findButtonPath = '//html/body/div[10]/div[2]/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button'

    # debug
    try:
        driver.find_element_by_xpath(findButtonPath)

    except selenium.common.exceptions.NoSuchElementException as err:

        selPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/span/img[2]'
        WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,selPath)))
        selElement = driver.find_element_by_xpath(selPath)
        selElement.click()

    try:
        okClass = 'search-item'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.CLASS_NAME,okClass)))
        for el in driver.find_elements_by_class_name(okClass):
            WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,'//b')))
            tmp = el.find_element_by_xpath('//b')
            if tmp.text == msg['TO']:
                tmp.click()
                break

    except selenium.common.exceptions.TimeoutException as err:

        toPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/input'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,toPath)))
        toElement = driver.find_element_by_xpath(toPath)
        toElement.send_keys(Keys.ENTER)



#############################################################
# preenche campo Subject

def fillSubject(driver,sendMailDoc):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    msg = db[sendMailDoc]

    # filling subject field
    subjectPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/input'
    WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,subjectPath)))
    subjectElement = driver.find_element_by_xpath(subjectPath)

    subjectConstant = msg['SUBJECT']+' -- '+str(datetime.datetime.now())

    subjectElement.send_keys(subjectConstant)
    subjectElement.send_keys(Keys.ENTER)

    return subjectConstant

#############################################################
# preenche campo body

def fillBody(driver,sendMailDoc):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    msg = db[sendMailDoc]

    # filling email body
    msgBodyFrame = 'iframe'
    WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.TAG_NAME,msgBodyFrame)))
    driver.switch_to_frame(driver.find_element_by_tag_name(msgBodyFrame))

    msgPath = '//html/body'
    WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,msgPath)))
    msgEl = driver.find_element_by_xpath(msgPath)
    msgEl.send_keys(msg['BODY'])
    msgEl.send_keys(Keys.ENTER)

#############################################################
# clica no botão enviar email

def clickSend(driver,sendMailDoc,windowCompose):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    msg = db[sendMailDoc]

    # clicking send
    driver.switch_to_default_content()

    sendPath = '//html/body/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,sendPath)))
    sendElement = driver.find_element_by_xpath(sendPath)
    sendElement.click()

    # waiting for closing compose window
    # selecting main window
    WebDriverWait(driver, doc['timeout']).until( lambda driver: windowCompose not in driver.window_handles)
    driver.switch_to_window(driver.window_handles[0])

#############################################################
# clicar em salvar rascunho

def clickSaveDraft(driver,sendMailDoc):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    msg = db[sendMailDoc]

    driver.switch_to_default_content()

    salvarPath = '//html/body/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[4]/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,salvarPath)))
    salvarEl = driver.find_element_by_xpath(salvarPath)
    salvarEl.click()

    # esperando o salvamento da msg
    waitPath = '//html/body/div[1]/div[4]/div'
    WebDriverWait(driver, doc['timeout']).until_not(EC.visibility_of_element_located((By.XPATH,waitPath)))
    
    driver.close()
    
    driver.switch_to_window(driver.window_handles[0])

#############################################################
# checar mensagem por assunto na pasta draft
# retorna o elemento caso sucesso
# throws exception em caso de erro

def checkDraftFolderForMessageSubject(driver,sendMailDoc,subjectConstant):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    msg = db[sendMailDoc]

    # expanding "+ entrada"
    entradaPath = '//html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div/ul/div/li/ul/li[1]/div/img[1]'
    WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,entradaPath)))
    entradaEl = driver.find_element_by_xpath(entradaPath)
    entradaEl.click()

        # expanding "+ rascunho"
    rascunhoPath = '//html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div/ul/div/li/ul/li[1]/ul/li[4]/div/a/span'
    WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,rascunhoPath)))
    rascunhoEl = driver.find_element_by_xpath(rascunhoPath)
    rascunhoEl.click()

    # checking msg subject

    while True:

        try:
            subjectPath = '//tbody/tr/td[5]/div'
            WebDriverWait(driver, doc['timeout']).until(EC.text_to_be_present_in_element((By.XPATH,subjectPath),subjectConstant))
            
            if subjectConstant == driver.find_element_by_xpath(subjectPath).text:
                return driver.find_element_by_xpath(subjectPath)
            
        except selenium.common.exceptions.ElementNotVisibleException as err:
            pass

        except Exception as err:
            raise Exception('False - msg not saved in drafts - '+subjectConstant)


#############################################################
# selects the inbox folder

def selectInbox(driver):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    # + Inbox
    plusInboxPath = '//html/body/div/div[3]/div/div/div/div[4]/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/ul/div/li/ul/li/div/img'
    WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,plusInboxPath)))
    plusEl = driver.find_element_by_xpath(plusInboxPath)

    # checking if is a + or a -
    cssclass = plusEl.get_attribute('class').split(' ')
    if 'x-tree-elbow-plus' in cssclass:
        plusEl.click()

    # click inbox
    inboxPath = '//html/body/div/div[3]/div/div/div/div[4]/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/ul/div/li/ul/li/div/a'
    WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,inboxPath)))
    inboxEl = driver.find_element_by_xpath(inboxPath)
    inboxEl.click()

#############################################################
# returns a list of all mail subjects in inbox

def listInboxMessagesSubject(driver):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    # select inbox
    selectInbox(driver)

    try:

        zeroMessagesPath = '//html/body/div[2]/div[3]/div/div/div/div[4]/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,zeroMessagesPath)))
        zeroEl = driver.find_element_by_xpath(zeroMessagesPath)

        if zeroEl.text == 'Nenhum dado para exibir':
            return []

    except selenium.common.exceptions.TimeoutException as err:

        messageSubjectPath = '//tbody/tr/td[5]/div'
        WebDriverWait(driver, doc['timeout']).until(EC.presence_of_all_elements_located((By.XPATH,messageSubjectPath)))

        ret = []

        for el in driver.find_elements_by_xpath(messageSubjectPath):
            ret.append( el.text )

        return ret

#############################################################
# selects an messages in Inbox

def inboxSelectMessage(driver,subject):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    # select inbox
    selectInbox(driver)

    try:

        zeroMessagesPath = '//html/body/div[2]/div[3]/div/div/div/div[4]/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,zeroMessagesPath)))
        zeroEl = driver.find_element_by_xpath(zeroMessagesPath)

        if zeroEl.text == 'Nenhum dado para exibir':
            return False

    except selenium.common.exceptions.TimeoutException as err:

        messageSubjectPath = '//tbody/tr/td[5]/div'
        WebDriverWait(driver, doc['timeout']).until(EC.presence_of_all_elements_located((By.XPATH,messageSubjectPath)))

        for el in driver.find_elements_by_xpath(messageSubjectPath):
            if el.text == subject:
                el.click()
                return True

        return False
    
#############################################################
# press delete msg button on email module

def clickDelete(driver,subjectConstant):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    deletePath = '//td[2]/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,deletePath)))
    deleteEl = driver.find_element_by_xpath(deletePath)
    deleteEl.click()

    # must confirme delete
    try:
        confirmPath = '//html/body/div[25]/div[2]/div[1]/div/div/div/div/div[2]/span'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,confirmPath)))

        yesPath = '//html/body/div[25]/div[2]/div[2]/div/div/div/div[1]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,yesPath)))
        yesEl = driver.find_element_by_xpath(yesPath)
        yesEl.click()

    except selenium.common.exceptions.TimeoutException as err:
        pass

    # wait for delete to complete    
    if not subjectConstant in listInboxMessagesSubject(driver):
        return True
    else:
        return False

#############################################################
# opens an msg from Inbox in a new window

def openMessageFromInbox(driver,subjectConstant):
  
    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    # select inbox
    selectInbox(driver)

    try:

        zeroMessagesPath = '//html/body/div[2]/div[3]/div/div/div/div[4]/div/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,zeroMessagesPath)))
        zeroEl = driver.find_element_by_xpath(zeroMessagesPath)

        if zeroEl.text == 'Nenhum dado para exibir':
            return False

    except selenium.common.exceptions.TimeoutException as err:

        messageSubjectPath = '//tbody/tr/td[5]/div'
        WebDriverWait(driver, doc['timeout']).until(EC.presence_of_all_elements_located((By.XPATH,messageSubjectPath)))

        for el in driver.find_elements_by_xpath(messageSubjectPath):

            if el.text == subjectConstant:

                action = selenium.webdriver.common.action_chains.ActionChains(driver)
                action.double_click( el )
                action.perform()

                # switch to compose window
                windowCompose = None

                WebDriverWait(driver, doc['timeout']).until( lambda driver: len(driver.window_handles) == 2 )

                windowCompose = driver.window_handles[-1]
                driver.switch_to_window(windowCompose)
                WebDriverWait(driver, doc['timeout']).until(EC.title_contains(subjectConstant))

                return windowCompose

        return None
    
#############################################################
# click delete in opened message
def clickDeleteInOpenedMessage(driver,window):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    # clicks delete button
    deletePath = '//button'
    WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,deletePath)))    
    deleteEl = driver.find_element_by_xpath(deletePath)
    deleteEl.click()

    # confirm delete
    try:
        confirmPath = '//div[2]/span'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,confirmPath)))

        yesPath = '//td/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,yesPath)))
        yesEl = driver.find_element_by_xpath(yesPath)
        yesEl.click()

    except selenium.common.exceptions.TimeoutException as err:
        pass


    # waiting for closing message window
    # selecting main window
    WebDriverWait(driver, doc['timeout']).until( lambda driver: window not in driver.window_handles)
    driver.switch_to_window(driver.window_handles[0])

#############################################################
