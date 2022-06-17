import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from aplikasi_keuangan import Ui_MainWindow as halaman_awal
from daftar import Ui_MainWindow as daftar_admin
from menu import Ui_MainWindow as menu_aplikasi
from key_utama import Ui_MainWindow as key
from input_syahriah import Ui_MainWindow as pembayaran

import model as model


class cashflowAplikasi(halaman_awal):
    def __init__(self, dialog):
        halaman_awal.__init__(self)
        self.setupUi(dialog)

        self.pushButtonDaftar.clicked.connect(self.daftarAdmin)
        self.pushButtonMasuk.clicked.connect(self.tampilanMenu)

    def daftarAdmin(self):
        self.daftarAdminMain = QtWidgets.QMainWindow()
        self.daftarAdminUi = daftarAdminAplikasi(self.daftarAdminMain)
        self.daftarAdminMain.show()

    def tampilanMenu(self):
        self.tampilanMenuMain = QtWidgets.QMainWindow()
        self.tampilanMenuUi = tampilanManuAplikasi(self.tampilanMenuMain)
        
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()

        passwordDariDatabase = ""

        try:
            passwordDariDatabase = model.bacaData(username)[1]
        except:
            pass
        
        pesan = QtWidgets.QMessageBox()
        pesan.setIcon(QMessageBox.Warning)
        pesan.setWindowTitle("Perhatian")

        if username == "" or password == "":
            pesan.setText("Masukkan Username dan Password terlebih dahulu..!!")
            pesan.exec_()
        elif password != passwordDariDatabase:
            self.lineEditUsername.setText(None)
            self.lineEditPassword.setText(None)
            pesan.setText("Username atau Password yang anda masukkan salah..!!")
            pesan.exec_()
        elif password == passwordDariDatabase:
            self.tampilanMenuMain.show()

            halamanAwalMain.close()

class daftarAdminAplikasi(daftar_admin):
    def __init__(self, dialog):
        daftar_admin.__init__(self)
        self.setupUi(dialog)
        model.buatDataAdmin()

        self.pushButtonSimpan.clicked.connect(self.simpanAdmin)
        
    def simpanAdmin(self):

        self.username = self.lineEditUsername.text()
        self.password = self.lineEditPassword.text()
        self.passwordLagi = self.lineEditPasswordlagi.text()
        
        self.pesan = QtWidgets.QMessageBox()
        self.pesan.setIcon(QMessageBox.Warning)
        self.pesan.setWindowTitle("Perhatian")
        
        if self.username == "" or self.password == "" or self.passwordLagi == "":
            self.pesan.setText("Masukkan Username dan Password terlebih dahulu..!!")
            self.pesan.exec_()
        elif self.password != self.passwordLagi:
            self.pesan.setText("Password dan Password Lagi beda..!!")
            self.pesan.exec_()
            self.lineEditPassword.setText(None)
            self.lineEditPasswordlagi.setText(None)
        elif self.password == self.passwordLagi:
            self.keyMain = QtWidgets.QMainWindow()
            self.keyUi = key()
            self.keyUi.setupUi(self.keyMain)
            self.keyMain.show()

            self.keyUi.pushButtonSimpan.clicked.connect(self.tampilanKey)
              
    def tampilanKey(self):
        keywordDariTxt = model.keyUtama()
        keywordDariUi = self.keyUi.lineEditKey.text()

        if keywordDariUi == keywordDariTxt:
            model.simpanAdmin(self.username, self.password)
            self.lineEditUsername.setText(None)
            self.lineEditPassword.setText(None)
            self.lineEditPasswordlagi.setText(None)
            self.pesan.setText("Data berhasil disimpan, silahkan Login..!!")
            self.pesan.exec_()
            self.keyMain.close()
            
        else:
            self.pesan.setText("Key Utama salah. Hubungi admin untuk dapat Key Utama..!!")
            self.pesan.exec_()

class tampilanManuAplikasi(menu_aplikasi):
    def __init__(self, dialog):
        menu_aplikasi.__init__(self)
        self.setupUi(dialog)

        self.pushButtonInput.clicked.connect(self.inputPembayaran)

    def inputPembayaran(self):
        self.inputPembayaranMain = QtWidgets.QMainWindow()
        self.inputPembayaranUi = pembayaran()
        self.inputPembayaranUi.setupUi(self.inputPembayaranMain)
        self.inputPembayaranMain.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    halamanAwalMain = QtWidgets.QMainWindow()
    halamanAwalUi = cashflowAplikasi(halamanAwalMain)
    halamanAwalMain.show()


    sys.exit(app.exec_())