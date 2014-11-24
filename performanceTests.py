#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: Marcelo Costa Toyama -mctoyama@gmail.com 2014

import optparse
import pxssh
import datetime
from subprocess import call
import re

import cfgDB
import aux

def send_command(s,cmd):
    s.sendline(cmd)
    s.prompt()
    ret = s.before
    return ret

def connect(host,user,password,myport):
    try:
        s = pxssh.pxssh()
        s.login(host,user,password,port=myport)
        return s
    except Exception as err:
        print '[-] Error connecting - ' + str(err)
        exit(0)

def main():

    # getting option parser
    parser = optparse.OptionParser("usage python performanceTests.py -h <hostname> -u <username> -p <password> --sshport <ssh port - default 22> -m <target module: (expressoMail,addressBook, calendar,...)>",add_help_option=False)

    parser.add_option("-h", dest='tgHostname', type="string", help="specify the hostname for the SSH client")    
    parser.add_option("-u", dest='tgUsername', type="string", help="specify the username for the SSH client")    
    parser.add_option("-p", dest='tgPassword', type="string", help="specify the password for the SSH client")    
    parser.add_option("--sshport", dest='tgPort', type="int", help="specify the port for the SSH client")    
    parser.add_option("-m", dest='tgModule', type="string", help="specify the Module to be realized a perfomance test")

    (options,args) = parser.parse_args()

    if options.tgHostname == None or options.tgUsername == None or options.tgPassword == None or options.tgModule == None:
        print parser.usage
        return

    if options.tgPort == None:
        options.tgPort = 22

    print("Initializend performance test...")

    # connecting to server
    s = connect(options.tgHostname,options.tgUsername,options.tgPassword,options.tgPort)
    print("Connecting ssh to server - OK")

    # It check's if configuration files are ok.
    print("checking configuration files on the server")
    
    # imapd.conf
    # debug_command: /usr/bin/strace -tt -o /tmp/strace.cyrus.%s.log -p %2$d <&- 2>&1 &

    ret = send_command(s, "cat /etc/imapd.conf")

    if not re.search("^(debug_command: /usr/bin/strace -tt -o /tmp/strace.cyrus.%s.log -p %2\$d \<&- 2\>&1 &)(\s*)$", ret, re.MULTILINE):
        print("/etc/imapd.conf missing line: debug_command: /usr/bin/strace -tt -o /tmp/strace.cyrus.%s.log -p %2$d <&- 2>&1 &")
        return 1

    print("/etc/imapd.conf - OK")
    
    # postgresql.conf
    # log_directory = '/data'
    # log_filename = 'postgresql-%Y-%m-%d.log'
    # debug_pretty_print = on
    # log_duration = on
    # log_line_prefix = '%t [%p]: [%l-1] user=postgres,db=%d '
    # log_statement = 'all'

    ret = send_command(s, "cat /etc/postgresql/9.4/main/postgresql.conf")

    if not re.search("^(log_directory = '/data/')(\s*#.*\s*)$", ret, re.MULTILINE):
        print("/etc/postgresql/9.4/main/postgresql.conf missing line: log_directory = '/data'")
        return 1

    if not re.search("^(log_filename = 'postgresql-%Y-%m-%d.log')(\s*#.*\s*)$", ret, re.MULTILINE):
        print("/etc/postgresql/9.4/main/postgresql.conf missing line: log_filename = 'postgresql-%Y-%m-%d.log'")
        return 1

    if not re.search("^(debug_pretty_print = on)(\s*#.*\s*)$", ret, re.MULTILINE):
        print("/etc/postgresql/9.4/main/postgresql.conf missing line: debug_pretty_print = on")
        return 1

    if not re.search("^(log_duration = on)(\s*#.*\s*)$", ret, re.MULTILINE):
        print("/etc/postgresql/9.4/main/postgresql.conf missing line: log_duration = on")
        return 1

    if not re.search("^(log_line_prefix = '%t \[%p\]: \[%l-1\] user=postgres,db=%d ')(\s*#.*\s*)$", ret, re.MULTILINE):
        print("/etc/postgresql/9.4/main/postgresql.conf missing line: log_line_prefix = '%t [%p]: [%l-1] user=postgres,db=%d '")
        return 1

    if not re.search("^(log_statement = 'all')(\s*#.*\s*)$", ret, re.MULTILINE):
        print("/etc/postgresql/9.4/main/postgresql.conf missing line: log_statement = 'all'")
        return 1

    print("/etc/postgresql/9.4/main/postgresql.conf - OK")

    # slapd.conf
    # loglevel 256

    ret = send_command(s, "cat /etc/ldap/slapd.conf")

    if not re.search("^(loglevel 256)(\s*)$", ret, re.MULTILINE):
        print("/etc/ldap/slapd.conf missing line: loglevel 256")
        return 1

    print("/etc/ldap/slapd.conf - OK")

    # getting date
    now = datetime.datetime.now()
    current = "%04d-%02d-%02d" % (now.year,now.month,now.day)

    # Limpar logs

    print("Cleaning server logs...")

    send_command(s, ">/data/postgresql-"+current+".log")
    send_command(s, ">/var/log/syslog")
    send_command(s, ">/tmp/strace.cyrus.imapd.log")
    send_command(s, "chown cyrus.mail /tmp/strace.cyrus.imapd.log")

    # setting up selenium

    print("Running selenium...")

    mainCfg = cfgDB.getDict('main.xml')

    if options.tgModule == 'expressoMail':

        print("Running expressoMail")

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        selectedModuleText = 'Email'

        aux.accessModule(mainCfg,driver,selectedModuleText)

        driver.quit()

    elif options.tgModule == "addressBook":

        print("Running adressBook")
        
        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        selectedModuleText = 'Catálogos de Endereços'

        aux.accessModule(mainCfg,driver,selectedModuleText)

        driver.quit()

    elif options.tgModule == "calendar" :

        print("Running calendar")

        # Create a new instance of the webdriver        
        driver = aux.createWebDriver(mainCfg)

        aux.login(mainCfg,driver)

        selectedModuleText = 'Calendário'

        aux.accessModule(mainCfg,driver,selectedModuleText)

        driver.quit()

    else:
        print parser.usage

    # It gets the results from log files

    print("Generating report from logs...")

    send_command(s, ">/data/resultPSQL-"+current+".txt")
    send_command(s, "echo '***************************************************' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo '"+options.tgModule+"' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo '***************************************************' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'P O S G R E S Q L' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'INSERT: ' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "cat /data/postgresql-"+current+".log | grep 'INSERT'|wc -l >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'UPDATE: ' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "cat /data/postgresql-"+current+".log | grep 'UPDATE'|wc -l >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'SELECT: ' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "cat /data/postgresql-"+current+".log | grep 'SELECT'|wc -l >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo '***************************************************' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'L D A P' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'BIND: ' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "for i in $(cat /var/log/syslog | grep 127.0.0.1 | awk '{print $3}'); do cat /var/log/syslog | grep $i; done | grep 'BIND' | awk '{print $8}'|wc -l >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'SRCH: ' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "for i in $(cat /var/log/syslog | grep 127.0.0.1 | awk '{print $3}'); do cat /var/log/syslog | grep $i; done | grep 'SRCH' | awk '{print $8}'|wc -l >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'MOD: '>>/data/resultPSQL-"+current+".txt")
    send_command(s, "for i in $(cat /var/log/syslog | grep 127.0.0.1 | awk '{print $3}'); do cat /var/log/syslog | grep $i; done | grep 'MOD' | awk '{print $8}'|wc -l >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo '***************************************************' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "echo 'IMAPD' >>/data/resultPSQL-"+current+".txt")
    send_command(s, "cat /tmp/strace.cyrus.imapd.log | grep -a --text 'TAG' | awk '{print $4}' | sort | uniq -c | sort -k 1 -n >>/data/resultPSQL-"+current+".txt")

    # cleaning
    s.logout()

    # It gets report from server
    call('sshpass -p "'+options.tgPassword+'" scp -P '+str(options.tgPort)+' '+options.tgUsername+'@'+options.tgHostname+':/data/resultPSQL-'+current+'.txt ./Count-LDAP-IMAP-PSQL',shell=True)

    print("Copying report to ./Count-LDAP-IMAP-PSQL/resultPSQL-"+current+".txt - OK")

    print("Goodbye!")

# executs the main script
if __name__ == "__main__":
    main()

