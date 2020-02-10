import logging,sys

BASE_DIR = sys.path[0]
LIBS_DIR = "%s/libs/"%(BASE_DIR)
SOURCES_DIR = "%s/sources/"%(BASE_DIR)
SOURCES_DIR = "%s/logs/"%(BASE_DIR)
Config = {
    "hushmail":{
        "loginEmail":"edens0hulk@hushmail.com",
        "loginPass":"edens.123.321",
    },
    "mysql":{
        "host":"localhost",
        "user":"fifi",
        "pass":"12345",
        "db":"botalex",
    }

}

Mensajes = {
    "trabajando":"Estamos trabajando para resolver esto lo mas pronto posible",
    "instagram":{
        "":"",
    }
}
