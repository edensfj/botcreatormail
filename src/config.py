import logging,sys

BASE_DIR = sys.path[0]
LIBS_DIR = "%s/libs/"%(BASE_DIR)
SOURCES_DIR = "%s/sources/"%(BASE_DIR)
LOGS_DIR = "%s/logs/"%(BASE_DIR)
Config = {
    "hushmail":{
        "loginEmail":"edens0hulk@hushmail.com", #vencida
        "loginPass":"",
    },
    "mysql":{
        "host":"puntoquimico.com.co",
        "user":"bot",
        "pass":"fabcaa97871555b68aa095335975e613",
        "db":"bot",
    }

}

Mensajes = {
    "trabajando":"Estamos trabajando para resolver esto lo mas pronto posible",
    "instagram":{
        "":"",
    }
}
