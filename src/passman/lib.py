#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from cryptography.fernet import Fernet
from tinydb import Query, TinyDB


def load_from_key(fname: str) -> Fernet:
    try:
        with open(fname, 'rb') as f:
            key = f.read()
            f.close()
    except FileNotFoundError as e:
        raise Exception('Key file not found: ')

    return Fernet(key)


def gen_key_file(fname: str):
    key = Fernet.generate_key()
    try:
        with open(fname, 'wb') as f:
            f.write(key)
            f.close()
    except:
        raise Exception('Error occurred while writing key to file.')


def init_db(fname: str) -> TinyDB:
    if not os.path.exists(fname):
        with open(fname, 'w+') as f:
            f.write('')
            f.close()
    db: TinyDB = TinyDB(fname)
    return db
