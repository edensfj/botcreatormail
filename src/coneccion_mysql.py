import MySQLdb,sys,time


class sql:
    def __init__ (self, host='127.0.0.1', user='fifi', password='12345', database='botalex'):
      create_emails = "CREATE TABLE IF NOT EXISTS emails (id int unsigned not null primary key auto_increment, nombre varchar(100) not null default '',email varchar(100) not null default '', password varchar(100) not null default '');"
      create_instragrams = "CREATE TABLE IF NOT EXISTS instagrams(id int unsigned not null primary key auto_increment,idemail int unsigned not null,username varchar(200) not null default '', password varchar(100) not null default '', FOREIGN KEY (idemail) references emails(id) on delete cascade);"
      create_trashemails = "CREATE TABLE IF NOT EXISTS trashemails(id int unsigned not null primary key auto_increment,nombre varchar(100) not null default '',email varchar(100) not null default '', password varchar(100) not null default '');"
      try:
        self.db = MySQLdb.connect(host, user, password, database)
      except Exception as e:
        print(e)
        try:
          try:
            db = MySQLdb.connect(host,user,password)
            cur = db.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS "+database)
            db = MySQLdb.connect(host,user,password,database)
            cur = db.cursor()
            cur.execute(create_emails)
            cur.execute(create_instragrams)
            cur.execute(create_trashemails)
            self.db = db
          except Exception as e3:
            sys.exit(e3)
        except Exception as e2:
          sys.exit(e2)
      self.cursor = self.db.cursor()
      self.cursor.execute(create_emails)
      self.cursor.execute(create_instragrams)
      self.cursor.execute(create_trashemails)

    def query(self,sql):
      self.cursor.execute(sql)
      return self.cursor
    def fetchall(self,sql):
      res = self.query(sql)
      return res.fetchall()

    def selectEmailById (self,id):
      self.cursor.execute("SELECT * FROM emails WHERE id='%s'",(int(id),))
      res = self.cursor
      return res.fetchone()
    def selectTrashEmailById (self,id):
      self.cursor.execute("SELECT * FROM trashemails WHERE id='%s'",(int(id),))
      res = self.cursor
      return res.fetchone()

    def checkPartialEmail(self,partialemail):
      self.cursor.execute("select id from emails where email like '%"+str(partialemail)+"%';")
      res = self.cursor
      if res.fetchone()==None:
        return False
      else:
        return True
    def checkEmail (self,email):
      self.cursor.execute("SELECT id FROM emails WHERE email=%s",(str(email),))
      res = self.cursor
      if res.fetchone()==None:
        return False
      else:
        return True
    def checkEmailById (self,idEmail):
      self.cursor.execute("SELECT id FROM emails WHERE id=%s",(str(idEmail),))
      res = self.cursor
      if res.fetchone()==None:
        return False
      else:
        return True
    def emailHasInstagram(self,idemail):
      self.cursor.execute("SELECT id FROM instagrams WHERE idemail=%s",(str(idemail),))
      res = self.cursor
      if res.fetchone()==None:
        return False
      else:
        return True
    def getNextEmailForInstagram(self):
      self.cursor.execute("SELECT id,nombre,email, CASE WHEN password = '' then md5(current_timestamp(6)) else password end as password from emails WHERE id > (SELECT IFNULL(MAX(idemail),0) FROM instagrams) LIMIT 1")
      res = self.cursor
      return res.fetchone()
    def checkNombre (self,nombre):
      self.cursor.execute("SELECT id FROM emails WHERE nombre=%s",(str(nombre),))
      res = self.cursor
      if res.fetchone()==None:
        return False
      else:
        return True
    def deleteEmail(self,id_email):
      self.cursor.execute("DELETE FROM emails WHERE id="+str(id_email))
      self.db.commit()
      return not self.checkEmailById(id_email)
    def insertEmail(self,val):
      self.cursor.execute("INSERT INTO emails (nombre,email,password) values (%s,%s,%s)", val)
      self.db.commit()
      estruct = {}
      lastid = self.cursor.lastrowid
      num = 0
      for i in self.fetchall("DESC emails"):
        estruct[i[0]] = self.selectEmailById(lastid)[num]
        num += 1
      return estruct
    def insertTrashEmail(self,val):
      self.cursor.execute("INSERT INTO trashemails (nombre,email,password) values (%s,%s,%s)", val)
      self.db.commit()
      estruct = {}
      lastid = self.cursor.lastrowid
      return lastid
    def fetchone(self,sql):
      res = self.query(sql)
      return res.fetchone()
    def lastEmail(self):
      res = self.query("SELECT * FROM emails ORDER BY id DESC LIMIT 1;")
      return res.fetchone()
    def fetch(self,sql):
      res = self.query(sql)
      return res.fetchone()

    def __del__(self):
      try:
        self.db.close()
      except Exception as e:
        sys.exit(e)
