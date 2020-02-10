from src.listaerrores import Error,Fore,Style
from src.new_sqlconnect import Sql
from src.config import Config as BotConfig
import os
welcome = u"\u2622"f'\t{Fore.RED}..::| INICIANDO PROGRAMA |::..{Style.RESET_ALL}\t'u"\U0001F47D"
powerby = u"\U0001F6E1"f" Creado por: {Fore.MAGENTA}edens{Style.RESET_ALL} "u"\u269B"
version = ' v0.1 '
namepackage = ' Bot Instagram: Skipp = Version: {} '.format(version)
os.system('clear')
width = 100
print()
print(welcome.center(width-len(welcome),' '))
print(powerby.center(width-len(powerby),' '))
print(namepackage.center(width-len(namepackage),' '))
print()
from src.new_randomuser import RandomUser
from src.new_instagram import Instagram
from pprintjson import pprintjson as ppjson
# from bs4 import BeautifulSoup
import sys
# import json
# import signal
#### inicio de programa ########


emailhush = BotConfig["hushmail"]["loginEmail"]
passhush  = BotConfig["hushmail"]["loginPass"]

sql = Sql()

while True:
    try:
        f = sql.lastEmailAliasAvailable()
        if f:
            createdby = f['createdby']
            usedby = f['usedby']
            if createdby=='1':
                a = sql.Select(["alias"]).From('alias').Where([("id",usedby)]).Run()[0]['alias']
                username = a.split("@")[0]
                fullname = username.split(".")[0].split("_")
                if len(fullname)==3:
                    fullname.pop(1)
                    fullname =" ".join(fullname)
                else:
                    fullname =" ".join(fullname)
                instagram = Instagram()
                instagram.createAccount(a, fullname,username,'temp_password', True)
            else:
                m = sql.Select(["*"]).From('emails').Where([("id",usedby),("hasinstagram","0")]).Run()[0]
                u=m['email']
                username = u.split("@")[0]
                fullname = username.split(".")[0].split("_")
                if len(fullname)==3:
                    fullname.pop(1)
                    fullname =" ".join(fullname)
                else:
                    fullname =" ".join(fullname)
                instagram = Instagram()
                instagram.createAccount(u, fullname, username, 'temp_password', True)
        else:
            users = RandomUser()
            for user in users.generate(1):
                ppjson(user)
                sys.exit()
    except KeyboardInterrupt:
        print()
        Error.warn("EJECUCION DETENIDA POR EL USUSARIO".center(70,'.'))
        sys.exit()

    """
        en esta parte se escoje si se crean cuentas de correo o se utilizan
        de una base de datos

        despues de crear o selecionar la cuenta de correo
        procedemos a crear la cuentas de instagram

    """
