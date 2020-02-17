from colorama import Fore, Style
from time import sleep
from datetime import datetime
from src.config import *


timeSleep=0.1
def append_new_line(text_to_append):
    now = datetime.now()
    nombre = now.strftime("%d-%m-%Y.txt")
    fecha = now.strftime("%d/%m/%Y, %H:%M:%S")
    text_to_append = "{}  =>  {}".format(fecha,text_to_append)
    try:
        file_object = open("{}{}".format(LOGS_DIR,nombre), "a+")
    except Exception as e:
        raise e
    else:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)
        file_object.close()

class Error:
    def info(msg=''):
        sleep(timeSleep)
        mensaje = f'[ {Fore.BLUE}'u"\u0021"f'{Fore.RESET} ]\t{Fore.BLUE}{msg}{Style.RESET_ALL}'
        append_new_line(mensaje)
        return print(mensaje)
    def executing(msg='',modulo=''):
        sleep(timeSleep)
        if not modulo.strip():
            mensaje = "\t"u"\u2794"f"  {msg}"
        else:
            mensaje = f"[{modulo}]\t"u"\u2794"f"  {msg}"
        append_new_line(mensaje)
        return print(mensaje)
    def ok(msg=''):
        sleep(timeSleep)
        mensaje = f'[ {Fore.GREEN}'u"\u2714"f'{Fore.RESET} ]\t{Fore.GREEN}{msg}{Style.RESET_ALL}'
        append_new_line(mensaje)
        return print(mensaje)
    def warn(msg=''):
        sleep(timeSleep)
        m = msg[:100:]
        mensaje = f'[ {Fore.YELLOW}'u"\u26A0"f'{Fore.RESET} ]\t{Fore.YELLOW}{m}...{Style.RESET_ALL}'
        append_new_line(mensaje)
        return print(mensaje)
    def e(error=0,msg=''):

        sleep(timeSleep)
        """
        0 = advertencia
        1 = ERROR FATAL
        2 = ERROR FATAL
        3 = ERROR FATAL
        4 = ERROR: entrada vacia
        """
        errors = [
            'ADVERTENCIA!!',
            f'[{Fore.RED} 'u"\U00010102"f'{Fore.RESET} ]\t{Style.RESET_ALL}%s'%(msg),
            'ERROR: No se pudo completar la accion %s'%(msg),
        ]
        if error>=len(errors):
            error=0
        else:
            error = error
        mensaje = errors[error]
        append_new_line(mensaje)
        return print(mensaje)
