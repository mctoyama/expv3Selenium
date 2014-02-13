#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

import aux
import report

import N1_Autenticacao
import N4_Mensagens_de_email

def main():

    logger = report.Logger()

    N1_Autenticacao.allTests(logger)
    N4_Mensagens_de_email.allTests(logger)

    logger.close()

# executs the main script
if __name__ == "__main__":
    main()

