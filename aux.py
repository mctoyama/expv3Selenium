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

import couchdb

# functions that tests login
def login(driver,url,language,username,passwd,lastName):

    try:

        server = couchdb.Server()
        db = server['test']
        doc = db['config']

        # go to expressov3 home
        driver.get(url)

        # checking language
        # waiting for page reload with correct language
        while True:

            path = '//div[3]/label'
            WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
            usuarioElement = driver.find_element_by_xpath(path)
            
            path = '//div[4]/label'
            WebDriverWait(driver, doc['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
            senhaElement = driver.find_element_by_xpath(path)

            if usuarioElement.text == u'Usuário:' and senhaElement.text == u'Senha:' :
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
                    
            # wait for loading portuguese language
            path = "//div[2]/span"
            WebDriverWait(driver, doc['timeout']).until_not(EC.visibility_of_element_located((By.XPATH,path)))

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

# creates web driver for given browser - look at couchdb['config']['webdriver']
def createWebDriver():
    
    server = couchdb.Server()
    db = server['test']
    doc = db['config']

    if doc['webdriver'] == u'Firefox':
        # Create a new instance of the Firefox driver
        return webdriver.Firefox()
    else:
        raise Exception("webdriver not found: "+doc['webdriver'])

