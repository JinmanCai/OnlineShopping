import hashlib
import os

##Generate random 32 bytes
salt = os.urandom(32)
print(salt)
##Hasing the password with the salt
##hashlib.pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)
hash_value = hashlib.pbkdf2_hmac('sha256', b'password', salt, 100000)
print(hash_value)
hash_value = hash_value.hex()
print(hash_value)

