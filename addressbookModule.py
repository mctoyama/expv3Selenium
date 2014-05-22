#!/usr/bin/env python
# -*- coding: utf-8 -*-

# auxiliary functions for addressbookModule

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import selenium.common.exceptions

import collections

#############################################################
# Clica no botão "Adicionar Contato" e espera a janela abrir
# Retorna o window id para a nova janela
def clickAddContact(driver,timeout):

    # selecting "Adicionar Contato"
    addContactButtonPath = 'html/body/div[1]/div[3]/div/div/div/div[4]/div/div/div[1]/div/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH,addContactButtonPath)))
    driver.find_element_by_xpath(addContactButtonPath).click()

    # wait for "Adicionar Contato" window
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
# Clica no botão Ok para enviar os dados do contato
def clickOk(driver,addContactWindow,timeout):

    # clicking ok to add the contact
    okButtonPath = 'html/body/div[1]/div[2]/div/div[2]/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button'
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH,okButtonPath)))
    driver.find_element_by_xpath(okButtonPath).click()


######################################
# Seleciona o 1o. contato entre os contatos do Catálogo de Endereços Pessoais
def selectContact(driver,timeout):

    driver.find_element_by_xpath("//img[contains(@class,'x-tree-node-icon') and contains(@class,'AddressbookContact')]").click()

    # Click in the span for all addressbooks
    allAddressbooksTextSpan = driver.find_element_by_xpath("//span[contains(text(),'Todos(as) Catálogos')]")
    if not allAddressbooksTextSpan.is_displayed():
        allAddressbooksSpan = driver.find_element_by_xpath("//span[contains(@class,'ux-arrowcollapse-header-text') and contains(text(),'Catálogos')]")
        allAddressbooksSpan.click()

    # Click in all personal addressbooks span
    path = "//ul/li/ul/li/div/a/span"
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH,path)))
    allAdds = driver.find_elements_by_xpath(path)
    for i in allAdds:
        if i.text == u'Catálogos':
            i.click()
            break

    # Click in the personal addressbook span
    path = "//li/ul/li[1]/ul/li/div/a/span"
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH,path)))
    driver.find_element_by_xpath(path).click()

    path = "//div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div[1]"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,path)))

    path = "//div[2]/div/div/div/div/div/div/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td/div"
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,path)))
    divCountRegs = driver.find_element_by_xpath(path)
    if divCountRegs.text == u'Não há Contatos para mostrar':
        raise Exception("Não há Contatos para mostrar")
    else:

        path = "//div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div[1]/table/tbody/tr[1]/td[1]/div"
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,path)))
        driver.find_element_by_xpath(path).click()
        return "//div[2]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div[1]/table/tbody/tr[1]"

######################################
# Recupera os dados do contato representado na linha informada
def getContactInfo(driver,timeout,contactInfoRowPath):
    contactInfoRow = driver.find_element_by_xpath(contactInfoRowPath)

    dc = ActionChains(driver).double_click(contactInfoRow)
    dc.perform()

    # wait for "Editar Contato" window
    WebDriverWait(driver,timeout).until( lambda driver: len(driver.window_handles) == 2 )

    addContactWindow = driver.window_handles[-1]

    driver.switch_to_window(addContactWindow)
    WebDriverWait(driver,timeout).until(EC.title_contains('Editar Contato'))

    streetCompanyText = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value")
    regionCompanyText = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input").get_attribute("value")
    postalCodeCompanyText = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value")
    cityCompanyText = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input").get_attribute("value")
    countryCompanyText = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/div/input").get_attribute("value")

    driver.find_element_by_xpath("//div/div[1]/div[1]/div[1]/ul/li[2]/a[2]/em/span/span").click()

    contactInfoReg = collections.namedtuple('contactInfoReg',['nameText','lastNameText','companyText','companyUnitText','phoneNumberText','cellPhoneNumberText','faxText','privatePhoneNumberText','privCellPhoneNumberText','privateFaxText','emailText','privateEmailText','websiteText','streetCompanyText','regionCompanyText','postalCodeCompanyText','cityCompanyText','countryCompanyText','streetPrivText','regionPrivText','postalCodePrivText','cityPrivText','countryPrivText'])

    reg = contactInfoReg(driver.find_element_by_xpath("//fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[3]/div/div/div/div[1]/input").get_attribute("value"), streetCompanyText, regionCompanyText, postalCodeCompanyText, cityCompanyText, countryCompanyText, driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input").get_attribute("value"),  driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input").get_attribute("value"), driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/div/input").get_attribute("value"))


    cancelBtnPath = "//td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/em/button"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH,cancelBtnPath)))
    driver.find_element_by_xpath(cancelBtnPath).click()

    WebDriverWait(driver, timeout).until( lambda driver: addContactWindow not in driver.window_handles)
    driver.switch_to_window(driver.window_handles[0])

    return reg

