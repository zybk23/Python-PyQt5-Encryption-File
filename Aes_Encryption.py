#! /usr/bin/python3

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile,join
import time



class encryption_function:
    def __init__(self, key):
        self.key = key

    def one_time_pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size =256):
        message=self.one_time_pad(message)
        initiliaze_vector = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC ,initiliaze_vector)
        return initiliaze_vector + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plain_text = fo.read()
        enc = self.encrypt(plain_text,self.key)
        with open(file_name + ".encrypt",'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self,cipher_text, key):
        initiliaze_vector = cipher_text[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, initiliaze_vector)
        plain_text = cipher.decrypt(cipher_text[AES.block_size:])
        return plain_text.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            cipher_text = fo.read()
        dec = self.decrypt(cipher_text, self.key)
        with open(file_name[:-8], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs=[]
        for dir_name, subdir_list, file_list in os.walk(dir_path):
            for file_name in file_list:
                if(file_name != 'aes_encryption.py' and file_name != 'init_passwd.txt.encrypt'):
                    dirs.append(dir_name+ "//"+ file_name)
        return dirs


    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)
    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)
