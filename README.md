expv3Selenium
=============

Selenium tests for Expresso V3

Autor 
# Marcelo Costa Toyama - mctoyama@gmail.com 2014
# Rafael Raymundo da Silva

=============
Tools used for selenium

* http://docs.seleniumhq.org/

* http://couchdb.apache.org/

=============
Load do couchdb

couchdb-load http://127.0.0.1:5984/test < couchdb.dump

=============
Dump do couchdb

couchdb-dump http://127.0.0.1:5984/test > couchdb.dump

=============

- fazer um parser para massa de emails enviados

- configurar couchdb database in file

- adicionar o tipo da execção ao log junto com o str(err)
- diversas exceções não possuem mensagem de erro