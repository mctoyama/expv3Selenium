#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

from selenium import webdriver

import aux

import N1_Autenticacao

def main():

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    try:
        N1_Autenticacao.CTV3_1(driver)

    except Exception as err:
        print str(err)

    driver.quit()

# executs the main script
if __name__ == "__main__":
    main()

