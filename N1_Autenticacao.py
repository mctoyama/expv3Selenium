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

#
# N1 - Autenticação
# 

import aux

# all testes for autenticacao module
def allTests(mainCfg,logger):
    CTV3_1(mainCfg,logger)
    CTV3_41(mainCfg,logger)
    CTV3_43(mainCfg,logger)
    CTV3_44(mainCfg,logger)
    CTV3_45(mainCfg,logger)
    CTV3_46(mainCfg,logger)
    CTV3_47(mainCfg,logger)
    CTV3_48(mainCfg,logger)

# CTV3-1:Logar no sistema com sucesso
def CTV3_1(mainCfg,logger):

    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        logger.save('CTV3_1','Logar no sistema com sucesso',"True")

    except Exception as err:
        logger.save('CTV3_1','Logar no sistema com sucesso',unicode(type(err))+unicode(err))        

    finally:
        driver.quit()


# CTV3-41:Logar no sistema com login incorreto
def CTV3_41(mainCfg,logger):

    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        tmpCfg = mainCfg.copy()
        tmpCfg['username'] = tmpCfg['username']+'invalid'
        tmpCfg['lastName'] = None

        aux.login(tmpCfg,driver)

        logger.save('CTV3_41','Logar no sistema com login incorreto',"True")
        
    except Exception as err:
        logger.save('CTV3_41','Logar no sistema com login incorreto',unicode(type(err))+unicode(err))        
    finally:
        driver.quit()

# CTV3-43:Logar no sistema com senha incorreta
def CTV3_43(mainCfg,logger):
    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        tmpCfg = mainCfg.copy()
        tmpCfg['passwd'] = tmpCfg['passwd']+'invalid'
        tmpCfg['lastName'] = None

        aux.login(tmpCfg,driver)

        logger.save('CTV3_43','Logar no sistema com senha incorreta',"True")
        
    except Exception as err:
        logger.save('CTV3_43','Logar no sistema com senha incorreta',unicode(type(err))+unicode(err))

    finally:
        driver.quit()

# CTV3-44:Logar no sistema com login vazio
def CTV3_44(mainCfg,logger):
    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)
        
        tmpCfg = mainCfg.copy()
        tmpCfg['username'] = ''
        tmpCfg['lastName'] = None

        aux.login(tmpCfg,driver)

        logger.save('CTV3_44','Logar no sistema com login vazio',"True")
        
    except Exception as err:
        logger.save('CTV3_44','Logar no sistema com login vazio',unicode(type(err))+unicode(err))

    finally:
        driver.quit()
    

# CTV3-45:Logar no sistema com senha vazia
def CTV3_45(mainCfg,logger):
    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        tmpCfg = mainCfg.copy()
        tmpCfg['passwd'] = ''
        tmpCfg['lastName'] = None
               
        aux.login(tmpCfg,driver)

        logger.save('CTV3_45','Logar no sistema com senha vazia',"True")
        
    except Exception as err:
        logger.save('CTV3_45','Logar no sistema com senha vazia',unicode(type(err))+unicode(err))

    finally:
        driver.quit()
    
# CTV3-46:Logar no sistema com login usando caracteres em branco
def CTV3_46(mainCfg,logger):
    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        tmpCfg = mainCfg.copy()
        tmpCfg['username'] = u'         '
        tmpCfg['lastName'] = None

        aux.login(tmpCfg,driver)

        logger.save('CTV3_46','Logar no sistema com login usando caracteres em branco',"True")
        
    except Exception as err:
        logger.save('CTV3_46','Logar no sistema com login usando caracteres em branco',unicode(type(err))+unicode(err))

    finally:
        driver.quit()
    

# CTV3-47:Logar no sistema com senha usando caracteres em branco
def CTV3_47(mainCfg,logger):
    try:

        # Create a new instance of the webdriver
        driver = aux.createWebDriver(mainCfg)

        tmpCfg = mainCfg.copy()
        tmpCfg['passwd'] = u'      '
        tmpCfg['lastName'] = None

        aux.login(tmpCfg,driver)

        logger.save('CTV3_47','Logar no sistema com senha usando caracteres em branco',"True")
        
    except Exception as err:
        logger.save('CTV3_47','Logar no sistema com senha usando caracteres em branco',unicode(type(err))+unicode(err))

    finally:
        driver.quit()

# CTV3-48:Logar no sistema com login usando caracteres especiais
def CTV3_48(mainCfg,logger):
    try:

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        tmpCfg = mainCfg.copy()
        tmpCfg['username'] = u'açúcar%$*232'
        tmpCfg['lastName'] = None

        aux.login(tmpCfg,driver)

        logger.save('CTV3_48','Logar no sistema com login usando caracteres especiais',"True")
        
    except Exception as err:
        logger.save('CTV3_48','Logar no sistema com login usando caracteres especiais',unicode(type(err))+unicode(err))

    finally:
        driver.quit()
