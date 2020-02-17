import requests,time, sys, urllib,os,random
from pprintjson import pprintjson as ppjson
from bs4 import BeautifulSoup
from tqdm import tqdm

from src.listaerrores import Error,Fore,Style
from src.new_sqlconnect import Sql
from src.config import Config as BotConfig
from src.new_randomproxy import RandomProxy
from src.new_tempmail import TempMail

widthCenter=70
# Error.info(''.center(widthCenter,'='))
# Error.info('iniciando temp mail y sql'.center(widthCenter,'='))
# Error.info(''.center(widthCenter,'='))
# tm=TempMail();
# sql = Sql()

class Instagram:
    """
    Docstring for Instagram
    #### ESTRUCTURA DE DATOS CREAR CUENTA #####

    #### FORMATO DE PASSWORD WNCRYPTED #####
    #PWD_INSTAGRAM_BROWSER:6:1579994909018:AfVQAOyhSqLJw4spFafaHs6ri+FxbZ1pIfEkvDMtxcpB9rQmBv2TDsoXcCEH/tysQl+Qvxqxi6MKm7/NuabZ4V/DljvtcqaLh00eSvqih3Oi9deYa50icpd5H4XX8CGa7HACzQ==
    """
    session = False
    proxy=None
    errorReconect = 0
    errorMaxReconect = 2
    errorMaxIntent = 2
    waitTimeRange=100
    listerrorExecutinModulo = 'INSTAGRAM'

    webCreateUrlAttempt = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
    webCreateUrl = "https://www.instagram.com/accounts/web_create_ajax/"
    webCreateUrlSharedData = "https://www.instagram.com/data/shared_data/"
    webLoginUrl = "https://www.instagram.com/accounts/login/ajax/"
    ######## varibles globales ########

    csrftoken = None
    xInstagramAJAX = None
    deviceId = None
    public_key=None
    key_id=None
    AcceptLanguage=None

    ####### Variables para crear la cuenta #########
    table='emails'
    column="email"
    createdby='0'
    nombre=None
    email=None
    username=None
    password=None
    enc_password=None
    idemail=None
    usedby=None
    ########## requests and response
    p_table = None

    def __init__(self):
        ##os.system('clear')
        Error.info("Configurando Instagram para su uso")
        self.proxy = RandomProxy()
        urlproxy = self.proxy.get()
        self.session = requests.Session()
        Error.executing("Configurando proxy",self.listerrorExecutinModulo)
        # self.session.proxies = {
        #     "http":"{}".format(urlproxy),
        #     "https":"{}".format(urlproxy),
        # }
        self.sql = Sql()
    def setVariablesCreate(self,**kw):
        Error.executing("Definiendo variables...",self.listerrorExecutinModulo)
        for item in kw:
            setattr(self,item,kw[item])
        return False;
    def initialConnect(self):
        self.changeProxy()
        Error.executing(f"Estableciendo conexion inicial",self.listerrorExecutinModulo)
        try:
            resp = requests.get(self.webCreateUrlSharedData)
        except requests.exceptions.ProxyError as err:
            Error.warn("Reconectando".center(widthCenter,'-'))
            Error.e(1,err)
            self.initialConnect()
        except requests.exceptions.SSLError as err:
            Error.warn("Reconectando".center(widthCenter,'-'))
            Error.e(1,err)
            self.initialConnect()
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
            Error.warn(e)
            if self.errorReconect>self.errorMaxReconect:
                self.errorReconect = 0
                self.initialConnect()
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(widthCenter,'.'))
                self.initialConnect()
        else:
            rjson=resp.json()
            self.csrftoken = rjson['config']['csrf_token']
            self.xInstagramAJAX = rjson['rollout_hash']
            self.AcceptLanguage = rjson['language_code']
            self.deviceId = rjson['device_id']
            self.public_key = rjson['encryption']['public_key']
            self.key_id = rjson['encryption']['key_id']
            return rjson
        return False;
    def guardarcuentacreada(self):
        self.sql.query(f"INSERT INTO emails(nombre,email,hasinstagram,istemp) VALUES('{self.nombre}','{self.email}','1','1')");
        self.sql.db.commit()
        self.idemail = self.sql.cursor.lastrowid;
        self.usedby = self.idemail;
        payload={
            "username":self.username,
            "password":self.password,
            "createdby":self.createdby,
            "usedby":self.usedby,
        }
        self.sql.createInstagramAccont(**payload)
        return self
    def emailIsTaken(self):
        Error.executing(f"el correo {self.email} alparecer esta en uso.",self.listerrorExecutinModulo)
        self.email = tm.getEmailLogin(True)
        Error.executing(f"Se actualizo a: {Fore.RED}{self.email}{Style.RESET_ALL}",self.listerrorExecutinModulo)
        return self.email
    def setNewEmail(self):
        Error.executing(f"el correo {self.email} alparecer esta en uso.",self.listerrorExecutinModulo)
        from src.new_tempmail import TempMail
        self.email = tm.getEmailLogin(True)
        Error.executing(f"Se actualizo a: {Fore.RED}{self.email}{Style.RESET_ALL}",self.listerrorExecutinModulo)
        return self.email
    def postCreateAccount(self):
        Error.info(f"{'Username:'+self.username.center(35,'~')}_{'Email: '+self.email.center(55,'~')}")
        formData = {
            'email':self.email,
            'password':self.password,
            'username':self.username,
            'first_name':self.nombre,
            'seamless_login_enabled' : '1',
            'tos_version' : 'row',
            'opt_into_one_tap' : 'false'
        }
        self.session = requests.Session();
        Error.executing("Actualizando Header",self.listerrorExecutinModulo)
        self.session.headers.update({
            "Accept-Language":self.AcceptLanguage,
            "Content-Type":"application/x-www-form-urlencoded",
            "X-CSRFToken":self.csrftoken,
            "X-IG-App-ID":"936619743392459",
            "X-IG-WWW-Claim":"0",
            "X-Instagram-AJAX":self.xInstagramAJAX,
            "X-Requested-With":"XMLHttpRequest",
            "Host": "www.instagram.com",
            "Origin": "https://www.instagram.com",
            "Referer":"https://www.instagram.com/",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
        });
        Error.executing("Actualizando Cookies",self.listerrorExecutinModulo)
        self.session.cookies.update({
            "csrftoken":self.csrftoken,
            "ig_did":self.deviceId,
        })
        self.session.proxies = {
            "http":"{}".format(self.changeProxy()),
            "https":"{}".format(self.changeProxy()),
        }
        try:
            resp = self.session.post(self.webCreateUrl, data=formData, allow_redirects=True)
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
            Error.warn(e)
            if self.errorReconect>self.errorMaxReconect:
                self.errorReconect = 0
                self.postCreateAccount()
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.postCreateAccount()
        else:
            Error.info(f"Status Code: {resp.status_code}".center(widthCenter,'.'))
            if resp.status_code==200:
                rjson = resp.json();
                if 'errors' in rjson:
                    errorType = rjson['error_type']
                    Error.e(1,f"Se encontraron errores al crear la cuenta de instagram, error type: {Fore.RED}{errorType}{Style.RESET_ALL}")
                    if errorType == 'generic_request_error':
                        self.checkGenericRequestError()
                    else:
                        for error in rjson['errors']:
                            Error.warn(f"Error en: [{error}]")
                            if error in ["error","ip"]:
                                for item in rjson['errors'][error]:
                                    Error.e(1,f"[{error}]: {item}")
                                    time.sleep(1)
                                if error=='ip':
                                    self.changeProxy()
                            else:
                                for item in rjson['errors'][error]:
                                    message = item['message']
                                    code = item['code']
                                    Error.e(1,f"[{Fore.RED}{code}{Style.RESET_ALL}]: {message}")
                                    if code == 'email_is_taken':
                                        self.emailIsTaken()
                                    if code == 'username_is_taken':
                                        Error.info("cambio el nombre de usuario".center(widthCenter,'-'))
                                        time.sleep(5)
                    self.postCreateAccount()
                else:
                    Error.ok("".center(widthCenter,'-'))
                    Error.ok("EXITO: Cuenta creada, Email:{} username:{} password: {}".format(self.email,self.username,self.password))
                    self.guardarcuentacreada();
                    Error.ok("".center(widthCenter,'-'))
            elif resp.status_code==429:
                self.waitrefresh()
                pass
            elif resp.status_code==400:
                Error.ok("".center(widthCenter,'-'))
                Error.ok("EXITO: Cuenta creada, Email:{} username:{} password: {}".format(self.email,self.username,self.password))
                self.guardarcuentacreada();
                Error.ok("".center(widthCenter,'-'))
                pass
            else:
                Error.warn(resp.text)
        return False
    def changeProxy(self):
        Error.executing("Cambiando proxy para esta Session",self.listerrorExecutinModulo)
        self.urlproxy = self.proxy.get()
        Error.info(f"Probando conexion del proxy: {self.urlproxy}")
        self.listerrorExecutinModulo = "INSTAGRAM"
        self.session.proxies = {
            "http":"{}".format(self.urlproxy),
            "https":"{}".format(self.urlproxy),
        }
        try:
            r = self.session.get("https://api.ipify.org/")
        except Exception as e:
            Error.e(1,"PROXY NO CONNECT")
            self.changeProxy();
            return False
        else:
            self.listerrorExecutinModulo = f"INSTAGRAM {Fore.RED}{r.text}{Style.RESET_ALL} "
            Error.executing(f"Ahora el proxy {self.urlproxy} esta en uso",self.listerrorExecutinModulo)
        return self.urlproxy;
    def waitrefresh(self):
        Error.executing(f"Muchas peticiones, Se detecto como DDOS",self.listerrorExecutinModulo)
        for i in tqdm(range(self.waitTimeRange)):
            time.sleep(0.2)
        if self.waitTimeRange >= 400:
            self.changeProxy()
        if self.waitTimeRange >= 800:
            self.waitTimeRange = 100
        self.waitTimeRange *= 2
        self.postCreateAccount()
    def checkGenericRequestError(self):
        self.session = requests.Session();
        Error.info("Intentando encontrar solucion a errores")
        formData2 = {
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'first_name': self.nombre,
            'opt_into_one_tap' : 'false'
        }
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)
        Error.executing("Accediendo al attempt",self.listerrorExecutinModulo)
        try:
            check = self.session.post(self.webCreateUrlAttempt, data=formData2, allow_redirects=True)
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
            Error.warn(e)
            if self.errorReconect>self.errorMaxReconect:
                self.errorReconect = 0
                self.changeProxy()
                self.checkGenericRequestError()
                return False
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.checkGenericRequestError()
                return False
        else:
            if check.status_code==200:
                Error.info(f"Estatus code: {check.status_code}".center(widthCenter,'.'))
                jsoncheck = check.json();
                new_username = jsoncheck["username_suggestions"]
                errorType = jsoncheck["error_type"]
                Error.e(1,f"Tipo de error: {Fore.RED}{errorType}{Style.RESET_ALL}")
                if errorType == 'form_validation_error':
                    if 'errors' in  jsoncheck:
                        jsoncheckerrors = jsoncheck['errors']
                        for err in jsoncheckerrors:
                            Error.e(1,f"Error en: [{err}]".center(widthCenter,'-'))
                            if err in ['email','username']:
                                for item in jsoncheckerrors[err]:
                                    m=item['message']
                                    c=item['code']
                                    Error.e(1,f"[{Fore.RED}{c}{Style.RESET_ALL}]: {m}")
                                    if c=='username_is_taken':
                                        self.username = random.choice(new_username)
                                        Error.executing(f"Actualizando username a: {self.username}",self.listerrorExecutinModulo)
                                        return True
                                    elif c=='email_is_taken':
                                        self.emailIsTaken()
                                        return True
                    self.postCreateAccount()
                else:
                    Error.e(1,"".center(widthCenter,'-'))
                    ppjson(jsoncheck)
                    Error.e(1,"".center(widthCenter,'-'))
                    return False
            elif check.status_code==429:
                Error.warn(f"Estatus code: {check.status_code}".center(widthCenter,'.'))
                self.waitrefresh()
                return False
            else:
                Error.warn(check.text);
                time.sleep(10)
        return False
    def createAccount(self,**kw):
        self.setVariablesCreate(**kw)
        self.initialConnect()
        self.postCreateAccount()
        Error.e(1,"FIN DE CODIGO")
        return True


