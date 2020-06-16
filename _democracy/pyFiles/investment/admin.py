#!/usr/bin/env python
# coding=utf-8

# Investment Admin | Democracy.
# ------------------------------------------------------------------------------
# josemariasosa 🌍

import json

from user.admin import get_default_currency
from movement.admin import create_movement

def get_user_investments(user):
    with open('data/api_db/Investment.json') as f:
        investments = json.load(f)
    if len(investments) > 0:
        investments = [
            x for x in investments
            if ((x['account'] == user['account'])
                and (x['user'] == user['user']))
        ]
    return investments

def is_valid_name(name, user, eval_if_in_db=True):
    investments = get_user_investments(user)
    if eval_if_in_db:
        return name not in [x['name'] for x in investments]
    return name in [x['name'] for x in investments]

def request_investment_parameters(user):
    while True:
        name = input('How you want to call this investment: ')
        if is_valid_name(name, user, eval_if_in_db=True):
            break
        print('==> The name is already taken! Choose different.')
    total = input('How much do you currently have: ')
    if total.isdigit():
        total = int(total)
    else:
        msg = 'The input must be an integer.'
        raise ValueError(msg)
    return {
        'name': name,
        'total': total,
        'currency': get_default_currency(user),
        'account': user['account'],
        'user': user['user']
    }

def request_deposit_parameters(user):
    while True:
        name = input('Deposit to investment name: ')
        if is_valid_name(name, user, eval_if_in_db=False):
            break
        print('==> The name was not found. Try again!')
    total = input('How much do you want to deposit: ')
    return {
        'name': name,
        'total': total,
        'currency': get_default_currency(user),
        'account': user['account'],
        'user': user['user']
    }

def insert_investment(investment):
    with open('data/api_db/Investment.json', 'r') as f:
        investments = json.load(f)
    investments.append(investment)
    with open('data/api_db/Investment.json', 'w') as f:
        json.dump(investments, f)

def create_investment(user):
    new_investment = request_investment_parameters(user)
    insert_investment(new_investment)
    movement = {
        'type': 'deposit',
        'account': user['account'],
        'user': user['user'],
        'currency': new_investment['currency'],
        'total': new_investment['total']
    }
    create_movement(user, movement)
    return None

def get_investment_total(user, account, name):
    investments = get_user_investments({'user': user, 'account': account})
    return [x['total'] for x in investments if x['name'] == name]

def update_investment(movement_type, deposit):
    user = deposit['user']
    account = deposit['account']
    name = deposit['name']
    total = get_investment_total(user, account, name)
    new_value = total + new_value
    print(new_value)
    exit()
    # if movement_type == 'deposit':


def deposit_investment(user):
    movement_type = 'deposit'
    deposit = request_deposit_parameters(user)
    update_investment(movement_type, deposit)
    print(deposit)
    print('end')
    exit()
    