######################################
# Atualiza os dados do contato representado na linha informada a partir do registro informado
def setContactInfo(driver,timeout,contactInfoRowPath,contactInfoReg):

    contactInfoRow = driver.find_element_by_xpath(contactInfoRowPath)

    # click in the edit button
    driver.find_element_by_xpath("//div[2]/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[2]/div[1]/div/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button").click()

    # wait for "Editar Contato" window
    WebDriverWait(driver,timeout).until( lambda driver: len(driver.window_handles) == 2 )

    addContactWindow = driver.window_handles[-1]

    driver.switch_to_window(addContactWindow)
    WebDriverWait(driver,timeout).until(EC.title_contains('Editar Contato'))

    webEl = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.streetCompanyText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.regionCompanyText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.regionCompanyText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.cityCompanyText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/div/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.countryCompanyText)
    webEl.send_keys(Keys.ENTER)

    driver.find_element_by_xpath("//div/div[1]/div[1]/div[1]/ul/li[2]/a[2]/em/span/span").click()

    webEl = driver.find_element_by_xpath("//fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.nameText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.lastNameText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.companyText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[1]/div/div/div[1]/div/div/div/div[1]/div/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.companyUnitText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.phoneNumberText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.cellPhoneNumberText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.faxText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.privatePhoneNumberText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.privCellPhoneNumberText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.privateFaxText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.emailText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.privateEmailText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//fieldset[2]/div/div/div/div/div/div[3]/div/div/div/div[3]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.websiteText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.streetPrivText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.regionPrivText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.postalCodePrivText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.cityPrivText)
    webEl.send_keys(Keys.ENTER)

    webEl = driver.find_element_by_xpath("//div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[1]/div/input")
    webEl.clear()
    webEl.send_keys(contactInfoReg.countryPrivText)
    webEl.send_keys(Keys.ENTER)

    OkBtnPath = "//td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/em/button"
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH,OkBtnPath)))
    driver.find_element_by_xpath(OkBtnPath).click()

    WebDriverWait(driver, timeout).until( lambda driver: addContactWindow not in driver.window_handles)
    driver.switch_to_window(driver.window_handles[0])


######################################
# Compara os dados do contato com os dados que estão sendo visualizados na seção inferior
# Por default, somente os campos abaixo aparecem tanto na linha da seção superior quanto na seção de informações do contato (seção inferior)
# Nome, Empresa, Cidade, E-mail, Telefone e Celular
def compareContactInfoSections(driver,timeout,contactInfoRowPath):
    contactInfoReg = getContactInfo(driver,timeout,contactInfoRowPath)

    companyUnitText = contactInfoReg.companyText + ' / ' + contactInfoReg.companyUnitText
    companyAddressText = companyUnitText + "\n" + contactInfoReg.streetCompanyText + "\n" + contactInfoReg.postalCodeCompanyText + " " + contactInfoReg.cityCompanyText + "\n" + contactInfoReg.regionCompanyText + " / " + contactInfoReg.countryCompanyText
    if companyAddressText != driver.find_element_by_xpath("//div[2]/div/div/div/div[1]/div[2]/div[6]").text:
        raise Exception(u"Endereço da empresa exibido incorretamente")

    nameLastNameText = contactInfoReg.nameText + " " + contactInfoReg.lastNameText
    privAddressText = nameLastNameText + "\n" + contactInfoReg.streetPrivText  + "\n" + contactInfoReg.postalCodePrivText + " " + contactInfoReg.cityPrivText + "\n" + contactInfoReg.regionPrivText + " / " + contactInfoReg.countryPrivText
    if privAddressText != driver.find_element_by_xpath("//div[2]/div/div/div/div[2]/div[6]").text:
        raise Exception(u"Endereço pessoal exibido incorretamente")

    companyInfoText = 'Telefone\n' + contactInfoReg.phoneNumberText + '\nCelular\n' + contactInfoReg.cellPhoneNumberText + '\nFax\n' + contactInfoReg.faxText + '\nE-mail\n' + contactInfoReg.emailText[:15] + '...\nWeb\n' + contactInfoReg.websiteText[:15] + '...'

    if (companyInfoText != driver.find_element_by_xpath("//div[2]/div/div/div/div/div[2]/div[7]").text):
        raise Exception("Informações profissionais do contato exibidas incorretamente")

    privInfoText = 'Telefone\n' + contactInfoReg.privatePhoneNumberText + '\nCelular\n' + contactInfoReg.privCellPhoneNumberText + '\nFax\n' + contactInfoReg.privateFaxText + '\nE-mail\n' + contactInfoReg.privateEmailText[:15] + '...\nWeb'
    if (privInfoText != driver.find_element_by_xpath("//div[2]/div/div/div/div[2]/div[7]").text):
        raise Exception("Informações pessoais do contato exibidas incorretamente")

