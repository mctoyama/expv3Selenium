#!/bin/bash

#
# Shell desenvolvido com o objetivo de limpar logs de um servidor 
# virtualizado e realizar a contagem de acessos aos servicos: LDAP, PSQL 
# e IMAP.
#
#						rafael.silva@serpro.gov.br

# checking module list

md="";

if [[ -z "$1" ]]; then
    echo "You must specify a module: expressoMail, ..."
    exit
elif [ "$1" = "expressoMail" ]; then
    md=$1;
else
    echo "There is no module "$1;
    exit
fi

## Limpar logs
# CURRENT = $(date +%F)
ssh root@127.0.0.1 -p 2222 ">/data/postgresql-'$(date +%F)'.log
>/var/log/syslog
>/tmp/strace.cyrus.imapd.log
chown cyrus.mail /tmp/strace.cyrus.imapd.log
exit"
clear

# Executa o teste automatizado 
/usr/bin/python ./performanceTests.py "-M" $md

# Retorna ao Servidor para contar dos dados desse teste
ssh root@127.0.0.1 -p 2222 ">/data/resultPSQL-'$(date +%F)'.txt
echo 'P O S G R E S Q L' >>/data/resultPSQL-'$(date +%F)'.txt
echo 'INSERT: ' >>/data/resultPSQL-'$(date +%F)'.txt
cat /data/postgresql-'$(date +%F)'.log | grep 'INSERT'|wc -l >>/data/resultPSQL-'$(date +%F)'.txt
echo 'UPDATE: ' >>/data/resultPSQL-'$(date +%F)'.txt
cat /data/postgresql-'$(date +%F)'.log | grep 'UPDATE'|wc -l >>/data/resultPSQL-'$(date +%F)'.txt
echo 'SELECT: ' >>/data/resultPSQL-'$(date +%F)'.txt
cat /data/postgresql-'$(date +%F)'.log | grep 'SELECT'|wc -l >>/data/resultPSQL-'$(date +%F)'.txt
echo '***************************************************' >>/data/resultPSQL-'$(date +%F)'.txt
echo 'L D A P' >>/data/resultPSQL-'$(date +%F)'.txt
echo 'BIND: ' >>/data/resultPSQL-'$(date +%F)'.txt
for i in \$(cat /var/log/syslog | grep 127.0.0.1 | awk '{print \$3}'); do cat /var/log/syslog | grep \$i; done | grep 'BIND' | awk '{print \$8}'|wc -l >>/data/resultPSQL-'$(date +%F)'.txt
echo 'SRCH: ' >>/data/resultPSQL-'$(date +%F)'.txt
for i in \$(cat /var/log/syslog | grep 127.0.0.1 | awk '{print \$3}'); do cat /var/log/syslog | grep \$i; done | grep 'SRCH' | awk '{print \$8}'|wc -l >>/data/resultPSQL-'$(date +%F)'.txt
echo 'MOD: '>>/data/resultPSQL-'$(date +%F)'.txt
for i in \$(cat /var/log/syslog | grep 127.0.0.1 | awk '{print \$3}'); do cat /var/log/syslog | grep \$i; done | grep 'MOD' | awk '{print \$8}'|wc -l >>/data/resultPSQL-'$(date +%F)'.txt
echo '***************************************************' >>/data/resultPSQL-'$(date +%F)'.txt
echo 'IMAPD' >>/data/resultPSQL-'$(date +%F)'.txt
cat /tmp/strace.cyrus.imapd.log | grep 'TAG' | awk '{print \$4}' | sort | uniq -c | sort -k 1 -n >>/data/resultPSQL-'$(date +%F)'.txt"

scp -P 2222 root@127.0.0.1:/data/resultPSQL-'$(date +%F)'.txt ./Count-LDAP-IMAP-PSQL
