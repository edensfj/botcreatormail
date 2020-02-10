import requests
import sys
import time
from src.listaerrores import Error,Fore,Style
from src.new_sqlconnect import Sql
from pprintjson import pprintjson as ppjson
from bs4 import BeautifulSoup
#


"""
cesantias. { pedir carta para }




##### HEADERS ######
    Host: secure.hushmail.com
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0
    Accept: application/json, text/javascript, */*; q=0.01
    Accept-Language: es-CO
    Accept-Encoding: gzip, deflate, br
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    X-Hush-Ajax-Start-Time: 1579745278757
    X-Requested-With: XMLHttpRequest
    Content-Length: 218
    Origin: https://secure.hushmail.com
    DNT: 1
    Connection: keep-alive
    Referer: https://secure.hushmail.com/validate/?hush_username=edens0hulk@hushmail.com
    Cookie: PHPSESSID2=AEAE686A234CE4AFFB519E9F5AC26D06; PHPSESSID=22911557F4F5D756C37697CC08C70C8D

##### COOOKIES   ######

    "PHPSESSID":"22911557F4F5D756C37697CC08C70C8D",
    "PHPSESSID2":"AEAE686A234CE4AFFB519E9F5AC26D06"




##### VERIFICACION DE CODIGO POR SMS #####

    "form_token":"e1ceed8e70107ef3ee6adb69e3d2cd39_686f5e71bb55",
    "__hushform_extra_fields":"",
    "hush_username":"edens0hulk@hushmail.com",
    "hush_country_code":"CO",
    "hush_sms_phone":"3125625372",
    "hush_sms_code":"904000",
    "processAjax":"verificationform"


##### ESTRUCTURA PARA CREAR ALIAS ######
(  https://secure.hushmail.com/1.1.6/preview/hushmail/edens0hulk@hushmail.com/preferences?format=json   )

    "form_token":"e1ceed8e70107ef3ee6adb69e3d2cd39_354fc431d6d3",
    "__hushform_extra_fields":"",
    "alias":"aliasdeprueba",
    "current_alias":"",
    "save":"Save",
    "processAjax":"editPseudonymsForm"
    ##### RESPONSE #####
        "params":{
            "changedPseudonymSelectors":[
                "element-in-place-container-c67b3bee362a8c4d2b068a132313a2ea"
            ]
         },
         "formValidation":true


##### ESTRUCTURA PARA LOGIN ######

    "form_token":"e1ceed8e70107ef3ee6adb69e3d2cd39_546b90918696",
    "__hushform_extra_fields":"",
    "next_webapp_page":"",
    "hush_domain":"hushmail.com",
    "hush_username":"edens0hulk@hushmail.com",
    "hush_passphrase":"edens.123.321",
    "hush_remember_me":"",
    "hush_authcode":"",
    "hush_authenticated":"",
    "hush_customerid":"0000000000000000",
    "processAjax":"authenticationform",
    "formPage":"loginpage"



"""




