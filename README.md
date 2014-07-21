expv3Selenium
=============

Selenium tests for Expresso V3

Autor 
# Marcelo Costa Toyama - marcelo.toyama@serpro.gov.br
# Juliana Hernandez - juliana.hernandez@serpro.gov.br

=============
Tools used for selenium

* http://docs.seleniumhq.org/

=============

Demo for ExpressoV3
https://comunidadeexpresso.serpro.gov.br/expressov3

Tests case for ExpressoV3
https://comunidadeexpresso.serpro.gov.br/mediawiki/index.php/Arquivo:CTV3_test_spec-2014-02-17.pdf

=============

How to use

edit files in ./cfg/ dir for testes parameters.
Example is in file ./sampleCfg/

Do this for all files in ./cfg/ dir

RUN
python allTests.py

=============
Added performance tests for ExpressoV3

REQUISITS
sudo apt-get install python-pexpect

running:
python performanceTests.py -h <expressov3 host> -u <root user> -p <root passwd> --sshport <ssh port> -m <module>

Parameters:
<expressov3 host> - host machine that us running the expressov3
<root user> - root user on the host above
<root passwd> - root's password on host above
<ssh port> - port for ssh on host above (default is 22)

Example
python performanceTests.py -h 192.168.25.29 -u root -p mypassword --sshport 22 -m expressoMail

The report will be written on 

./Count-LDAP-IMAP-PSQL/resultPSQL-YYYY-MM-DD.txt

YYYY = Year
MM = month
DD = day

=============

