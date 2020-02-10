import requests,time, sys, urllib,os,random
from pprintjson import pprintjson as ppjson
from bs4 import BeautifulSoup
from tqdm import tqdm
from prettytable import PrettyTable

from src.listaerrores import Error,Fore,Style
from src.new_sqlconnect import Sql
from src.config import Config as BotConfig
from src.new_randomproxy import RandomProxy
from src.new_tempmail import TempMail


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
        self.session.proxies = {
            "http":"{}".format(urlproxy),
            "https":"{}".format(urlproxy),
        }
        self.sql = Sql()
        self.tempmail = TempMail();
    def setVariablesCreate(self,**kw):
        for item in kw:
            if item in ['setAvailableEmail']:
                continue
            kw[item] = str(kw[item])
            setattr(self,item,kw[item])
        if self.email.isdigit():
            self.email = self.sql.getEmailById(self.email)
        check = self.sql.Select(["id"]).From(self.table).Where([(self.column,self.email)]).Run()
        if len(check)==0:
            self.table="alias"
            self.column="alias";
            self.createdby='1'
            check = self.sql.Select(["id"]).From(self.table).Where([(self.column,self.email)]).Run()
            if len(check)==0:
                return False
            else:
                self.idemail=check[0]['id']
        else:
            self.idemail=check[0]['id']
        self.idemail = str(self.idemail)
        self.usedby = self.idemail
    def initialConnect(self):
        Error.executing(f"Estableciendo conexion inicial",self.listerrorExecutinModulo)
        self.session.headers.update({
            "content-language":"es-la",
            "Accept-Language":"es-CO",
            "Content-Type":"application/x-www-form-urlencoded",
        })
        try:
            requests_start = self.session.get(self.webCreateUrlSharedData)
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
            Error.warn(e)
            if self.errorReconect>self.errorMaxReconect:
                self.errorReconect = 0
                self.changeProxy()
                self.initialConnect()
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.initialConnect()
        else:
            Error.executing(f"Actualizando Header",self.listerrorExecutinModulo)
            rjson=requests_start.json()
            self.csrftoken = rjson['config']['csrf_token']
            self.xInstagramAJAX = rjson['rollout_hash']
            self.AcceptLanguage = rjson['language_code']
            self.deviceId = rjson['device_id']
            self.public_key = rjson['encryption']['public_key']
            self.key_id = rjson['encryption']['key_id']
            self.session.headers.update({
                "Accept-Language":self.AcceptLanguage,
                "Content-Type":"application/x-www-form-urlencoded",
                "X-CSRFToken":self.csrftoken,
                "X-IG-App-ID":"936619743392459",
                "X-IG-WWW-Claim":"0",
                "X-Instagram-AJAX":self.xInstagramAJAX,
                "X-Requested-With":"XMLHttpRequest",
            })
            self.session.cookies.update({
                "csrftoken":self.csrftoken,
                "ig_did":self.deviceId,
            })
            return rjson
    def emailIsTaken(self):
        Error.executing(f"el correo {self.email} alparecer esta en uso.",self.listerrorExecutinModulo)
        r = self.sql.Select(["*"]).From(self.table).Where([("id",self.idemail)]).Limit("1").Run()[0]
        emailErrors = r["errors"]
        if emailErrors > self.errorMaxIntent:
            Error.executing(f"El {self.column}:[{self.email}] probado para la creacion, cuenta con [{emailErrors}] errores registrados, se procedera a omision",self.listerrorExecutinModulo)
            Error.executing(f"Actualizando estado del {self.column}, ID:{self.idemail} en la base de datos a 2",self.listerrorExecutinModulo)
            self.sql.Update(self.table,[("hasinstagram","2")]).Where([("id",self.idemail)])
            self.setNewEmail()
            self.postCreateAccount()
        else:
            Error.executing(f"Intentando crear cuenta nuevamente con: {self.email}",self.listerrorExecutinModulo)
            self.sql.Update(self.table,[("errors","{}".format(emailErrors+1))]).Where([("id",self.idemail)])
            self.postCreateAccount()
    def fixError(self,error):
        print(error)
    def setNewEmail(self):
        Error.executing(f"Creando email temporal",self.listerrorExecutinModulo)
        self.email = self.tempmail.getEmailLogin(True)
        self.sql.query("INSERT INTO emails(nombre,email,istemp) VALUES('{}','{}','{}')".format(self.nombre,self.email,'1'))
        self.sql.db.commit()
        self.idemail = self.sql.cursor.lastrowid
        self.usedby = self.idemail
        self.createdby='0'
        self.table="emails"
        self.column="email";
        Error.executing("Se actualizo el email y los datos",self.listerrorExecutinModulo)
        return self.email
    def setPretyTable(self,arr=[],show=True):
        self.p_table = PrettyTable(["ID","email/alias","Username","Nombre","table","column","createdby","usedby"])
        self.p_table.add_row(arr)
        if show:
            print(self.p_table)
    def postCreateAccount(self):
        self.setPretyTable([self.idemail,self.email,self.username,self.nombre,self.table,self.column,self.createdby,self.usedby])
        Error.info(f"Preparando {self.listerrorExecutinModulo} para creacion de cuentas")
        Error.executing(f"Generando FormData",self.listerrorExecutinModulo)
        self.password = "temp_password"
        self.enc_password = "#PWD_INSTAGRAM_BROWSER:6:1580446133845:AfVQAAeYuUWCpQWXu7bmSe96nvecx4D+4yretxrze80K5kIi9yybwuS7NdD08oTUIai5PWmwx98MJeV+Ec2PdK8GLtK6Wn01T6mooZnYKNg3mWOPaA671TpZFrUcjHT9yned3CTyj5WMF0sOI2wY0O4="
        formData = {
            'email': '{}'.format(self.email),
            'password': '{}'.format(self.password),
            'enc_password': '{}'.format(self.enc_password),
            'username': '{}'.format(self.username),
            'first_name': '{}'.format(urllib.parse.quote_plus(self.nombre)),
            'seamless_login_enabled' : '1',
            'tos_version' : 'row',
            'opt_into_one_tap' : 'false'
        }
        self.session.headers.update({
            "Accept-Language":self.AcceptLanguage,
            "Content-Type":"application/x-www-form-urlencoded",
            "X-CSRFToken":self.csrftoken,
            "X-IG-App-ID":"936619743392459",
            "X-IG-WWW-Claim":"0",
            "X-Instagram-AJAX":self.xInstagramAJAX,
            "X-Requested-With":"XMLHttpRequest",
        })
        self.session.cookies.update({
            "csrftoken":self.csrftoken,
            "ig_did":self.deviceId,
        })
        # ppjson(formData)
        Error.executing(f"Creando cuenta de instagram",self.listerrorExecutinModulo)
        try:
            requests_create = self.session.post(self.webCreateUrl, data=formData, allow_redirects=True)
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
            Error.warn(e)
            if self.errorReconect>self.errorMaxReconect:
                self.errorReconect = 0
                self.changeProxy()
                self.postCreateAccount()
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.postCreateAccount()
        else:
            if requests_create.status_code==200:
                Error.ok(f"Estatus code: {requests_create.status_code}".center(50,'.'))
                rjson = requests_create.json()
                ppjson(rjson)
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
                                    Error.executing(f"[{error}]: {item}",self.listerrorExecutinModulo)
                                    time.sleep(1)
                                if error=='ip':
                                    self.changeProxy()
                                    self.postCreateAccount()
                            else:
                                for item in rjson['errors'][error]:
                                    message = item['message']
                                    code = item['code']
                                    Error.executing(f"[{Fore.RED}{code}{Style.RESET_ALL}]: {message}",self.listerrorExecutinModulo)
                                    if code == 'email_is_taken':
                                        self.emailIsTaken()
                else:
                    print()
                    print("prosigo con la creacion de la cuenta")
                    Error.ok("EXITO: Cuenta creada, Email:{} username:{} password: {}".format(self.email,self.username,self.password))
                    print(rjson)
                    time.sleep(100)
                    sys.exit()
            else:
                Error.info(f"Estatus code: {requests_create.status_code}".center(50,'.'))
                ppjson(requests_create.json())
                if requests_create.status_code==429:
                    self.waitrefresh()
                    # ppjson(requests_create.json())
    def changeProxy(self):
        Error.executing("Cambiando proxy para esta Session",self.listerrorExecutinModulo)
        urlproxy = self.proxy.get()
        self.session.proxies = {
            "http":"{}".format(urlproxy),
            "https":"{}".format(urlproxy),
        }
        Error.executing(f"Ahora el proxy {urlproxy} esta en uso",self.listerrorExecutinModulo)
    def waitrefresh(self):
        Error.executing(f"Esperando tiempo de fresqueo, la conexion fue detectada por systemas anti DDOS",self.listerrorExecutinModulo)
        for i in tqdm(range(self.waitTimeRange)):
            time.sleep(0.2)
        if self.waitTimeRange >= 400:
            self.changeProxy()
        if self.waitTimeRange >= 800:
            self.waitTimeRange = 100
        self.waitTimeRange *= 2
        self.postCreateAccount()
    def checkGenericRequestError(self):
        Error.info("Intentando encontrar solucion a errores")
        formData2 = {
            'email': '{}'.format(self.email),
            'password': '{}'.format(self.password),
            'enc_password': '{}'.format(self.enc_password),
            'username': '{}'.format(self.username),
            'first_name': '{}'.format(urllib.parse.quote_plus(self.nombre)),
            'opt_into_one_tap' : 'false'
        }
        self.session.headers.update({
            "Accept-Language":self.AcceptLanguage,
            "Content-Type":"application/x-www-form-urlencoded",
            "X-CSRFToken":self.csrftoken,
            "X-IG-App-ID":"936619743392459",
            "X-IG-WWW-Claim":"0",
            "X-Instagram-AJAX":self.xInstagramAJAX,
            "X-Requested-With":"XMLHttpRequest",
        })
        self.session.cookies.update({
            "csrftoken":self.csrftoken,
            "ig_did":self.deviceId,
        })
        Error.executing("Accediendo al attempt",self.listerrorExecutinModulo)
        try:
            checkG = self.session.post(self.webCreateUrlAttempt, data=formData2, allow_redirects=True)
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {self.listerrorExecutinModulo}")
            Error.warn(e)
            if self.errorReconect>self.errorMaxReconect:
                self.errorReconect = 0
                self.changeProxy()
                self.checkGenericRequestError()
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.checkGenericRequestError()
        else:
            ppjson(checkG.json())
            if checkG.status_code==200:
                Error.ok(f"Estatus code: {checkG.status_code}".center(50,'.'))
            else:
                Error.info(f"Estatus code: {checkG.status_code}".center(50,'.'))
            if checkG.status_code==200:
                j=checkG.json()
                new_username = j["username_suggestions"]
                errorType = j["error_type"]
                Error.e(1,f"Tipo de error: {Fore.RED}{errorType}{Style.RESET_ALL}")
                if errorType == 'form_validation_error':
                    if 'errors' in j:
                        je=j['errors']
                        for err in je:
                            Error.warn(f"Error en: [{err}]")
                            if err=='email':
                                for item in je[err]:
                                    m=item['message']
                                    c=item['code']
                                    Error.executing(f"[{Fore.RED}{c}{Style.RESET_ALL}]: {m}",self.listerrorExecutinModulo)
                                    if c=='email_is_taken':
                                        Error.executing(f"Actualizando estado del {self.column} en la base de datos a 2",self.listerrorExecutinModulo)
                                        self.sql.Update(self.table,[("hasinstagram","2")]).Where([("id",self.idemail)])
                                        self.setNewEmail()
                            elif err=='username':
                                for item in je[err]:
                                    m=item['message']
                                    c=item['code']
                                    Error.executing(f"[{Fore.RED}{c}{Style.RESET_ALL}]: {m}",self.listerrorExecutinModulo)
                                    if c=='username_is_taken':
                                        self.username = random.choice(new_username)
                                        Error.executing(f"Actualizando username a: {self.username}",self.listerrorExecutinModulo)
                ppjson(j)
                time.sleep(2)
                self.postCreateAccount()
            elif checkG.status_code==429:
                self.waitrefresh()
            else:
                print(checkG.text)
    def createAccount(self,email='',nombre='',username='',password='',setAvailableEmail=False):
        self.setVariablesCreate(email=email,nombre=nombre,username=username,password=password,setAvailableEmail=setAvailableEmail)
        try:
            self.initialConnect()
        except Exception as e:
            Error.info(e)
        else:
            # ppjson(r)
            self.postCreateAccount()
            Error.e(1,"FIN DE CONDIGO")
