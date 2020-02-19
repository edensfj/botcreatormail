import requests,random,time
from src.new_randomuser import RandomUser
from src.new_tempmail import TempMail
from src.new_sqlconnect import Sql
from pprintjson import pprintjson as ppjson
from src.listaerrores import Error,Fore,Style


webCreateUrlAttempt = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
webCreateUrl = "https://www.instagram.com/accounts/web_create_ajax/"
webCreateUrlSharedData = "https://www.instagram.com/data/shared_data/"
webLoginUrl = "https://www.instagram.com/accounts/login/ajax/"



resp1 = requests.get(webCreateUrlSharedData)
rjson=resp1.json()
csrftoken = rjson['config']['csrf_token']
xInstagramAJAX = rjson['rollout_hash']
AcceptLanguage = rjson['language_code']
deviceId = rjson['device_id']
public_key = rjson['encryption']['public_key']
key_id = rjson['encryption']['key_id']


proxystor =['socks5://127.0.0.1:9051','socks5://puntoquimico.com.co:9050']


s = requests.Session()

torproxy = random.choice(proxystor);

# s.proxies = {'http':'socks5://192.168.0.13:9051','https':'socks5://192.168.0.13:9051'}
s.proxies = {'http':'socks5://127.0.0.1:9051','https':'socks5://127.0.0.1:9051'}
# s.proxies = {'http':'socks5://104.237.137.138:9050','https':'socks5://104.237.137.138:9050'}
# s.proxies = {'http':torproxy,'https':torproxy}
ip = s.get("https://api.ipify.org/").text
s.headers.update({
"Accept-Language":AcceptLanguage,
"Content-Type":"application/x-www-form-urlencoded",
"X-CSRFToken":csrftoken,
"X-IG-App-ID":"936619743392459",
"X-IG-WWW-Claim":"0",
"X-Instagram-AJAX":xInstagramAJAX,
"X-Requested-With":"XMLHttpRequest",
"Host": "www.instagram.com",
"Origin": "https://www.instagram.com",
"Referer":"https://www.instagram.com/",
"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
})
s.cookies.update({
"csrftoken":csrftoken,
"ig_did":deviceId,
})

users = RandomUser()
for user in users.generate(1):
    tm_ = TempMail(user['username'])
    email = tm_.getEmailLogin();
    username = user['username']
    nombre = user['fullname']
    formData = {
    'email':email,
    'password':"temp_password",
    "enc_password":"#PWD_INSTAGRAM_BROWSER:6:1581326795652:AfVQAES3SDQpLiXhMquGh27QjTmdrCh+ZVdKlpRntC4W/xYAcKGenKfTDEU/HfIWGWBHtMeXl+figp3vK+KnJB0aAW5VijtZQogHwBrN5l52QLs5gAmn9WEGmtyROg9ZYplxDH2GF7rEkXaezCAOhqI=",
    'username':username,
    'first_name':nombre,
    'seamless_login_enabled' : '1',
    'tos_version' : 'row',
    'opt_into_one_tap' : 'false'
    }
    Error.executing(f"GRNERANDO CUENTA DE INSTAGRAM [{username}] ",ip)
    resp2 = s.post(webCreateUrl, data=formData, allow_redirects=True)
    jsonr = resp2.json()
    Error.info(jsonr);
    if 'checkpoint_url' in jsonr:
        Error.ok("EXITO: Cuenta creada, Email:{} username:{} password: {}".format(email,username,"temp_password"))
        sql = Sql()
        sql.query(f"INSERT INTO emails(nombre,email,hasinstagram,istemp) VALUES('{user['fullname']}','{email}','1','1')");
        sql.db.commit()
        idemail = sql.cursor.lastrowid;
        usedby = idemail;
        payload={
        "username":username,
        "password":"temp_password",
        "createdby":"0",
        "usedby":usedby,
        }
        sql.createInstagramAccont(**payload)
    ppjson(jsonr)
    timesleep = int(random.randrange(20))
    time.sleep(3)
