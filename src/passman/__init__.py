#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cryptography.fernet import Fernet
from tinydb import TinyDB, Query
import click
import secrets
import toml
import os
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

    @staticmethod
    def from_dict(dat: dict):
        ent = entry(dat['name'], dat['username'], dat['url'], dat['password'])
        return ent

    @staticmethod
    def generate_password(length: int = 20):
        return secrets.token_urlsafe(length)

    def __str__(self):
        return f'Service: {self.name}\nUsername: {self.username}\nURL: {self.url}\nPassword: {self.password}'


@click.command()
@click.argument('name', default=None)
@click.option('--config',
              '-c',
              default=os.path.expanduser('~/.config/passman.toml'))
def app(name, config):
    #Read Config file
    settings = toml.load(config)
    #Init db
    db = init_db(settings['db_path'])


if __name__ == "__main__":
    app()
