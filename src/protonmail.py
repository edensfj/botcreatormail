import time, random, string, datetime, sys
import requests, shutil
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from src.coneccion_mysql import sql
class Protonmail:
  url = 'https://mail.protonmail.com/create/new?language=en'
  prefixFiles = 'GetHIPData'
  driver = 'chromedriver'
  pathsources = '/home/fifi/tmp/botcreatoremail/sources/'
  def __init__(self,data=[],browser='Chrome',pathlib='/home/fifi/tmp/botcreatoremail/libs/'):
    self.db = sql()
    if browser == 'Firefox':
      self.driver = 'geckodriver'
      self.browser = webdriver.Firefox(executable_path=pathlib+self.driver)
    elif browser == 'Chrome':
      self.browser = webdriver.Chrome(pathlib+self.driver)
    self.execute(data)
  def execute(self,data=[]):
    for i in data:
      if "¿" in i["email"]:
        continue
      if self.db.checkEmail(i["email"]):
        print("El email: ",i["email"]," Exite. saltando")
        continue
      username = i["email"].split('@')[0]
      print(i["email"], i["password"])
      self.browser.get(self.url)
      time.sleep(5)
      try:
        iframe = self.browser.find_element_by_xpath('//*[@class="top"]')
        self.browser.switch_to.frame(iframe)
        self.browser.find_element_by_id('username').send_keys(username)
        self.browser.switch_to.default_content()
        # iframe username
        self.browser.find_element_by_id('password').send_keys(i["password"])
        self.browser.find_element_by_id('passwordc').send_keys(i["password"])
        # iframe click
        self.browser.find_element_by_tag_name('html').send_keys(Keys.END)
        iframe = self.browser.find_element_by_xpath('//*[@class="bottom"]')
        self.browser.switch_to.frame(iframe)
        time.sleep(1)
        btn2 = self.browser.find_element_by_tag_name('button')
        btn2.click()
        self.browser.switch_to.default_content()
        self.browser.find_element_by_tag_name('html').send_keys(Keys.HOME)
      except Exception as e:
        print(e)
        continue
      time.sleep(1)
      try:
        modalFooter = self.browser.find_element_by_class_name('modal-footer')
        btn = modalFooter.find_element_by_id('confirmModalBtn')
        btn.click()
      except Exception as e:
        print(e)
        continue 
      time.sleep(1)
      self.browser.execute_script("alert('tienes 40 segundos para resolver el captcha')")
      self.db.insertEmail((i["nombre"],i["email"],i["password"]))
      time.sleep(40)
      
      # time.sleep(5)
      # try:
      #   self.browser.find_element_by_id("id-signup-radio-email").click()
      #   self.browser.find_element_by_id("emailVerification").send_keys("edens0hulk@hotmail.com")
      # except Exception as e:
      #   print(e)
      #   continue 
      # aqui reviso el correo y el mensaje de protonmail
      #   veo el codigo: 463412
      # ingreso el codigo   codeValue       id
      
      # pre finish
      # verification-panel   id
      verificationPanel = self.browser.find_element_by_id('verification-panel')
      btn = verificationPanel.find_element_by_class_name("humanVerification-completeSetup-create")
      print(btn)
      print(btn.text)
      btn.click()
      time.sleep(30)
      
      
      
      #finish  
      # primer nombre segundo nombre     displayName    id
      self.browser.find_element_by_id('displayName').send_keys(i["firstName"]+' '+i["lastName"])
      modalFooter = self.browser.find_element_by_class_name('modal-footer')
      btn = modalFooter.find_element_by_id('confirmModalBtn')
      btn.click()
      
      
      time.sleep(60)
    self.browser.quit()