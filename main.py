import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from aplikasi_keuangan import Ui_MainWindow as halaman_awal
from daftar import Ui_MainWindow as daftar_admin
from menu import Ui_MainWindow as menu_aplikasi
from key_utama import Ui_MainWindow as key
from input_syahriah import Ui_MainWindow as pembayaran
from input_nama import Ui_MainWindow as nama
from riwayat_pembayaran import Ui_MainWindow as riwayat

import model as model


class cashflowAplikasi(halaman_awal):
    def __init__(self, dialog):
        halaman_awal.__init__(self)
        self.setupUi(dialog)

        self.pushButtonDaftar.clicked.connect(self.daftarAdmin)
        self.pushButtonMasuk.clicked.connect(self.tampilanMenu)

        self.pesan = QtWidgets.QMessageBox()
        self.pesan.setIcon(QMessageBox.Warning)
        self.pesan.setWindowTitle("Perhatian")

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

        if username == "" or password == "":
            self.pesan.setText("Masukkan Username dan Password terlebih dahulu..!!")
            self.pesan.exec_()
        elif password != passwordDariDatabase:
            self.lineEditUsername.setText(None)
            self.lineEditPassword.setText(None)
            self.pesan.setText("Username atau Password yang anda masukkan salah..!!")
            self.pesan.exec_()
        elif password == passwordDariDatabase:
            self.tampilanMenuMain.show()

            halamanAwalMain.close()

class daftarAdminAplikasi(daftar_admin):
    def __init__(self, dialog):
        daftar_admin.__init__(self)
        self.setupUi(dialog)
        model.buatDataAdmin()

        self.pushButtonSimpan.clicked.connect(self.simpanAdmin)
        
        self.pesan = QtWidgets.QMessageBox()
        self.pesan.setIcon(QMessageBox.Warning)
        self.pesan.setWindowTitle("Perhatian")

    def simpanAdmin(self):

        self.username = self.lineEditUsername.text()
        self.password = self.lineEditPassword.text()
        self.passwordLagi = self.lineEditPasswordlagi.text()
        
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

        self.pushButtonInputPembayaran.clicked.connect(self.inputPembayaran)
        self.pushButtonInputNama.clicked.connect(self.inputNama)
        self.pushButtonRiwayat.clicked.connect(self.riwayatPembayaran)

        self.pesan = QtWidgets.QMessageBox()
        self.pesan.setIcon(QMessageBox.Warning)
        self.pesan.setWindowTitle("Perhatian")

    def inputPembayaran(self):
        self.inputPembayaranMain = QtWidgets.QMainWindow()
        self.inputPembayaranUi = pembayaran()
        self.inputPembayaranUi.setupUi(self.inputPembayaranMain)
        self.inputPembayaranMain.show()

        self.inputPembayaranUi.pushButton.clicked.connect(self.bayar)

        self.namaDiComboBox()
        self.bulanDiComboBox()
        self.nominalLabel()
        self.inputPembayaranUi.comboBoxNama.currentTextChanged.connect(self.nominalLabel)
        self.inputPembayaranUi.comboBoxBulan.currentTextChanged.connect(self.nominalLabel)


    def bayar(self):
        self.namaSaatIni = self.inputPembayaranUi.comboBoxNama.currentText()
        self.bulanSaatIni = self.inputPembayaranUi.comboBoxBulan.currentText()
        
        self.indexBulan = (model.ambilIndexBulan(self.bulanSaatIni.lower())) + 1
        self.data = model.dataDariNama(self.namaSaatIni)[0]
        
        try:
            self.nominal = int(self.inputPembayaranUi.lineEditUang.text())
            model.bayarDenganNamaDanBulan(self.namaSaatIni, self.bulanSaatIni, self.nominal)

            self.inputPembayaranUi.labelInfo.setText("Pembayaran berhasil ditambahkan..!!")
            self.inputPembayaranUi.lineEditUang.setText(None)
        except:
            self.inputPembayaranUi.labelInfo.setText("Masukkan angka..!!")

    def nominalLabel(self):
        self.namaSaatIni = self.inputPembayaranUi.comboBoxNama.currentText()
        self.bulanSaatIni = self.inputPembayaranUi.comboBoxBulan.currentText()

        self.indexBulan = (model.ambilIndexBulan(self.bulanSaatIni.lower())) + 1
        self.data = model.dataDariNama(self.namaSaatIni)[0]

        self.inputPembayaranUi.labelInfo.clear()
        self.inputPembayaranUi.labelInfo.setText(str(self.data[self.indexBulan]))

    def namaDiComboBox(self):
        namaNama = model.ambilNama()
        for nama in namaNama:
            self.inputPembayaranUi.comboBoxNama.addItem(nama[0])

    def bulanDiComboBox(self):
        bulanBulan = model.ambilBulan()
        for bulan in bulanBulan:
            self.inputPembayaranUi.comboBoxBulan.addItem(bulan[0].capitalize())

    def inputNama(self):
        self.inputNamaMain = QtWidgets.QMainWindow()
        self.inputNamaUi = nama()
        self.inputNamaUi.setupUi(self.inputNamaMain)
        self.inputNamaMain.show()
        self.tampilkanNama()

        self.inputNamaUi.pushButtonSimpan.clicked.connect(self.tambahNama)
        self.inputNamaUi.pushButtonSelesai.clicked.connect(self.inputNamaMain.close)

    def tambahNama(self):
        self.namaBaru = self.inputNamaUi.lineEditnama.text()
        
        model.tambahNama(self.namaBaru)
        self.pesan.setText(f"Nama {self.namaBaru} berhasil ditambahkan..!!")
        self.pesan.exec_()
        self.inputNamaUi.lineEditnama.setText(None)
        
        self.inputNamaMain.close()
        self.inputNama()

    def tampilkanNama(self):
        dataNama = model.ambilNama()

        for nama in dataNama:
            rowPosition = self.inputNamaUi.tableWidgetNama.rowCount()
            self.inputNamaUi.tableWidgetNama.insertRow(rowPosition)
            self.inputNamaUi.tableWidgetNama.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(rowPosition + 1)))
            self.inputNamaUi.tableWidgetNama.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(nama[0]))

    def riwayatPembayaran(self):
        self.riwayatPembayaranMain = QtWidgets.QMainWindow()
        self.riwayatPembayaranUi = riwayat()
        self.riwayatPembayaranUi.setupUi(self.riwayatPembayaranMain)
        self.riwayatPembayaranMain.show()

        self.riwayatPembayaranUi.pushButtonKembali.clicked.connect(self.riwayatPembayaranMain.close)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    halamanAwalMain = QtWidgets.QMainWindow()
    halamanAwalUi = cashflowAplikasi(halamanAwalMain)
    halamanAwalMain.show()


    sys.exit(app.exec_())