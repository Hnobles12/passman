#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cryptography.fernet import Fernet
from tinydb import TinyDB, Query


def save_key(fname: str) -> None:
    key = Fernet.generate_key()
    with open(fname, 'wb') as f:
        f.write(key)
        f.close()


def get_key(fname: str):
    with open(fname, 'rb') as f:
        key = f.read()
        f.close()
    return key


#save_key('test.key')
key = get_key('test.key')

f = Fernet(key)
#passwd = f.encrypt('12345678910asdfga'.encode())

db = TinyDB('test.db')
with open('test.db', 'rb') as fl:
    encrypted = f.encrypt(fl.read())
    fl.close()

with open('test2.db', 'wb') as fl:
    fl.write(encrypted)
    fl.close()

#db.insert({'name': 'Rachel', 'age': 22, 'pass': passwd.decode()})

user = Query()

print(entry := db.search(user.name == 'Rachel'))
print(len(entry))
#print(f.decrypt(entry[0]['pass'].encode()))
