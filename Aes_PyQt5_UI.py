#! /usr/bin/python3
from Crypto.Hash import MD2
import Aes_Encryption
import os
import time
import requests
import sys
from PyQt5.QtWidgets import qApp, QTextEdit, QPushButton, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLayout, \
    QFileDialog,QLineEdit,QInputDialog

def key_generator():
    new_key=MD2.new()
    new_key.update(input("Yeni key değeri giriniz:"))
    return new_key.hexdigest()

key = key_generator()
print("Oluşturulan key değeri:",key)
enc = Aes_Encryption.encryption_function(key)
clear = lambda:os.system('cls')

class Pencere(QWidget):

    def __init__(self):

        super().__init__()

        self.buton()

    def buton(self):

        self.dosya_sifrele=QPushButton("Dosya şifrelemek için tıklayın")

        self.sifre_kaldir=QPushButton("Dosyadaki şifreyi kaldırmak için tıklayın")

        self.tum_dosyalari_sifrele=QPushButton("Tüm dosyaları şifrelemek için tıklayın")

        self.tum_sifreleri_kaldir=QPushButton("Tüm şifreleri kaldırmak için tıklayın")

        self.programi_calistir=QPushButton("Programı çalıştırmak için basınız")

        self.yazi_alani=QTextEdit()

        self.textedit=QLineEdit()
        self.textedit.move(20, 20)
        self.textedit.resize(160, 40)



        v_box=QVBoxLayout()
        v_box.addWidget(self.yazi_alani)
        v_box.addWidget(self.textedit)
        v_box.addLayout(v_box)
        #h_box=QHBoxLayout()

        v_box.addWidget(self.programi_calistir)
        v_box.addStretch()

        v_box.addWidget(self.dosya_sifrele)
        v_box.addStretch()
        v_box.addWidget(self.sifre_kaldir)
        v_box.addStretch()
        v_box.addWidget(self.tum_dosyalari_sifrele)
        v_box.addStretch()
        v_box.addWidget(self.tum_sifreleri_kaldir)


        self.setLayout(v_box)
        self.setWindowTitle("AES Şifreleme Programı")

        self.dosya_sifrele.clicked.connect(self.tek_dosya_sifrele)
        self.tum_dosyalari_sifrele.clicked.connect(self.tumunu_sifrele)
        self.tum_sifreleri_kaldir.clicked.connect(self.tumunu_kaldir)
        self.programi_calistir.clicked.connect(self.calistir)
        self.sifre_kaldir.clicked.connect(self.tek_dosya_kaldir)
        self.show()

    def calistir(self):
        if os.path.isfile('init_passwd.txt.encrypt'):
            while True:
                password,ok= QInputDialog.getText(self,"Parolanızı giriniz","Parolanızı giriniz")
                if ok :
                    enc.decrypt_file("init_passwd.txt.encrypt")
                    p = ''
                    with open("init_passwd.txt", "r") as f:
                        p = f.readlines()
                    if p[0] == password:
                        enc.encrypt_file("init_passwd.txt")
                        self.yazi_alani.append("Program Çalışıyor.....\nAşağıdaki Seçeneklerden Birini Seçiniz...")
                        break

        else:
            while True:
                clear()
                password,ok = QInputDialog.getText(self,"Şifrelemek için parolanızı giriniz","şifrelemek için parolanızı giriniz")
                if ok:
                    self.textedit.setText("Parolanızı belirlediniz")
                repassword,ok= QInputDialog.getText(self,"Doğrulamak için parolanızı giriniz","doğrulamak için parolanızı giriniz")
                if ok :
                    self.textedit.setText("Parolanızı doğruladınız")
                if password == repassword:
                    break
                else:
                    self.yazi_alani.append("Girilen parola değerleri aynı değil!")
            f = open("init_passwd.txt", "w+")
            f.write(password)
            f.close()
            enc.encrypt_file("init_passwd.txt")
            self.yazi_alani.append("Başlangıç ayarları yapıldı lütfen programı tekrar başlatın! ")
            time.sleep(1)

    def tumunu_sifrele(self):
        enc.encrypt_all_files()
        self.yazi_alani.append("Tüm Dosyalar Şifrelendi...")

    def tumunu_kaldir(self):
        enc.decrypt_all_files()
        self.yazi_alani.append("Tüm Dosyaların Şifresi Çözüldü...")

    def tek_dosya_sifrele(self):
        enc.encrypt_file(QInputDialog.getText(self,"dosya şifreleme","Şifrelenecek dosyanın ismini giriniz"))
        self.yazi_alani.append(QInputDialog.getText()+"dosyası şifrelendi..")

    def tek_dosya_kaldir(self):
        enc.decrypt_file(QInputDialog.getText(self,"şifre kaldırma","Şifresini kaldırmak istediğiniz dosyanın ismini giriniz"))
        self.yazi_alani.append(QInputDialog.getText()+"dosyasının şifresi çözüldü..")

app=QApplication(sys.argv)
pencere=Pencere()
sys.exit(app.exec_())
