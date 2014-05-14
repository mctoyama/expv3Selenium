#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

# auxiliary functions for calendarModule

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import selenium.common.exceptions

import cfgDB

import datetime
import time

#############################################################
# clicks Add Event in toolbar button

def clickAddEvent(mainCfg,driver):

    # selecting add event
    addEventPath = '//div[2]/table/tbody/tr/td/table/tbody/tr/td/div/div[2]/div/div/div/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, mainCfg['timeout']).until(EC.element_to_be_clickable((By.XPATH,addEventPath)))
    driver.find_element_by_xpath(addEventPath).click()

    # wait for add event window
    WebDriverWait(driver, mainCfg['timeout']).until( lambda driver: len(driver.window_handles) == 2 )

    windowCompose = driver.window_handles[-1]

    driver.switch_to_window(windowCompose)
    WebDriverWait(driver, mainCfg['timeout']).until(EC.title_contains('Adicionar Evento'))
    
    return windowCompose

#############################################################
# It fills the new event summary

def fillSummary(mainCfg,driver,text):

    inputPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/div[1]/div/div/div/input'
    WebDriverWait(driver, mainCfg['timeout']).until(EC.visibility_of_element_located((By.XPATH,inputPath)))
    inputSummary = driver.find_element_by_xpath(inputPath)
    inputSummary.send_keys(text)
    inputSummary.send_keys(Keys.ENTER)

#############################################################
# it checks the new event private checkbox

def checkPrivate(mainCfg,driver,state):
    
    checkPath  = '//html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div/fieldset[2]/div/div/div[4]/div[1]/div/input'
    WebDriverWait(driver, mainCfg['timeout']).until(EC.visibility_of_element_located((By.XPATH,checkPath)))
    checkInput = driver.find_element_by_xpath(checkPath)

    if state:
        if not checkInput.is_selected():
            checkInput.click()
    else:
        if checkInput.is_selected():
            checkInput.click()

#############################################################
# it clicks on save and close button - inside new event window

def clickSaveAndClose(mainCfg,driver,windowCompose):
    
    saveClass = 'action_saveAndClose'
    WebDriverWait(driver, mainCfg['timeout']).until(EC.element_to_be_clickable((By.CLASS_NAME,saveClass)))
    driver.find_element_by_class_name(saveClass).click()

    # waiting for closing compose window
    # selecting main window
    WebDriverWait(driver, mainCfg['timeout']).until( lambda driver: windowCompose not in driver.window_handles)
    driver.switch_to_window(driver.window_handles[0])

#############################################################
# it lists all events on the current calendar page

def listEvents(mainCfg,driver):

    ret = []
    
    try:
        eventClass = 'cal-daysviewpanel-event-body'
        WebDriverWait(driver, mainCfg['timeout']).until(EC.presence_of_all_elements_located((By.CLASS_NAME,eventClass)))

        for el in driver.find_elements_by_class_name(eventClass):
            ret.append( el.text )

    except selenium.common.exceptions.TimeoutException as err:
        pass

    return ret

#############################################################
# it selects and retuns an event, given subject

def selectEvent(mainCfg,driver,subject):

    ret = None
    
    try:
        eventClass = 'cal-daysviewpanel-event-body'
        WebDriverWait(driver, mainCfg['timeout']).until(EC.presence_of_all_elements_located((By.CLASS_NAME,eventClass)))

        for el in driver.find_elements_by_class_name(eventClass):
            if el.text == subject:
                el.click()
                ret = el
                break

    except selenium.common.exceptions.TimeoutException as err:
        pass

    return ret

#############################################################
# it clicks on delete button on toolbar

def clickDelete(mainCfg,driver,summary):
    
    # before delete summary list
    summaryList = listEvents(mainCfg,driver)

    # delete button
    deletePath = '//div[2]/table/tbody/tr/td/table/tbody/tr/td/div/div[2]/div/div/div/div/table/tbody/tr/td[3]/table/tbody/tr[2]/td[2]/em/button'

    WebDriverWait(driver, mainCfg['timeout']).until(EC.element_to_be_clickable((By.XPATH,deletePath)))
    driver.find_element_by_xpath(deletePath).click()

    # must confirme delete
    try:
 	confirmPath = '//div[2]/span'
        WebDriverWait(driver, mainCfg['timeout']).until(EC.visibility_of_element_located((By.XPATH,confirmPath)))

 	yesPath = '//div[2]/div/div/div/div/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button'
        WebDriverWait(driver, mainCfg['timeout']).until(EC.element_to_be_clickable((By.XPATH,yesPath)))
        yesEl = driver.find_element_by_xpath(yesPath)
        yesEl.click()

    except selenium.common.exceptions.TimeoutException as err:
        pass

    # wait for delete to complete    
    if summary is not None:
        return summary not in listEvents(mainCfg,driver)
    else:
        return set(summaryList) != set(listEvents(mainCfg,driver))
    

#############################################################
#############################################################
#############################################################
