#!/usr/bin/env python
# coding=utf-8

# Shamir's Secret Sharing | SSSS | Democracy.
# ------------------------------------------------------------------------------
# josemariasosa 🎹

"""
    ssss-split: prompt the user for a secret and generate a set of corresponding shares.
    ssss-combine: read in a set of shares and reconstruct the secret.

    Options
        -t threshold    Specify the number of shares necessary to reconstruct the secret.
        -n shares       Specify the number of shares to be generated.

    https://linux.die.net/man/1/ssss-split
"""

import json

from mod import Mod
from os import urandom


def import_credentials(file):
    with open(file, 'rb') as f:
        text = f.read()
    return text

def import_mersenne():
    with open('data/utl/mersenne_prime.json', 'r') as f:
        mersenne = json.load(f)
        mersenne = sorted(mersenne, key=lambda d: d['n'])
    return mersenne

def import_combine_shards(file):
    shards = []
    prime = None
    for line in open(file, 'rb'):
        to_insert = line.decode('utf-8').rstrip("\n")
        if 'prime' in to_insert:
            prime = to_insert.replace('prime--', '')
            if prime.isdigit():
                prime = int(prime)
            else:
                msg = 'Something went wrong with the prime number.'
                ValueError(msg)
        else:
            to_insert = to_insert.split('--')[1:]
            if all([x.isdigit() for x in to_insert]):
                shards.append(tuple([int(x) for x in to_insert]))
            else:
                msg = 'Something went wrong with one of the shards.'
                ValueError(msg)
    P = 2**prime - 1
    shards = [(Mod(x[0], P), Mod(x[1], P)) for x in shards]
    return shards, P

def int_from_bytes(s):
    acc = 0
    for b in s:
        acc = acc * 256
        acc += b
    return acc

def evaluate(coefficients, x):
    acc = 0
    power = 1
    for c in coefficients:
        acc += c * power
        power *= x
    return acc

def get_prime(secret):
    mersenne = import_mersenne()
    for prime in mersenne:
        P = 2**prime['p'] - 1
        if secret < P:
            return P, prime['p']
    msg = 'Error: The secret is way too long.'
    raise ValueError(msg)

def export_shards(shards, P):
    file = open('data/secret/shards.key', 'wb')
    for item in shards.items():
        line = (str(item[0]) + '--'
                + str(int(item[1][0])) + '--'
                + str(int(item[1][1])) + '\n')
        line = line.encode('utf-8')
        file.write(line) # The key is type bytes still
    file.write(f'prime--{P}'.encode('utf-8'))
    file.close()

def retrieve_original(secrets, P):
    x_s = [s[0] for s in secrets]
    acc = Mod(0, P)
    for i in range(len(secrets)):
        others = list(x_s)
        cur = others.pop(i)
        factor = Mod(1, P)
        for el in others:
            factor *= el * (el - cur).inverse()
        acc += factor * secrets[i][1]
    return acc

def acceptance_criteria(t, n):
    if isinstance(t, int) and isinstance(n, int):
        if n >= t:
            return True
    return False

def ssss_split(file, t=3, n=5):
    if acceptance_criteria(t, n):
        credentials = import_credentials(file)
        secret = int.from_bytes(credentials, 'little')

        # Define the Nth Mersenne Prime.
        P, prime = get_prime(secret)

        secret = Mod(secret, P)
        polynomial = [secret]
        for i in range(t-1):
            polynomial.append(Mod(int_from_bytes(urandom(16)), P))

        shards = {}
        for i in range(n):
            x = Mod(int_from_bytes(urandom(16)), P)
            y = evaluate(polynomial, x)
            shards[i] = (x, y)

        export_shards(shards, prime)
    else:
        msg = 'Error: At least one of the (t, n) parameters is wrong.'
        ValueError(msg)

def ssss_combine(file):
    retrieved, P = import_combine_shards(file)
    retrieved_secret = retrieve_original(retrieved, P)
    myint = int(retrieved_secret)
    recoveredbytes = myint.to_bytes((myint.bit_length() + 7) // 8, 'little')
    recoveredstring = recoveredbytes.decode('utf-8')
    return recoveredstring
