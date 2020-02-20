import random
import time
import string
import hashlib
import sys
import os.path
import unidecode
import json
from pprintjson import pprintjson as ppjson


file="./nombres.xlsx"
file_json="./nombres.json"
# wb = xlrd.open_workbook(file)
# sheet = wb.sheet_by_index(0)
# nombres_unicos = []


Users=[]
number=10


with open(file_json, 'r') as json_file:
    nombres = json.loads(json_file.read());
    for nombre in range(number):
        select = random.sample(nombres, 2)
        randomNumber = random.randrange(10,99)
        randomLetters = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
        username = "_".join(select)+str(randomNumber)+randomLetters
        fname = select[0]
        lname = select[1]
        fullname = " ".join(select)
        password =  hashlib.md5(str(str(time.time())+username).encode('utf-8')).hexdigest()
        Users.append({
            "fname":fname,
            "lname":lname,
            "fullname":fullname,
            "username":username.lower(),
            "password":password,
            "country":"CO",
            "age":random.randrange(18,50)
        })
ppjson(Users)






# my_data_file = open(file_json)
# nombres = json.loads(my_data_file.read());
# Users = []
# select = random.sample(nombres, 2)
# randomNumber = random.randrange(10,99)
# randomLetters = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
# username = "_".join(select)+str(randomNumber)+randomLetters
# fname = select[0]
# lname = select[1]
# fullname = " ".join(select)
# password =  hashlib.md5(str(str(time.time())+username).encode('utf-8')).hexdigest()
#
#
# Users.append({
#     "fname":fname,
#     "lname":lname,
#     "fullname":fullname,
#     "username":username,
#     "password":password,
#     "country":"CO",
#     "age":random.randrange(18,50)
# })
#
# print(Users)

# with open('nombres.json', 'w') as json_file:
#     json.dump(mylist, json_file)

#
# for i in range(sheet.nrows):
#     nombre = sheet.cell_value(i, 0).strip().split()
#     for j in range(len(nombre)):
#         nombres_unicos.append(nombre[j])
#
