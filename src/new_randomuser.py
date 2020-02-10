import random
import xlrd
import time
import string
import hashlib
import sys
import os.path
import unidecode
from src.listaerrores import Error,Fore,Style


class RandomUser:
    Nombres = []
    Users = []
    path=sys.path[0]
    sru_listerrorExecutinModulo="S-RANDUSER"
    def __init__(self):
        Error.executing("Iniciando la creacion de nombres aleatorios",self.sru_listerrorExecutinModulo)
        self.path = sys.path[0]
        self.username = "username"
        # self.generate()

    def generate(self,number=10,file='',index=0):
        Error.executing("Cargando archivo de nombres...",self.sru_listerrorExecutinModulo)
        if not file.strip():
            file =self.path+'/libs/nombres.xlsx'
            Error.executing(f"Archivo {file} por defecto",self.sru_listerrorExecutinModulo)
        if os.path.isfile(file):
            wb = xlrd.open_workbook(file)
            sheet = wb.sheet_by_index(index)
            Error.executing(f"Generando nombres",self.sru_listerrorExecutinModulo)
            for i in range(sheet.nrows):
                nombre = sheet.cell_value(i, 0).strip().split()
                for j in range(len(nombre)):
                    for rex in [string.punctuation[i:i+1] for i in range(0, len(string.punctuation), 1)]:
                      nombre[j] = nombre[j].replace(rex,'',10)
                      nombre[j] = unidecode.unidecode(nombre[j])
                    self.Nombres.append(nombre[j].lower())
            Error.executing(f"Generando informacion de cuentas...",self.sru_listerrorExecutinModulo)
            for i in range(number):
                password = password = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
                fname = random.choice(self.Nombres)
                lname = random.choice(self.Nombres)
                fullname = "%s %s"%(fname,lname)
                randomNumber = random.randrange(10,99)
                randomLetters = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
                if random.choice([True,False]):
                    username = "%s_%s_%s"%(fname,f"{randomLetters}{randomNumber}",lname)
                else:
                    username = "%s_%s.%s"%(fname,lname,f"{randomLetters}{randomNumber}")
                self.Users.append({
                    "fname":fname,
                    "lname":lname,
                    "fullname":fullname,
                    "username":username,
                    "password":password,
                    "country":"CO",
                    "age":random.randrange(18,50)
                })
            Error.ok(f"Informacion de cuentas generada: #{len(self.Users)} habilitados.")
            return self.Users
        else:
            sys.exit(Error.e(1,"FILE %s No Existe."%(file)))