class Hushmail:
    listerrorExecutinModulo = 'HUSHMAIL'
    logged = False
    session = False
    errorReconect = 0
    aliasExtencion = ''
    loginUrlGet = 'https://secure.hushmail.com/preview/hushmail/'
    loginUrlPost = 'https://secure.hushmail.com/1.1.6/preview/hushmail/authentication/?format=json'
    loginUrlAlias = 'https://secure.hushmail.com/1.1.6/preview/hushmail/edens0hulk@hushmail.com/preferences/aliases?format=json'
    urlCreateAlias ='https://secure.hushmail.com/1.1.6/preview/hushmail/edens0hulk@hushmail.com/preferences?format=json'
    def __init__(self,email='',password=''):
        Error.info("Configurando Hushmail para su uso")
        if not email.strip():
            Error.e(1,"No se pudo configurar una cuenta de correo")
            Error.warn("Saliendo del script")
            sys.exit("Saliendo del script")
        if not password.strip():
            Error.e(1,"No se pudo configurar una clave de paso")
            Error.warn("Saliendo del script")
        self.email = email
        self.password = password
    def login(self):
        Error.info(f"Iniciando session en Hushmail como [{self.email}]")
        self.session = requests.Session()
        try:
            session_start = self.session.get(self.loginUrlGet)
        except Exception as e:
            Error.e(1,"No es posible hacer la conexion a Hushmail")
            Error.warn(e)
            if self.errorReconect>5:
                self.errorReconect = 0
                Error.e(1,"SALIENDO DEL SCRIPT".center(50,'.'))
                sys.exit()
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.login()
        else:
            Error.executing("Recopilando Headers & Cookies",self.listerrorExecutinModulo)
            soup = BeautifulSoup(session_start.text, 'html.parser')
            Error.executing("Parseando resultado",self.listerrorExecutinModulo)
            form_token = soup.find('input',{'name':'form_token'})['value']
            Error.executing("Obteniendo form_token para el login",self.listerrorExecutinModulo)
            Error.executing("Aplicando nuevos Headers",self.listerrorExecutinModulo)
            self.session.headers.update({
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "DNT":"1",
                "Host":"secure.hushmail.com",
                "Origin":"https://secure.hushmail.com",
                # "Referer":"https://secure.hushmail.com/preview/hushmail/",
                "Referer":self.loginUrlGet,
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "X-Hush-Ajax-Start-Time":str(int(time.time()*1000)),
                "X-Requested-With":"XMLHttpRequest"
            })
            Error.executing("Construyendo url-encode para el formulario",self.listerrorExecutinModulo)
            dataPost = {
                "form_token":form_token,
                # "form_token":"e1ceed8e70107ef3ee6adb69e3d2cd39_546b90918696",
                "__hushform_extra_fields":"",
                "next_webapp_page":"",
                "hush_domain":"hushmail.com",
                "hush_username":self.email,
                # "hush_username":"edens0hulk@hushmail.com",
                "hush_passphrase":self.password,
                # "hush_passphrase":"edens.123.321",
                "hush_remember_me":"",
                "hush_authcode":"",
                "hush_authenticated":"",
                "hush_customerid":"0000000000000000",
                "processAjax":"authenticationform",
                "formPage":"loginpage",
            }
            try:
                create_request = self.session.post(self.loginUrlPost, data=dataPost, allow_redirects=True)
            except Exception as e:
                Error.e(1,"No es posible hacer la conexion a Hushmail")
                if self.errorReconect>5:
                    self.errorReconect = 0
                    Error.e(1,"SALIENDO DEL SCRIPT".center(50,'.'))
                    sys.exit()
                else:
                    self.errorReconect += 1
                    Error.info("Intentando reconectar".center(50,'.'))
                    self.login()
            else:
                response = create_request.json()
                if response['formValidation']:
                    Error.ok(f"{self.email} Ha iniciado session correctamente")
                else:
                    Error.e(1,f"No fue posible crear la session como [{self.email}]")
                    ppjson(response)
    def createAlias(self,form_token='',alias='',savealias=False):
        Error.info(f"Iniciando creacion de alias...")
        if not alias.strip():
            Error.warn(f"No es posible crear el alias '{alias}'")
        else:
            Error.executing("Accediendo a alias de hushmail",self.listerrorExecutinModulo)
            try:
                requestsAlias = self.session.get(self.loginUrlAlias)
            except Exception as e:
                Error.e(1,"No es posible hacer la conexion a Hushmail")
                Error.warn(e)
                if self.errorReconect>5:
                    self.errorReconect = 0
                    return False
                else:
                    self.errorReconect += 1
                    Error.info("Intentando reconectar".center(50,'.'))
                    self.createAlias(form_token=form_token,alias=alias)
            else:
                Error.executing("Verificando form_token",self.listerrorExecutinModulo)
                if not form_token.strip():
                    htmlAlias = BeautifulSoup(requestsAlias.json()['content'][0]['elements'][0]['html'], 'html.parser')
                    formAlias = htmlAlias.find("form", {"name":"editPseudonymsForm_new"})
                    self.aliasExtencion = formAlias.find("span", {"class":"secondary"}).text
                    AliasToken = formAlias.find("input",{"name":"form_token"})['value']
                else:
                    AliasToken = form_token
                form_token = AliasToken
                self.session.headers.update({
                    "Connection":"keep-alive",
                    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Hush-Ajax-Start-Time":f"{int(time.time()*1000)}",
                    "X-Hush-Generated-Password-Method":"Store",
                    "X-Requested-With":"XMLHttpRequest",
                })
                formDataAlias = {
                    "form_token":form_token,
                    "__hushform_extra_fields":"",
                    "alias":str(alias),
                    "current_alias":"",
                    "save":"Save",
                    "processAjax":"editPseudonymsForm"
                }
                Error.executing(f"Creando Alias {alias}",self.listerrorExecutinModulo)
                try:
                    requestsCreateAlias = self.session.post(self.urlCreateAlias, data=formDataAlias, allow_redirects=True)
                except Exception as e:
                    Error.e(1,"No es posible hacer la conexion a Hushmail")
                    Error.warn(e)
                    Error.info("Intentando reconectar".center(50,'.'))
                    if self.errorReconect>5:
                        self.errorReconect = 0
                        return False
                    else:
                        self.errorReconect += 1
                        Error.info("Intentando reconectar".center(50,'.'))
                        self.createAlias(form_token=form_token,alias=alias)
                else:
                    responseCreateAlias = requestsCreateAlias.json()
                    if responseCreateAlias['formValidation']:
                        if savealias:
                            sql = Sql()
                            idalias = ql.insertAlias(f"{alias}{self.aliasExtencion}",self.email)
                            if not idalias:
                                return False
                            else:
                                return idalias
                        return True
                    else:
                        return False







     #
