#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

# auxiliary functions for selenium CTs

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import selenium.common.exceptions
import selenium.webdriver.firefox.firefox_profile

#############################################################
# functions that tests login
def login(mainCfg,driver):

    # go to expressov3 home
    driver.get(mainCfg['url'])
    
    # checking language
    # waiting for page reload with correct language
    while True:

        if driver.title == 'Expresso 3.0 - Por favor, insira seus dados de login':
            break

        # choosing language if not portuguese
        path = "//div/img"
        WebDriverWait(driver, mainCfg['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
        localeButton = driver.find_element_by_xpath(path)
        localeButton.click()

        path = ".x-combo-list-item"
        WebDriverWait(driver, mainCfg['timeout']).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,path)))
        languagesList = driver.find_elements_by_css_selector(path)
        for i in languagesList:
            if i.text == mainCfg['language']:
                i.click()
                break

        # wait for loading portuguese language
        path = "//div[2]/span"
        WebDriverWait(driver, mainCfg['timeout']).until_not(EC.visibility_of_element_located((By.XPATH,path)))

        # waiting for loading portuguese window title
        WebDriverWait(driver, mainCfg['timeout']).until(EC.title_contains('Por favor, insira seus dados de login'))

    # find the element that's username 
    path = "//div[3]/div/input"
    WebDriverWait(driver, mainCfg['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
    inputUsername = driver.find_element_by_xpath(path)
    inputUsername.send_keys(mainCfg['username'])
    
    # find the element that's password
    path = "//div[4]/div/input"
    WebDriverWait(driver, mainCfg['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
    inputUserpasswd = driver.find_element_by_xpath(path)
    inputUserpasswd.send_keys(mainCfg['passwd'])
    
    # find the element that's login button
    path = "//button"
    WebDriverWait(driver, mainCfg['timeout']).until(EC.visibility_of_element_located((By.XPATH,path)))
    inputLoginbutton = driver.find_element_by_xpath(path)
    inputLoginbutton.click()

    if mainCfg['lastName'] is not None:
        # we have to wait for the page to refresh, the last thing that seems to be updated is the user's lastName
        path = "//td[2]/table/tbody/tr/td[2]/em/button"
        WebDriverWait(driver, mainCfg['timeout']).until(EC.text_to_be_present_in_element((By.XPATH,path),mainCfg['lastName']))
    else:
        # check for error in login
        path = '//div[2]/span'
        WebDriverWait(driver, mainCfg['timeout']).until(EC.text_to_be_present_in_element((By.XPATH,path),u'Usuário e/ou senha incorretos!'))

#############################################################
# creates web driver for given browser
def createWebDriver(mainCfg):
    if mainCfg['webdriver'] == u'Firefox':

        # Create a new instance of the Firefox profile
        profile = selenium.webdriver.firefox.firefox_profile.FirefoxProfile();
        profile.native_events_enabled = True

        # adding firebug
        try :
            profile.add_extension(mainCfg['firebug'])
            profile.set_preference("extensions.firebug.currentVersion", "1.9.2") #Avoid startup screen

        except KeyError as err:
            pass

        # adding firexpath
        try:
            profile.add_extension(mainCfg['firexpath'])

        except KeyError as err:
            pass

        try:
            # checking if remote selenium server
            return RemoteWebDriver(mainCfg['seleniumServer'],DesiredCapabilities.FIREFOX)

        except KeyError as err:
            # returning local driver
            return webdriver.Firefox(profile)

    else:
        raise Exception("webdriver not found: "+mainCfg['webdriver'])

#######################################################################################
# function that provide access to a Module of ExpressoV3 given its identification text
def accessModule(mainCfg,driver,moduleIDText):
    # Wait for span (with the access to the modules of ExpressoV3) to be clickable
    modulesOptionPath = 'html/body/div[1]/div[3]/div/div/div/div[3]/div/div/div/div[1]/div[1]/ul/li[1]/a[2]/em/span'
    WebDriverWait(driver, mainCfg['timeout']).until(EC.element_to_be_clickable((By.XPATH,modulesOptionPath)))
    driver.find_element_by_xpath(modulesOptionPath).click()

    # Find the menu with the options
#    modulesMenuPath = '//html/body/div[27]/ul/div/div[1]'
    modulesMenuPath = '//ul/div/div/ul'
    WebDriverWait(driver, mainCfg['timeout']).until(EC.visibility_of_element_located((By.XPATH,modulesMenuPath)))
    modulesMenu = driver.find_element_by_xpath(modulesMenuPath)

    # Click in the option of the informed module
    modulesMenu.find_element_by_xpath("//span[contains(@class,'x-menu-item-text') and contains(text(),'" + moduleIDText + "')]").click()

    # wait for the window of the informed module
    modulekWindowPath = "//span[contains(@class,'x-tab-strip-text') and contains(text(),'" + moduleIDText + "')]"
    WebDriverWait(driver, mainCfg['timeout']).until(EC.presence_of_element_located((By.XPATH,modulekWindowPath)))

    # Verify if all the 3 sections are visible
    # west panel
    sectionPath = 'html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[3]/div'
    WebDriverWait(driver,mainCfg['timeout']).until(EC.presence_of_element_located((By.XPATH,sectionPath)))

    # center panel - top
    sectionPath = 'html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[2]/div/div/div[2]/div/div/div[1]'
    WebDriverWait(driver,mainCfg['timeout']).until(EC.presence_of_element_located((By.XPATH,sectionPath)))

    # center panel - bottom
    sectionPath = ' html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[2]/div/div/div[2]/div/div/div[2]'
    WebDriverWait(driver,mainCfg['timeout']).until(EC.presence_of_element_located((By.XPATH,sectionPath)))


