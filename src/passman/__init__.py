#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import secrets
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e
from getpass import getpass
from hashlib import sha256

import click
import toml
from colorama import Fore, Style
from cryptography.fernet import Fernet, InvalidToken
from tinydb import Query, TinyDB

from .lib import *


class Entry:
    def __init__(self,
                 name: str,
                 username: str = None,
                 url: str = None,
                 password: str = None):
        self.name = name
        self.username = username or ''
        self.url = url or ''
        self.password = password or self.generate_password()
    
    def encrypt_(self, crypt_worker):
        #self.name = crypt_worker.encrypt(self.name.encode()).decode()
        self.username = crypt_worker.encrypt(self.username.encode()).decode()
        self.url = crypt_worker.encrypt(self.url.encode()).decode()
        self.password = crypt_worker.encrypt(self.password.encode()).decode()

    def encrypt_to_dict(self, crypt_worker)->dict:
        self.encrypt_(crypt_worker)
        return self.__dict__
    
    def decrypt(self,crypt_worker:Fernet)->None:
        #self.name = crypt_worker.decrypt(self.name.encode()).decode()
        self.username = crypt_worker.decrypt(self.username.encode()).decode()
        self.url = crypt_worker.decrypt(self.url.encode()).decode()
        self.password = crypt_worker.decrypt(self.password.encode()).decode()

    @staticmethod
    def from_dict(dat: dict):
        ent = Entry(dat['name'], dat['username'], dat['url'], dat['password'])
        return ent

    @staticmethod
    def generate_password(length: int = 20):
        return secrets.token_urlsafe(length)

    def __str__(self):
        return f'{Style.DIM}Service:{Style.NORMAL} {self.name}\n{Style.DIM}Username:{Style.NORMAL} {self.username}\n{Style.DIM}URL:{Style.NORMAL} {self.url}\n{Style.DIM}Password:{Style.NORMAL} {Fore.RED}{self.password}{Style.RESET_ALL}'


@click.command()
@click.argument('name', default=None, required=False, help='Name of service')
@click.option('--config',
              '-c',
              default=os.path.expanduser('~/.config/passman.toml'),help="Path to a config file.")
@click.option('--new','-n', is_flag=True,help="Add a new service")
def app(name, config, new):
    #Read Config file
    settings = toml.load(config)

    #Authenticate User
    master_pass = getpass("Enter Master Password: ")
    hasher = sha256()
    hasher.update(master_pass.encode())
    master_pass_h = b64e(hasher.digest())
    crypt_worker = Fernet(master_pass_h)


    #Init db
    db = init_db(settings['data_path']+'/passman_data.db')

    #Add entry:
    if new:
        service = input("Enter service name: ")
        uname = input('Enter username: ')
        url = input("Enter service url: ")
        passwd = input("Enter password (leave blank for auto-gen): ")
        if passwd == '':
            passwd = None

        db.insert(Entry(service, uname, url, passwd).encrypt_to_dict(crypt_worker))

    # Find and display Entry:
    if not name == None:
        user = Query()
        entry = db.search(user.name == name)
        if entry == []:
            print("Entry for this service name does not exist.")
            return

        entry = Entry.from_dict(entry[0])

        try:
            entry.decrypt(crypt_worker)
        except InvalidToken:
            print('Incorrect master password.')
            return

        print(entry)


if __name__ == "__main__":
    app()
