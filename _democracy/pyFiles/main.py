#!/usr/bin/env python
# coding=utf-8

# Main | Democracy.
# ------------------------------------------------------------------------------
# josemariasosa 🎹

from user.admin import create_user
from user.admin import user_login


from modules.ssss import ssss_split
from modules.ssss import ssss_combine

# # With test_credentias you can build shards.
# file = 'local/credentials'
# ssss_split(file, t=3, n=5)

# # With some of the shards you could build back the credentials.
# combine = 'data/secret/input_shards.key'
# credentials = ssss_combine(combine)






def main():
    user_login()

if __name__ == '__main__':
    main()

exit()








from functools import reduce
from operator import mul

from cryptography.fernet import Fernet




import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password_provided = "pas--sword" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b'salt__' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

print(key)
exit()










# print(secret)
exit()


print(secret)


print(P)