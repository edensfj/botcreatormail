import requests, random, sys, re
from bs4 import BeautifulSoup
from src.listaerrores import Error,Fore,Style


class RandomProxy:
    proxys = []
    errorReconect = 0
    arp_listerrorExecutinModulo="S-RANDPROXY"
    url=''
    def __init__(self,url='https://www.sslproxies.org/'):
        Error.info(f"Restableciendo proxys")
        self.proxys = []
        self.url = url
        Error.executing(f"Generando lista de proxys desde {url}",self.arp_listerrorExecutinModulo)
        try:
            r = requests.get(url)
        except Exception as e:
            Error.e(1,f"No es posible hacer la conexion a {url}")
            Error.warn(e)
            if self.errorReconect>5:
                self.errorReconect = 0
                sys.exit()
            else:
                self.errorReconect += 1
                Error.info("Intentando reconectar".center(50,'.'))
                self.__init__(url)
        else:
            Error.executing(f"Parseando proxys",self.arp_listerrorExecutinModulo)
            sp = BeautifulSoup(r.text, 'html.parser')
            if url in ["https://www.sslproxies.org/","http://www.sslproxies.org/"]:
                self.sslproxies(sp)

    def kuaidaili(self,data=None):
        if data is not None:
            fl = data.find('div',{"id":"freelist"})
            print(fl)
    def sslproxies(self,data=None):
        if data is not None:
            table = data.find('table',{'id':'proxylisttable'})
            trs = table.findAll('tr')
            for tr in trs:
                ip = tr.findChildren()[0].text.strip()
                port = tr.findChildren()[1].text.strip()
                if [ip,port]==['IP Address','Port']:
                    continue
                elif not ip.strip():
                    continue
                elif not port.strip():
                    continue
                self.proxys.append('http://{}:{}'.format(ip,port))
    def get(self):
        select_proxy = random.choice(self.proxys)
        Error.executing(f"Proxy [{select_proxy}] seleccionado.",self.arp_listerrorExecutinModulo)
        return select_proxy