##################### intento un nuevo metodo ############
    def crearcuenta(self,**kw):
        self.initialConnect()
        self.setVariablesCreate(**kw)
        formData = {
            'email':self.email,
            'password':self.password,
            'username':self.username,
            'first_name':self.nombre,
            'seamless_login_enabled' : '1',
            'tos_version' : 'row',
            'opt_into_one_tap' : 'false'
        }
        s = requests.Session()
        s.headers.update({
            "Accept-Language":self.AcceptLanguage,
            "Content-Type":"application/x-www-form-urlencoded",
            "X-CSRFToken":self.csrftoken,
            "X-IG-App-ID":"936619743392459",
            "X-IG-WWW-Claim":"0",
            "X-Instagram-AJAX":self.xInstagramAJAX,
            "X-Requested-With":"XMLHttpRequest",
            "Host": "www.instagram.com",
            "Origin": "https://www.instagram.com",
            "Referer":"https://www.instagram.com/",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
        })
        s.cookies.update({
            "csrftoken":self.csrftoken,
            "ig_did":self.deviceId,
        })
        s.proxies = {
            "http":"{}".format(self.urlproxy),
            "https":"{}".format(self.urlproxy),
        }
        ppjson(s.proxies)
        Error.executing(f"Creando cuenta...",self.listerrorExecutinModulo)
        try:
            resp = s.post(self.webCreateUrl, data=formData, allow_redirects=True)
        except Exception as e:
            Error.info("Intentando reconectar con instagram".center(50,'.'))
            self.crearcuenta(**kw)
        else:
            Error.info(f"Status Code: {resp.status_code}".center(widthCenter,'.'))
            if resp.status_code==200:
                rjson = resp.json();
                if 'errors' in rjson:
                    errorType = rjson['error_type']
                    Error.e(1,f"Se encontraron errores al crear la cuenta de instagram, error type: {Fore.RED}{errorType}{Style.RESET_ALL}")
                    for error in rjson['errors']:
                        Error.warn(f"Error en: [{error}]")
                        if error in ["error","ip"]:
                            for item in rjson['errors'][error]:
                                Error.e(1,f"[{error}]: {item}")
                        else:
                            for item in rjson['errors'][error]:
                                message = item['message']
                                code = item['code']
                                Error.e(1,f"[{Fore.RED}{code}{Style.RESET_ALL}]: {message}")
                else:
                    Error.ok("".center(widthCenter,'-'))
                    Error.ok("EXITO: Cuenta creada, Email:{} username:{} password: {}".format(self.email,self.username,self.password))
                    self.guardarcuentacreada();
                    Error.ok("".center(widthCenter,'-'))
            elif resp.status_code==429:
                Error.executing(f"Muchas peticiones, Se detecto como DDOS",self.listerrorExecutinModulo)
                pass
            elif resp.status_code==400:
                Error.ok("".center(widthCenter,'-'))
                Error.ok("EXITO: Cuenta creada, Email:{} username:{} password: {}".format(self.email,self.username,self.password))
                self.guardarcuentacreada();
                Error.ok("".center(widthCenter,'-'))
                pass
            else:
                Error.warn(resp.text)