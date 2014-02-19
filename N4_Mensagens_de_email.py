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

#############################################################
# all tests for this module
def allTests(logger):
    CTV3_31(logger)
    CTV3_522(logger)
    CTV3_7(logger)

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
        aux.openComposeMailWindow(driver,'CTV3_31_param')
        logger.save('CTV3_31','True')        

    except Exception as err:
        logger.save('CTV3_31',str(type(err))+str(err))        

    finally:
#        driver.quit()
        pass

#############################################################
#CTV3-522:Salvar MENSAGEM rascunho sem destinatário
def CTV3_522(logger):

    try:
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver()

        server = couchdb.Server()
        db = server[configDB.dbname()]
        doc = db[configDB.configDoc()]
        
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])

        ##########
        # salvar rascunho

        msg = db['CTV3_522_param']

        # waiting for main window
        path = '//td[11]/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))

        # selecting compor
        selectPath = '//div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,selectPath)))
        selectBtn = driver.find_element_by_xpath(selectPath)
        selectBtn.click()

        # wait for compor email window
        windowCompose = driver.window_handles[-1]

        driver.switch_to_window(windowCompose)
        WebDriverWait(driver, doc['timeout']).until(EC.title_contains('Compor mensagem:'))

        # filling subject field
        subjectPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/input'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,subjectPath)))
        subjectElement = driver.find_element_by_xpath(subjectPath)
        subjectElement.send_keys(msg['SUBJECT'])
        subjectElement.send_keys(Keys.ENTER)

        # filling email body
        msgBodyFrame = '//html/body/div/div[2]/div/form/div/div[2]/div/div/div/div/div/div/div/div/div[4]/iframe'
        driver.switch_to_frame(driver.find_element_by_xpath(msgBodyFrame))
        msgPath = '//html/body'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,msgPath)))
        msgEl = driver.find_element_by_xpath(msgPath)
        msgEl.send_keys(msg['BODY'])

        # click salvar rascunho
        driver.switch_to_default_content()

        salvarPath = '//html/body/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[4]/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,salvarPath)))
        salvarEl = driver.find_element_by_xpath(salvarPath)
        salvarEl.click()

        # esperando o salvamento da msg
        waitPath = '//html/body/div[1]/div[4]/div'
        WebDriverWait(driver, doc['timeout']).until_not(EC.visibility_of_element_located((By.XPATH,waitPath)))

        # verificando o salvamento - msg na pasta draft
        driver.close()
        driver.switch_to_window(driver.window_handles[-1])

        # + entrada
        entradaPath = '//html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div/ul/div/li/ul/li[1]/div/img[1]'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,entradaPath)))
        entradaEl = driver.find_element_by_xpath(entradaPath)
        entradaEl.click()

        rascunhoPath = '//html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div/ul/div/li/ul/li[1]/ul/li[4]/div/a/span'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,rascunhoPath)))
        rascunhoEl = driver.find_element_by_xpath(rascunhoPath)
        rascunhoEl.click()

        # checking msg subject
        begin = datetime.datetime.now()

        while True:

            subjectPath = '//tbody/tr/td[5]/div'
            WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,subjectPath)))
            subjectElen = driver.find_element_by_xpath(subjectPath)
        
            if subjectElen.text == msg['SUBJECT']:

                logger.save('CTV3_522','True')
                break

            elif datetime.datetime.now() > begin + datetime.timedelta(seconds=doc['timeout']):

                logger.save('CTV3_522','False - msg not saved in drafts - '+subjectElen.text)
                break

    except Exception as err:
        logger.save('CTV3_522',str(type(err))+str(err))        

    finally:
        driver.quit()    

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

        ##########
        # salvar rascunho

        msg = db['CTV3_7_param']

        # waiting for main window
        path = '//td[11]/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))

        # selecting compor
        selectPath = '//div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,selectPath)))
        selectBtn = driver.find_element_by_xpath(selectPath)
        selectBtn.click()

        # wait for compor email window
        windowCompose = driver.window_handles[-1]

        driver.switch_to_window(windowCompose)
        WebDriverWait(driver, doc['timeout']).until(EC.title_contains('Compor mensagem:'))

        # filling subject field
        subjectPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/input'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,subjectPath)))
        subjectElement = driver.find_element_by_xpath(subjectPath)
        subjectElement.send_keys(msg['SUBJECT'])
        subjectElement.send_keys(Keys.ENTER)

        # filling email body
        msgBodyFrame = '//html/body/div/div[2]/div/form/div/div[2]/div/div/div/div/div/div/div/div/div[4]/iframe'
        driver.switch_to_frame(driver.find_element_by_xpath(msgBodyFrame))
        msgPath = '//html/body'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,msgPath)))
        msgEl = driver.find_element_by_xpath(msgPath)
        msgEl.send_keys(msg['BODY'])

        # click salvar rascunho
        driver.switch_to_default_content()

        salvarPath = '//html/body/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[4]/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,salvarPath)))
        salvarEl = driver.find_element_by_xpath(salvarPath)
        salvarEl.click()

        # esperando o salvamento da msg
        waitPath = '//html/body/div[1]/div[4]/div'
        WebDriverWait(driver, doc['timeout']).until_not(EC.visibility_of_element_located((By.XPATH,waitPath)))

        # verificando o salvamento - msg na pasta draft
        driver.close()
        driver.switch_to_window(driver.window_handles[-1])

        # + entrada
        entradaPath = '//html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div/ul/div/li/ul/li[1]/div/img[1]'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,entradaPath)))
        entradaEl = driver.find_element_by_xpath(entradaPath)
        entradaEl.click()

        rascunhoPath = '//html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[3]/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div/ul/div/li/ul/li[1]/ul/li[4]/div/a/span'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,rascunhoPath)))
        rascunhoEl = driver.find_element_by_xpath(rascunhoPath)
        rascunhoEl.click()

        # checking msg subject
        begin = datetime.datetime.now()

        while True:

            subjectPath = '//tbody/tr/td[5]/div'
            WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,subjectPath)))
            subjectElen = driver.find_element_by_xpath(subjectPath)
        
            if subjectElen.text == msg['SUBJECT']:

                action = selenium.webdriver.common.action_chains.ActionChains(driver)
                action.double_click(subjectElen)
                action.perform()

                break

            elif datetime.datetime.now() > begin + datetime.timedelta(seconds=doc['timeout']):

                logger.save('CTV3_7','False - msg not saved in drafts - '+subjectElen.text)
                break

        # switch to compose window
        begin = datetime.datetime.now()

        windowCompose = None

        while True:
            
            if datetime.datetime.now() > begin + datetime.timedelta(seconds=doc['timeout']):

                raise Exception('erro de timeout enquanto carrega janela para compor msg')

            elif len(driver.window_handles) == 2:

                windowCompose = driver.window_handles[-1]
                driver.switch_to_window(windowCompose)
                WebDriverWait(driver, doc['timeout']).until(EC.title_contains('Compor mensagem:'))
                break

        # filling TO field
        toPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/input'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,toPath)))
        toElement = driver.find_element_by_xpath(toPath)
        toElement.send_keys(msg['TO'])

        selPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/span/img[2]'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,selPath)))
        selElement = driver.find_element_by_xpath(selPath)
        selElement.click()

        try:
            okClass = 'search-item'
            WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.CLASS_NAME,okClass)))
            for el in driver.find_elements_by_class_name(okClass):
                tmp = el.find_element_by_xpath('//b')
                if tmp.text == msg['TO']:
                    notFound = False
                    tmp.click()
                    break

        except selenium.common.exceptions.TimeoutException as err:
            toPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/input'
            WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,toPath)))
            toElement = driver.find_element_by_xpath(toPath)
            toElement.send_keys(Keys.ENTER)

        # clicking send
        driver.switch_to_default_content()

        sendPath = '//html/body/div[1]/div[2]/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,sendPath)))
        sendElement = driver.find_element_by_xpath(sendPath)
        sendElement.click()

        # waiting for closing compose window
        # selecting main window
        while True:

            try:
                WebDriverWait(driver, doc['timeout']).until( lambda driver: windowCompose not in driver.window_handles[-1])
                break
            
            except selenium.common.exceptions.TimeoutException as err:
                pass
        
        driver.switch_to_window(driver.window_handles[-1])
        logger.save('CTV3_7','True')        

    except Exception as err:
        logger.save('CTV3_7',str(type(err))+str(err))        

    finally:
        driver.quit()

#############################################################
