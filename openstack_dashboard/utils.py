from itertools import *

def xor_crypt_string(plaintext, key):
    ciphertext = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(plaintext, cycle(key)))
    return ciphertext.encode('base64')

def xor_decrypt_string(ciphertext, key):
    ciphertext = ciphertext.decode('base64')
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(ciphertext, cycle(key)))
