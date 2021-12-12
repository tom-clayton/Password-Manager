
"""
securestrings.py 

A python library for saving and loading encrypted strings for securing 
passwords, etc. with AES256 bit encryption using pycryptodome. 

Tom Clayton 2020.

TODO change key generation.

"""

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(data, password, iv=None):
    """encrypt data"""
    key = hashlib.sha256(password.encode()).digest() 
    
    if iv:
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        data = cipher.encrypt(pad(data, 16))
        return data 
    else:
        cipher = AES.new(key, AES.MODE_CBC)
        data = cipher.encrypt(pad(data, 16))
        return cipher.iv + data
        
            
def decrypt(data, password, iv):
    """decrypt data"""
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    try:
        return unpad(cipher.decrypt(data), 16)
    except Exception as e: 
        return None

def save_string(filename, password, string):
    """save encrypted string"""
    with open(filename, 'wb') as fo:
        fo.write(encrypt(string.encode(), password))

def load_string(filename, password):
    """load encrypted string"""
    with open(filename, 'rb') as fo:
        load_data = fo.read()
    
    iv = load_data[:16]       
    data = load_data[16:]
    return decrypt(data, password, iv).decode()

