from src.config import Config,Mensajes
from src.listaerrores import Error
import MySQLdb,sys


class Sql:
    listerrorExecutinModulo = 'SQL'
    def __init__(self, host=Config["mysql"]["host"], user=Config["mysql"]["user"], password=Config["mysql"]["pass"], database=Config["mysql"]["db"]):
        Error.info(f"Creando Conexion a base de datos MYSQL [{host}]")
        try:
            self.db = MySQLdb.connect(host, user, password, database)
        except Exception as e:
            Error.e(1,e)
            Error.e(1,"Es necesaria una conexion a una base de datos para poder continuar")
            sys.exit()
        else:
            Error.executing(f"Conexion a MYSQL establecida como User:[{user}], DB:[{database}]",self.listerrorExecutinModulo)
            self.cursor = self.db.cursor()
            self.Update.Where.db = self
            self.Delete.db = self
            self.Select.db = self
    def query(self,sql):
        Error.executing("Ejecutando Query",self.listerrorExecutinModulo)
        self.cursor.execute(sql)
        return self.cursor
    def fetchAll(self,sql):
        res = self.query(sql)
        return res.fetchall()
    def fetchOne(self,sql):
        res = self.query(sql)
        return res.fetchone()
    def checkHasAlias(self,email):
        Error.executing(f"Verificando si {email} tiene Alias",self.listerrorExecutinModulo)
        self.cursor.execute(f"SELECT count(a.id) FROM alias a INNER JOIN emails e ON e.id=a.idemail WHERE (e.email='{str(email)}' OR e.id='{str(email)}')")
        if self.cursor.fetchone()[0]>0:
            return True
        else:
            return False
    def checkAliasEmail(self,alias,email):
        Error.executing(f"Verificando Alias: {alias} para Email: {email}",self.listerrorExecutinModulo)
        self.cursor.execute(f"SELECT a.id FROM alias a INNER JOIN emails e ON e.id=a.idemail WHERE a.alias like '%{str(alias)}%' AND (e.email='{str(email)}' OR e.id='{str(email)}')")
        idalias = self.cursor.fetchone()
        if idalias==None:
            return False
        else:
            return idalias[0]
    def getIdEmail(self, email=''):
        if not email.strip():
            Error.e(1,"No es posible buscar id a un email vacio")
            return False
        else:
            Error.executing(f"Buscando ID de {email}",self.listerrorExecutinModulo)
            self.cursor.execute(f"SELECT id FROM emails WHERE email='{str(email)}' ")
            resp = self.cursor.fetchone()
            if resp==None:
                return False
            else:
               return resp[0]
    def getEmailById(self, id='', isAlias=False):
        id = str(id)
        if not id.isdigit():
            Error.e(1,"No es posible buscar email Formato de ID no valido")
            return False
        else:
            if isAlias:
                Error.executing(f"Se seleccionó el modo [Alias]",self.listerrorExecutinModulo)
                Error.executing(f"Buscando Alias con ID:{id}",self.listerrorExecutinModulo)
                sqlquery = f"SELECT alias FROM alias WHERE id=5 AND hasinstagram=0;";
            else:
                Error.executing(f"Se seleccionó el modo [Email]",self.listerrorExecutinModulo)
                Error.executing(f"Buscando Email con ID:{id}",self.listerrorExecutinModulo)
                sqlquery = f"SELECT email FROM emails WHERE id={id} AND hasinstagram=0;";

            self.cursor.execute(sqlquery)
            resp = self.cursor.fetchone()
            if resp==None:
                Error.e(1,f"No se encontro el email con ID:{id}")
                return False
            else:
                Error.executing(f"{resp[0]} esta disponible",self.listerrorExecutinModulo)
                return resp[0]
    def insertAlias(self,alias='',idemail=1):
        Error.executing(f"Guardando alias {alias} en base de datos",self.listerrorExecutinModulo)
        if not str(idemail).isdigit():
            idemail = self.getIdEmail(idemail)
            if not idemail:
                Error.warn(f"No es posible insertar el alias {alias} en la base de datos, El ID del email es incorrecto")
                return False
        try:
            self.cursor.execute(f"INSERT INTO alias(alias,idemail) VALUES('{alias}','{idemail}')")
        except Exception as e:
            Error.e(1,f"No fue posible insertar alias [{alias}] a la base de datos")
            Error.warn(e)
            return False
        else:
            self.db.commit()
            Error.executing(f"[{alias}] se insertó correctamente",self.listerrorExecutinModulo)
            return self.cursor.lastrowid
    def lastEmailAliasAvailable(self,social='instagram'):
        Error.executing(f"Buscando un Email valido para {social}.",self.listerrorExecutinModulo)
        query1 = "SELECT id FROM emails "
        query2 = "SELECT id FROM alias "
        if social=='instagram':
            where = " WHERE hasinstagram='0' LIMIT 1"
            f = self.fetchOne(query1+where)
            if f is None:
                Error.warn(f"No se pudo encontrar un email valido para {social}")
                Error.executing(f"Buscando un Alias valido para {social}.",self.listerrorExecutinModulo)
                f2 = self.fetchOne(query2+where)
                if f2 is None:
                    Error.e(1,f"NO HAY EMAILs O ALIAS VALIDO PARA {social}")
                    return False
                else:
                    Error.info(f"Se encontro Alias valido para {social}")
                    return {"createdby":"1","usedby":f"{str(f2[0])}"}
            else:
                Error.info(f"Se encontro Email valido para {social}")
                return {"createdby":"0","usedby":f"{str(f[0])}"}
        elif social=='facebook':
            Error.info(Mensajes["trabajando"])
            return False
        else:
            Error.executing(f"No es posible determinar la red social {social}",self.listerrorExecutinModulo)
            return False
    def hasInstagram(self,email=None, alias=False):
        if email is None:
            return False
        email = str(email)
        sql = "SELECT id FROM "
        if alias:
            sql += f" alias WHERE alias='{email}' OR id='{email}'"
        else:
            sql += f" emails WHERE email='{email}' OR id='{email}'"

        result = self.fetchOne(sql)
        if result is None:
            return False
        else:
            return result[0]
    def updateEmail(self,email='',arr=[]):
        Error.executing("Configurando Email o Alias para actualizar",self.listerrorExecutinModulo)
        email = str(email)
        tabla = 'emails'
        if not email.isdigit():
            emailId = self.getIdEmail(email)
            if not emailId:
                Error.executing(f"Buscando ID de Alias: {email}",self.listerrorExecutinModulo)
                aliasId = self.fetchOne("SELECT id FROM alias WHERE alias='{}'".format(email))
                if aliasId is None:
                    Error.e(1,f"No es posible actualizar la tabla: {tabla}, el Email o Alias buscado no Existe")
                    return False
                else:
                    Error.info("Se ha encontrado alias con los parametros buscados, Cambiando a modo [Alias]")
                    tabla = 'alias'
                    email = aliasId[0]
            else:
                Error.info("Manteniendo el modo[Email]")
                email = emailId
        else:
            emailText = self.getEmailById(email)
            if not emailText:
                Error.e(1,f"No es posible actualizar la tabla: {tabla}, el Email o Alias buscado no Existe")
                return False


        self.Update(tabla,arr).Where([("id",email)])
    def createInstagramAccont(self,**columns):
        sql = "INSERT INTO instagram"
        sql += "("
        values = " VALUES ("
        i=1
        for column in columns:
            if i==len(columns):
                sql += "{})".format(str(column))
                values += "'{}')".format(str(columns[column]))
            else:
                sql += "{},".format(str(column))
                values += "'{}',".format(str(columns[column]))
            i += 1
        try:
            self.cursor.execute(sql+values)
        except Exception as e:
            Error.e(1,f"No fue posible insertar la cuenta de instagram en la base de datos")
            Error.warn(e)
            return False
        else:
            self.db.commit()
            Error.ok(f"Cuenta de instagram se agrego correctamente.")
            return self.cursor.lastrowid
    class Select:
        db=None
        def __init__(self,arr=[]):
            s = "SELECT "
            s += ",".join(arr)
            self.From._select = s
            self.From.db = self.db
        class From:
            db=None
            _where=''
            _from=''
            _select=''
            _group=''
            _inner=''
            _limit=''
            _order=''
            def __init__(self,table=''):
                self._from += " FROM {}".format(table)
                self.Inner._self = self
                self.Where._self = self
                self.Group._self = self
                self.Order._self = self
                self.Limit._self = self
                self.Run._self = self
            class Inner:
                _self=None
                def __init__(self,arr=[]):
                    for inners in arr:
                        self._self._inner += " INNER JOIN "
                        for inner in inners:
                            self._self._inner += "{} ON ".format(inner)
                            self._self._inner += "=".join(inners[inner])
                    self.Where._self = self._self
                    self.Order._self = self._self
                    self.Limit._self = self._self
                    self.Run._self = self._self
                class Limit:
                    _self=None
                    def __init__(self,limit=''):
                        self._self.Limit(limit)
                        self.Run._self = self._self
                    class Run:
                        _self=None
                        def __new__(self):
                            return self._self.Run()
                class Order:
                    _self=None
                    def __init__(self,arr=[],order="ASC"):
                        self._self.Order(arr,order)
                        self.Limit._self = self._selfl
                        self.Run._self = self._self
                    class Limit:
                        _self=None
                        def __init__(self,limit=''):
                            self._self.Limit(limit)
                            self.Run._self = self._self
                        class Run:
                            _self=None
                            def __new__(self):
                                return self._self.Run()
                    class Run:
                        _self=None
                        def __new__(self):
                            return self._self.Run()
                class Where:
                    _self=None
                    def __init__(self,arr=[],logical='AND',operador='='):
                        self._self.Where(arr,logical,operador)
                        self.Group._self = self._self
                        self.Order._self = self._self
                        self.Run._self = self._self
                        self.Limit._self = self._self
                    class Limit:
                        _self=None
                        def __init__(self,limit=''):
                            self._self.Limit(limit)
                            self.Run._self = self._self
                        class Run:
                            _self=None
                            def __new__(self):
                                return self._self.Run()
                    class Run:
                        _self=None
                        def __new__(self):
                            return self._self.Run()
                    class Group:
                        _self=None
                        def __init__(self,arr=[]):
                            self._self.Group(arr)
                            self.Order._self = self._self
                            self.Limit._self = self._self
                            self.Run._self = self._self
                        class Run:
                            _self=None
                            def __new__(self):
                                return self._self.Run()
                        class Limit:
                            _self=None
                            def __init__(self,limit=''):
                                self._self.Limit(limit)
                                self.Run._self = self._self
                            class Run:
                                _self=None
                                def __new__(self):
                                    return self._self.Run()
                        class Order:
                            _self=None
                            def __init__(self,arr=[],order="ASC"):
                                self._self.Order(arr,order)
                                self.Limit._self = self._self
                                self.Run._self = self._self
                            class Limit:
                                _self=None
                                def __init__(self,limit=''):
                                    self._self.Limit(limit)
                                    self.Run._self = self._self
                                class Run:
                                    _self=None
                                    def __new__(self):
                                        return self._self.Run()
                            class Run:
                                _self=None
                                def __new__(self):
                                    return self._self.Run()
                    class Order:
                        _self=None
                        def __init__(self,arr=[],order="ASC"):
                            self._self.Order(arr,order)
                            self.Limit._self = self._self
                            self.Run._self = self._self
                        class Limit:
                            _self=None
                            def __init__(self,limit=''):
                                self._self.Limit(limit)
                                self.Run._self = self._self
                            class Run:
                                _self=None
                                def __new__(self):
                                    return self._self.Run()
                        class Run:
                            _self=None
                            def __new__(self):
                                return self._self.Run()
                class Run:
                    _self=None
                    def __new__(self):
                        return self._self.Run()
            class Where:
                _self=None
                def __init__(self,arr=[],logical='AND',operador='='):
                    self._self._where += " WHERE "
                    i=1
                    for column,value in arr:
                        self._self._where += f'{column} {operador} "{value}"'
                        if i!=len(arr):
                            self._self._where += " {} ".format(logical)
                        i+=1
                    self.Group._self = self._self
                    self.Order._self = self._self
                    self.Inner._self = self._self
                    self.Limit._self = self._self
                    self.Run._self = self._self
                class Limit:
                    _self=None
                    def __init__(self,limit=''):
                        self._self.Limit(limit)
                        self.Run._self = self._self
                    class Run:
                        _self=None
                        def __new__(self):
                            return self._self.Run()
                class Run:
                    _self=None
                    def __new__(self):
                        return self._self.Run()
                class Inner:
                    _self=None
                    def __init__(self,arr=[]):
                        self._self.Inner(arr)
                        self.Run._self = self._self
                        self.Order._self = self._self
                        self.Limit._self = self._self
                    class Limit:
                        _self=None
                        def __init__(self,limit=''):
                            self._self.Limit(limit)
                            self.Run._self = self._self
                        class Run:
                            _self=None
                            def __new__(self):
                                return self._self.Run()
                    class Run:
                        _self=None
                        def __new__(self):
                            return self._self.Run()
                    class Order:
                        _self=None
                        def __init__(self,arr=[],order="ASC"):
                            self._self.Order(arr,order)
                            self.Run._self = self._self
                        class Run:
                            _self=None
                            def __new__(self):
                                return self._self.Run()
                class Order:
                    _self=None
                    def __init__(self,arr=[],order="ASC"):
                        self._self.Order(arr,order)
                        self.Run._self = self._self
                    class Run:
                        _self=None
                        def __new__(self):
                            return self._self.Run()
                class Group:
                    _self=None
                    def __init__(self,arr=[]):
                        self._self.Group(arr)
            class Group:
                _self=None
                def __init__(self,arr=[]):
                    self._self._group += " GROUP BY "
                    self._self._group += ",".join(arr)
                    self._self._group += " "
                    self.Run._self = self._self
                    self.Limit._self = self._self
                class Limit:
                    _self=None
                    def __init__(self,limit=''):
                        self._self.Limit(limit)
                        self.Run._self = self._self
                    class Run:
                        _self=None
                        def __new__(self):
                            return self._self.Run()
                class Run:
                    _self=None
                    def __new__(self):
                        return self._self.Run()
            class Order:
                _self=None
                def __init__(self,arr=[],order="ASC"):
                    self._self._order += " ORDER BY "
                    self._self._order += ",".join(arr)
                    self._self._order += " {} ".format(order.upper())
                    self.Run._self = self._self
                    self.Limit._self = self._self
                class Limit:
                    _self=None
                    def __init__(self,limit=''):
                        self._self.Limit(limit)
                        self.Run._self = self._self
                    class Run:
                        _self=None
                        def __new__(self):
                            return self._self.Run()
                class Run:
                    _self=None
                    def __new__(self):
                        return self._self.Run()
            class Limit:
                _self=None
                def __init__(self,limit=''):
                    self._self._limit += " LIMIT {};".format(limit)
                    self.Run._self = self._self
                class Run:
                    _self=None
                    def __new__(self):
                        return self._self.Run()
            class Run:
                _self=None
                def __new__(self):
                    qr = f'{self._self._select}{self._self._from}{self._self._inner}{self._self._where}{self._self._order}{self._self._group}{self._self._limit}'
                    Error.executing(qr,self._self.db.listerrorExecutinModulo)
                    try:
                        resp = list(self._self.db.fetchAll(qr))
                    except Exception as e:
                        Error.e(1,"ERROR AL EJECUTAR QUERY")
                        Error.warn(e)
                        return [];
                    else:
                        resp_new = []
                        field_name = [field[0] for field in self._self.db.cursor.description]
                        for row in resp:
                            row_new = zip(field_name,row)
                            resp_new.append(dict(row_new))
                        return resp_new;
    class Delete:
        db=None
        def __init__(self,table=None):
            if self.db==None:
                Error.e(1,"ERROR FATAL: No db select")
            else:
                if table==None:
                    Error.e(1,"ERROR FATAL: No table select")
                else:
                    self.Where.db = self.db
                    self.Where.delete = "DELETE FROM {} WHERE ".format(table)
        class Where:
            delete=None
            db=None
            def __init__(self,arr=[],logical="AND",operador='='):
                if self.delete==None:
                    Error.e(1,"No es posible ejecutar la query")
                else:
                    Error.executing("Parseando Array en WHERE",Sql.listerrorExecutinModulo)
                    w='';i=1;
                    for column,value in arr:
                        w+=f'{column}{operador}{value}'
                        if i!=len(arr):
                            w += logical
                        i += 1
                    self.delete += w
                    self.db.query(self.delete)
                    self.db.db.commit()
                    numwrro = self.db.cursor.rowcount
                    Error.warn(f"{numwrro} record(s) deleted")
    class Update:
        def __init__(self,table,arr=[]):
            Error.executing("Parseando Array en SET",Sql.listerrorExecutinModulo)
            f='';i=1
            for column,value in arr:
                f+=f"UPDATE {table} SET {column}='{value}'"
                if i!=len(arr):
                    f += ', '
                i += 1
                self.Where.update = f
        class Where:
            update=None
            db=None
            def __init__(self,arr=[],logical='AND',operador='='):
                if self.update==None:
                    Error.e(1,"No es psible actualizar base de datos")
                else:
                    Error.executing("Parseando Array en WHERE",Sql.listerrorExecutinModulo)
                    w=' WHERE ';i=1;
                    for column,value in arr:
                        w+=f'{column}{operador}{str(value)}'
                        if i!=len(arr):
                            w += logical
                        i += 1
                    self.update += w
                    self.db.query(self.update)
                    self.db.db.commit()
                    numwrro = self.db.cursor.rowcount
                    if numwrro>1:
                        Error.info(f"Se actualizaron {numwrro} tablas")
                    elif numwrro==1:
                        Error.info(f"Se actualizo {numwrro} tabla")
                    else:
                        Error.warn("No se actualizo la base de datos")
#     def __del__(self):
# #        Error.executing("Cerrando conexion",self.listerrorExecutinModulo)
#         try:
#             self.db.close()
#         except Exception as e:
#             Error.e(1,e)
#         else:
#             print("Conexion DB cerrada")
# #            Error.ok("Conexion DB cerrada")
