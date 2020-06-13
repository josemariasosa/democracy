#!/usr/bin/env python
# coding=utf-8

# User Admin | Democracy.
# ------------------------------------------------------------------------------
# josemariasosa 🎹

import os
import json
import base64
from getpass import getpass

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def import_users(account, user):
    with open('data/api_db/User.json', 'r') as f:
        users = json.load(f)
    if len(users) > 0:
        users = [
            x for x in users
            if (x['account'] == account) and (x['user'] == user)
        ]
    return users

def import_users_pass(account, user, _pass):
    with open('data/api_db/User.json', 'r') as f:
        users = json.load(f)
    if len(users) > 0:
        users = [
            x for x in users
            if ((x['account'] == account)
                and (x['user'] == user)
                and (x['pass']) == _pass)
        ]
    return users

def pass_to_key(password, account):
    password = password.encode()
    salt = account.encode('utf-8')  # The salt is the account name.
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key.decode("utf-8")

def validate_password(account):
    while True:
        _pass = getpass('Write down your pass: ')
        if getpass('Write password again: ') == _pass:
            break;
        else:
            print('==> Passwords does not match!')
            print('==> Try again, or exit.\n')
    return pass_to_key(_pass, account)

def create_account():
    _account = input('Give me a **unique** account name: ')
    _user = input('Give me user name: ')
    _pass = validate_password(_account)
    return {
        'account': _account,
        'user': _user,
        'pass': _pass
    }

def check_valid_new_user(new_user):
    users = import_users(account=new_user['account'],
                         user=new_user['user'])
    if len(users) == 0:
        return True
    return False

def check_user_login(user):
    users = import_users_pass(account=user['account'],
                         user=user['user'],
                         _pass=user['pass'])
    if len(users) == 1:
        return True
    return False

def insert_user(user):
    with open('data/api_db/User.json', 'r') as f:
        users = json.load(f)
    users.append(user)
    with open('data/api_db/User.json', 'w') as f:
        json.dump(users, f)

def create_user():
    new_user = create_account()
    if check_valid_new_user(new_user):
        print('************')
        insert_user(new_user)
    else:
        msg = 'User is already taken!'
        raise ValueError(msg)

def user_login():
    _account = input('Democracy account: ')
    _user = input('user: ')
    _pass = getpass('pass: ')
    user = {
        'account': _account,
        'user': _user,
        'pass': pass_to_key(_pass, _account)
    }
    if check_user_login(user):
        print('success!')
    else:
        print('fail')

    exit()

