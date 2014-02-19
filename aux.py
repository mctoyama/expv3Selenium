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

import selenium.common.exceptions

import couchdb

import configDB

#############################################################
# functions that tests login
def login(driver,url,language,username,passwd,lastName):

    try:

        server = couchdb.Server()
        db = server[configDB.dbname()]
        doc = db[configDB.configDoc()]

        # go to expressov3 home
        driver.get(url)

        # checking language
        # waiting for page reload with correct language
        while True:

            if driver.title == 'Expresso 3.0 - Por favor, insira seus dados de login':
                break

            # choosing language if not portuguese
            path = "//div/img"
            WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
            localeButton = driver.find_element_by_xpath(path)
            localeButton.click()

            path = ".x-combo-list-item"
            WebDriverWait(driver, doc['timeout']).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,path)))
            languagesList = driver.find_elements_by_css_selector(path)
            for i in languagesList:
                if i.text == language:
                    i.click()
                    break

            # wait for loading portuguese language
            path = "//div[2]/span"
            WebDriverWait(driver, doc['timeout']).until_not(EC.visibility_of_element_located((By.XPATH,path)))

            # waiting for loading portuguese window title
            WebDriverWait(driver, doc['timeout']).until(EC.title_contains('Por favor, insira seus dados de login'))

        # find the element that's username 
        path = "//div[3]/div/input"
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
        inputUsername = driver.find_element_by_xpath(path)
        inputUsername.send_keys(username)
    
        # find the element that's password
        path = "//div[4]/div/input"
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
        inputUserpasswd = driver.find_element_by_xpath(path)
        inputUserpasswd.send_keys(passwd)
    
        # find the element that's login button
        path = "//button"
        WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
        inputLoginbutton = driver.find_element_by_xpath(path)
        inputLoginbutton.click()

        if lastName is not None:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the user's lastName
            path = "//td[2]/table/tbody/tr/td[2]/em/button"
            WebDriverWait(driver, doc['timeout']).until(EC.text_to_be_present_in_element((By.XPATH,path),lastName))
        else:
            # check for error in login
            path = '//div[2]/span'
            WebDriverWait(driver, doc['timeout']).until(EC.text_to_be_present_in_element((By.XPATH,path),u'Usuário e/ou senha incorretos!'))
        
    except Exception as err:
       raise err

#############################################################
# creates web driver for given browser - look at couchdb[configDB.configDoc()]['webdriver']
def createWebDriver():
    
    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    if doc['webdriver'] == u'Firefox':
        # Create a new instance of the Firefox driver
        return webdriver.Firefox()
    else:
        raise Exception("webdriver not found: "+doc['webdriver'])

#############################################################
# aux 
def openComposeMailWindow(driver,sendMailDoc):

    server = couchdb.Server()
    db = server[configDB.dbname()]
    doc = db[configDB.configDoc()]

    msg = db[sendMailDoc]

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

#############################################################
    
    
