#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

import aux
import report

import N1_Autenticacao

def main():

    logger = report.Logger()

    N1_Autenticacao.CTV3_1(logger)
    N1_Autenticacao.CTV3_41(logger)
    N1_Autenticacao.CTV3_43(logger)
    N1_Autenticacao.CTV3_44(logger)
    N1_Autenticacao.CTV3_45(logger)
    N1_Autenticacao.CTV3_46(logger)
    N1_Autenticacao.CTV3_47(logger)
    N1_Autenticacao.CTV3_48(logger)

    logger.close()

# executs the main script
if __name__ == "__main__":
    main()

