import string
import random
from hashlib import md5
import requests

from pprintjson import pprintjson as ppjson
from src.listaerrores import Error,Fore,Style
from src.new_randomuser import RandomUser
from src.config import *

class TempMail(RandomUser):
    errorReconect = 0
    errorMaxReconect = 2


    login=None
    domain=None
    api_domain="api4.temp-mail.org"
    domains=[]
    listerrorExecutinModulo="TEMPMAIL"
    mailid=None
    mail=None
    def __init__(self,login=None, domain=None, api_domain="api4.temp-mail.org"):
        Error.info("Iniciando configuracoin de TempMail")
        self.login=login
        self.domain=domain
        self.api_domain=api_domain
        Error.executing("Buscando domains validos para tempmail",self.listerrorExecutinModulo)
        url = f"https://{self.api_domain}/request/domains/format/json/"
        r = requests.get(url)
        self.domains = r.json()
    def getHash(self,email=None):
        if email is None:
            self.mailid = md5(self.mail.encode('utf-8')).hexdigest()
        else:
            self.mailid = md5(email.encode('utf-8')).hexdigest()
    def getEmailLogin(self,setnew=False):
        if setnew:
            if self.login is None:
                Error.executing(f"Generando una cuenta de email nueva",self.listerrorExecutinModulo)
                if len(self.Users)==0:
                    self.generate(1)
                self.login = self.Users[0]['username']
            if self.domain is None:
                Error.executing("Buscando domains validos para tempmail",self.listerrorExecutinModulo)
                url = f"https://{self.api_domain}/request/domains/format/json/"
                try:
                    r = requests.get(url)
                except Exception as e:
                    Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
                    Error.warn(e)
                    if self.errorReconect>self.errorMaxReconect:
                        self.errorReconect = 0
                        Error.e(1,f"No es posible mostrar lista de correo")
                        return False
                    else:
                        self.errorReconect += 1
                        Error.info("Intentando reconectar".center(50,'.'))
                        self.getEmailLogin(setnew)
                else:
                    self.domains = r.json()
                    self.domain = random.choice(self.domains)
            self.mail = "{}{}".format(self.login,self.domain)
            self.mailid = self.getHash()
        else:
            if self.login is None:
                n = self.generate(1)
                Error.executing("Selecionando username para el email",self.listerrorExecutinModulo)
                self.login = n[0]['username']
            if self.domain is None:
                Error.executing("Selecionando dominio de email",self.listerrorExecutinModulo)
                self.domain = random.choice(self.domains)
            mail = "{}{}".format(self.login,self.domain)
            if self.mail is None:
                self.mail = mail
                Error.executing(f"Generando HASH del email: {Fore.YELLOW}{self.mail}{Style.RESET_ALL}",self.listerrorExecutinModulo)
                self.mailid = md5(self.mail.encode('utf-8')).hexdigest()
        return self.mail
    def getInboxMail(self):
        # https://api4.temp-mail.org/request/mail/id/b867f1fd7346280901b19da061fdc90e/format/json
        Error.executing(f"Verificando inbox de:{Fore.YELLOW}{self.mail}{Style.RESET_ALL}",self.listerrorExecutinModulo)
        if self.mailid is None:
            Error.executing("No se ha encontrado un HASH de email, procediendo a generar cuenta",self.listerrorExecutinModulo)
            self.getEmailLogin(True)
        url = f"https://{self.api_domain}/request/mail/id/{self.mailid}/format/json"
        try:
            r = requests.get(url)
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
            Error.warn(e)
            if self.errorReconect>self.errorMaxReconect:
                self.errorReconect = 0
                Error.e(1,f"No es posible mostrar lista de correo")
                return False
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.getInboxMail(idemail)
        else:
            mails = r.json()
            if 'error' in mails:
                Error.info(f"La cuenta de correo {Fore.YELLOW}{self.mail}{Style.RESET_ALL}  no tiene emails en INBOX")
                mails = []
            else:
                for mail in mails:
                    mail.pop("mail_html")
                    mail.pop("mail_text_only")
            return mails
    def deleteEmail(self,idemail):
        Error.executing(f"Eliminando email de {Fore.YELLOW}{self.mail}{Style.RESET_ALL} con id:{idemail}",self.listerrorExecutinModulo)
        url = f"https://{self.api_domain}/request/delete/id/{idemail}/format/json"
        try:
            r = requests.get(url)
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
            Error.warn(e)
            if self.errorReconect>self.errorMaxReconect:
                self.errorReconect = 0
                Error.e(1,f"No es posible eliminar el email:{idemail}")
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.deleteEmail(idemail)
        else:
            rj = r.json()
            if rj["result"]=="success":
                Error.ok(f"Se elimino el email:{idemail} con exito")
        pass
    def deleteAllEmails(self):
        Error.executing(f"{Fore.RED}Eliminando todos los emails de{Style.RESET_ALL} {Fore.YELLOW}{self.mail}{Style.RESET_ALL}",self.listerrorExecutinModulo)
        mails = self.getInboxMail()
        if len(mails)!=0:
            for mail in mails:
                self.deleteEmail(mail['mail_id'])
