#!/usr/bin/env python
# -*- coding: utf-8 -*-

# auxiliary functions for addressbookModule

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import selenium.common.exceptions

#############################################################
# Clica no botão "Adicionar Contato" e espera a janela abrir
# Retorna o window id para a nova janela
def clickAddContact(driver,timeout):

    # selecting "Adicionar Contato"
    addContactButtonPath = 'html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[1]/div/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH,addContactButtonPath)))
    driver.find_element_by_xpath(addContactButtonPath).click()

    # wait for compor email window
    WebDriverWait(driver,timeout).until( lambda driver: len(driver.window_handles) == 2 )

    addContactWindow = driver.window_handles[-1]

    driver.switch_to_window(addContactWindow)
    WebDriverWait(driver,timeout).until(EC.title_contains('Adicionar Contato'))
    
    return addContactWindow


######################################
# Preenche o Sobrenome
def fillLastName(driver,timeout,lastNameText):
    # filling last name field
    lastNamePath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,lastNamePath)))
    lastNameElement = driver.find_element_by_xpath(lastNamePath)
    lastNameElement.send_keys(lastNameText)
    lastNameElement.send_keys(Keys.ENTER)


######################################
# Preenche a Empresa
def fillCompany(driver,timeout,companyText):
    # filling company field
    companyPath = '//html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,companyPath)))
    companyElement = driver.find_element_by_xpath(companyPath)
    companyElement.send_keys(companyText)
    companyElement.send_keys(Keys.ENTER)

######################################
# Preenche o Título
def fillTitle (driver,timeout,titleText):
    # filling title field
    titlePath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,titlePath)))
    titleElement = driver.find_element_by_xpath(titlePath)
    titleElement.send_keys(titleText)
    titleElement.send_keys(Keys.ENTER)


######################################
# Preenche o Nome
def fillName (driver,timeout,nameText):
    # filling name field
    namePath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,namePath)))
    nameElement = driver.find_element_by_xpath(namePath)
    nameElement.send_keys(nameText)
    nameElement.send_keys(Keys.ENTER)


######################################
# Preenche o Nome do Meio
def fillMiddleName (driver,timeout,middleNameText):
    # filling middle name field
    middleNamePath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,middleNamePath)))
    middleNameElement = driver.find_element_by_xpath(middleNamePath)
    middleNameElement.send_keys(middleNameText)
    middleNameElement.send_keys(Keys.ENTER)


######################################
# Preenche a Unidade da Empresa
def fillCompanyUnit (driver,timeout, companyUnitText):
    # filling company unit field
    companyUnitPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,companyUnitPath)))
    companyUnitElement = driver.find_element_by_xpath(companyUnitPath)
    companyUnitElement.send_keys(companyUnitText)
    companyUnitElement.send_keys(Keys.ENTER)


######################################
# Preenche o Título do Trabalho
def fillWorkTitle (driver,timeout,workTitleText):
    # filling work title field
    workTitlePath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,workTitlePath)))
    workTitleElement = driver.find_element_by_xpath(workTitlePath)
    workTitleElement.send_keys(workTitleText)
    workTitleElement.send_keys(Keys.ENTER)


######################################
# Preenche o Dia do Aniversário
def fillBirthday (driver,timeout,birthdayText):
    # filling birthday field
    birthdayPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[1]/div/div/div[2]/div/div/div/div/div/div/div[3]/div/div/div/div[1]/div/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,birthdayPath)))
    birthdayElement = driver.find_element_by_xpath(birthdayPath)
    birthdayElement.send_keys(birthdayText)
    birthdayElement.send_keys(Keys.ENTER)


######################################
# Preenche o Telefone (Empresa)
def fillPhoneNumber (driver,timeout,phoneNumberText):
    # filling phone number field
    phoneNumberPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,phoneNumberPath)))
    phoneNumberElement = driver.find_element_by_xpath(phoneNumberPath)
    phoneNumberElement.send_keys(phoneNumberText)
    phoneNumberElement.send_keys(Keys.ENTER)


######################################
# Preenche o Celular (Empresa)
def fillCellPhoneNumber (driver,timeout,cellPhoneNumberText):
    # filling cell phone number field
    cellPhoneNumberPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,cellPhoneNumberPath)))
    cellPhoneNumberElement = driver.find_element_by_xpath(cellPhoneNumberPath)
    cellPhoneNumberElement.send_keys(cellPhoneNumberText)
    cellPhoneNumberElement.send_keys(Keys.ENTER)


######################################
# Preenche o Fax (Empresa)
def fillFax (driver,timeout,faxText):
    # filling fax field
    faxPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,faxPath)))
    faxElement = driver.find_element_by_xpath(faxPath)
    faxElement.send_keys(faxText)
    faxElement.send_keys(Keys.ENTER)


######################################
# Preenche o Telefone (Particular)
def fillPrivatePhoneNumber (driver,timeout,privatePhoneNumberText):
    # filling private phone number field
    privatePhoneNumberPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,privatePhoneNumberPath)))
    privatePhoneNumberElement = driver.find_element_by_xpath(privatePhoneNumberPath)
    privatePhoneNumberElement.send_keys(privatePhoneNumberText)
    privatePhoneNumberElement.send_keys(Keys.ENTER)


######################################
# Preenche o Celular (Particular)
def fillPrivCellPhoneNumber (driver,timeout,PrivCellPhoneNumberText):
    # filling private cell phone number field
    PrivCellPhoneNumberPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,PrivCellPhoneNumberPath)))
    PrivCellPhoneNumberElement = driver.find_element_by_xpath(PrivCellPhoneNumberPath)
    PrivCellPhoneNumberElement.send_keys(PrivCellPhoneNumberText)
    PrivCellPhoneNumberElement.send_keys(Keys.ENTER)


######################################
# Preenche o Fax (Particular)
def fillprivateFax (driver,timeout,privateFaxText):
    # filling private fax field
    privateFaxPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,privateFaxPath)))
    privateFaxElement = driver.find_element_by_xpath(privateFaxPath)
    privateFaxElement.send_keys(privateFaxText)
    privateFaxElement.send_keys(Keys.ENTER)


######################################
# Preenche o E-mail
def fillEmail (driver,timeout,emailText):
    # filling email field
    emailPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,emailPath)))
    emailElement = driver.find_element_by_xpath(emailPath)
    emailElement.send_keys(emailText)
    emailElement.send_keys(Keys.ENTER)


######################################
# Preenche o E-mail (Particular)
def fillprivateEmail (driver,timeout,privateEmailText):
    # filling privateEmail field
    privateEmailPath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,privateEmailPath)))
    privateEmailElement = driver.find_element_by_xpath(privateEmailPath)
    privateEmailElement.send_keys(privateEmailText)
    privateEmailElement.send_keys(Keys.ENTER)


######################################
# Preenche o Website
def fillWebsite (driver,timeout,websiteText):
    # filling website field
    websitePath = 'html/body/div[1]/div[2]/div/form/div/div[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/div/fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[3]/div/div/div/div[1]/input'
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,websitePath)))
    websiteElement = driver.find_element_by_xpath(websitePath)
    websiteElement.send_keys(websiteText)
    websiteElement.send_keys(Keys.ENTER)


######################################
# Preenche a Empresa
def clickOk(driver,addContactWindow,timeout):

    # clicking ok to add the contact
    okButtonPath = 'html/body/div[1]/div[2]/div/div[2]/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH,okButtonPath)))
    driver.find_element_by_xpath(okButtonPath).click()


