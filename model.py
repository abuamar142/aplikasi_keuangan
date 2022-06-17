import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

def buatDataAdmin():
    try:
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS  data_admin
                ([username] TEXT, [password] TEXT)
        ''')
        print("Tabel Data Admin berhasil dibuat..!!")
        connection.commit()
    except sqlite3.Error as error:
        print(error)

def buatDataSyahriah():
    try:
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS  syahriah
                ([nama] TEXT, [syawal]      INTEGER, [dzulqo'dah]   INTEGER, [dzulhijjah]    INTEGER,
                            [muharram]      INTEGER, [safar]        INTEGER, [robi'ul awal]  INTEGER,
                            [robi'ul akhir] INTEGER, [jumadil awal] INTEGER, [jumadil akhir] INTEGER,
                            [rajab]         INTEGER, [sya'ban]      INTEGER, [ramadhan]      INTEGER)
        ''')
        print("Tabel Syahriah berhasil dibuat..!!")
        connection.commit()
    except sqlite3.Error as error:
        print(error)

def simpanAdmin(username, password):
    try:    
        cursor.execute('''
                INSERT INTO data_admin(username, password)
                VALUES (?,?)
        ''',    ((username,password)))
        connection.commit()
        print("Data berhasil ditambahkan..!!")
    except sqlite3.Error as error:
        print(error)

def bacaData(username):
    try:
        data = cursor.execute('''
                SELECT * FROM data_admin WHERE username=?
        ''',(username,))
        baris = data.fetchall()
        return(baris[0])
    except sqlite3.Error as e:
        print(e)

def keyUtama():
    keys = open ("key.txt", "r")
    key = (keys.read()).strip()
    
    return key

def tambahNama(nama):
    try:    
        cursor.execute('''
                INSERT INTO syahriah(nama)
                VALUES (?)
        ''',    (nama,))
        connection.commit()
        print("Data berhasil ditambahkan..!!")
    except sqlite3.Error as error:
        print(error)

def ambilNama():
    try:
        data = cursor.execute('''
                SELECT * FROM syahriah
        ''')
        baris = data.fetchall()
        return baris
    except sqlite3.Error as e:
        print(e)