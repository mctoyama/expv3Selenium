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
import configDB

#############################################################
# all tests for this module
def allTests(logger):
    CTV3_8(logger)
    CTV3_7(logger)
    CTV3_31(logger)
    CTV3_522(logger)

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
        aux.openComposeMailWindow(driver,'CTV3_8_param')
        logger.save('CTV3_8','True')        

    except Exception as err:
        logger.save('CTV3_8',str(type(err))+str(err))        

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
        aux.openComposeMailWindow(driver,'CTV3_31_param')
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
        
        aux.login(driver,doc['url'],doc['language'],doc['username'],doc['passwd'],doc['lastName'])

        ##########
        # salvar rascunho

        msg = db['CTV3_522_param']

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

        # filling subject field
        subjectConstant = msg['SUBJECT'] + str(datetime.datetime.now())

        subjectPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/input'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,subjectPath)))
        subjectElement = driver.find_element_by_xpath(subjectPath)
        subjectElement.send_keys(subjectConstant)
        subjectElement.send_keys(Keys.ENTER)

        # filling email body
        msgBodyFrame = 'iframe'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.TAG_NAME,msgBodyFrame)))
        driver.switch_to_frame(driver.find_element_by_tag_name(msgBodyFrame))

        msgPath = '//html/body'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,msgPath)))
        msgEl = driver.find_element_by_xpath(msgPath)
        msgEl.send_keys(msg['BODY'])
        msgEl.send_keys(Keys.ENTER)

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

        driver.switch_to_window(driver.window_handles[0])

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
                    break

            except selenium.common.exceptions.ElementNotVisibleException as err:
                pass

            except Exception as err:
                raise Exception('CTV3_522','False - msg not saved in drafts - '+msg['SUBJECT'])

        logger.save('CTV3_522','True')

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

        msg = db['CTV3_7_param']

        ##########
        # salvar rascunho
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

        # filling subject field
        subjectConstant = msg['SUBJECT'] + str(datetime.datetime.now())

        subjectPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/input'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,subjectPath)))
        subjectElement = driver.find_element_by_xpath(subjectPath)
        subjectElement.send_keys(subjectConstant)
        subjectElement.send_keys(Keys.ENTER)

        # filling email body
        msgBodyFrame = 'iframe'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.TAG_NAME,msgBodyFrame)))
        driver.switch_to_frame(driver.find_element_by_tag_name(msgBodyFrame))

        msgPath = '//html/body'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,msgPath)))
        msgEl = driver.find_element_by_xpath(msgPath)
        msgEl.send_keys(msg['BODY'])
        msgEl.send_keys(Keys.ENTER)

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

        driver.switch_to_window(driver.window_handles[0])

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

                    action = selenium.webdriver.common.action_chains.ActionChains(driver)
                    action.double_click( driver.find_element_by_xpath(subjectPath) )
                    action.perform()
                    break

            except selenium.common.exceptions.ElementNotVisibleException as err:
                pass

            except Exception as err:
                raise Exception('CTV3_522','False - msg not saved in drafts - '+msg['SUBJECT'])

        # switch to compose window
        windowCompose = None

        WebDriverWait(driver, doc['timeout']).until( lambda driver: len(driver.window_handles) == 2 )

        windowCompose = driver.window_handles[-1]
        driver.switch_to_window(windowCompose)
        WebDriverWait(driver, doc['timeout']).until(EC.title_contains('Compor mensagem:'))
            
        # filling TO field
        toPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/input'
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,toPath)))
        toElement = driver.find_element_by_xpath(toPath)
        toElement.send_keys(msg['TO'])

        try:
            okClass = 'search-item'
            WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.CLASS_NAME,okClass)))
            for el in driver.find_elements_by_class_name(okClass):
                tmp = el.find_element_by_xpath('//b')
                if tmp.text == msg['TO']:
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
        WebDriverWait(driver, doc['timeout']).until(EC.element_to_be_clickable((By.XPATH,sendPath)))
        sendElement = driver.find_element_by_xpath(sendPath)
        sendElement.click()

        # waiting for closing compose window
        # selecting main window
        WebDriverWait(driver, doc['timeout']).until( lambda driver: windowCompose not in driver.window_handles)
        
        driver.switch_to_window(driver.window_handles[0])
        logger.save('CTV3_7','True')        

    except Exception as err:
        logger.save('CTV3_7',str(type(err))+str(err))        

    finally:
        driver.quit()

#############################################################
