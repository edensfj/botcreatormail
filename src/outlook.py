import time, random, string, datetime, sys
import requests, shutil
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

class Outlook:
  url = 'https://signup.live.com/signup'
  prefixFiles = 'GetHIPData'
  driver = 'chromedriver'
  pathsources = '/home/fifi/tmp/botcreatoremail/sources/'
  def __init__(self,data=[],browser='Chrome',pathlib='/home/fifi/tmp/botcreatoremail/libs/'):
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
      self.browser.get(self.url)
      time.sleep(3)
      try:
        self.browser.find_element_by_id('MemberName').send_keys(i["email"])
        self.browser.find_element_by_id('iSignupAction').click()
      except Exception as e:
        print(e)
        continue
      time.sleep(3)
      try:
        self.browser.find_element_by_id('PasswordInput').send_keys(i["password"])
        self.browser.find_element_by_id('ShowHidePasswordCheckbox').click()
        self.browser.find_element_by_id('iSignupAction').click()
      except Exception as e:
        print(e)
        continue
      time.sleep(3)
      try:
        self.browser.find_element_by_id('FirstName').send_keys(i["firstName"])
        self.browser.find_element_by_id('LastName').send_keys(i["lastName"])
        self.browser.find_element_by_id('iSignupAction').click()
      except Exception as e:
        print(e)
        continue
      time.sleep(3)
      try:
        selectBD = Select(self.browser.find_element_by_id('BirthDay'))
        selectBD.select_by_value(str(random.randint(1,28)))

        selectBY = Select(self.browser.find_element_by_id('BirthYear'))
        selectBY.select_by_value(str(random.randint(1990,datetime.datetime.now().year-18)))

        selectBM = Select(self.browser.find_element_by_id('BirthMonth'));
        selectBM.select_by_value(str(random.randint(1,12)))
        self.browser.find_element_by_id('iSignupAction').click()
      except Exception as e:
        continue
      time.sleep(3)
      self.browser.execute_script(open('/home/fifi/tmp/botcreatoremail/src/jstest.js').read())
      time.sleep(1)
      self.resolvedImage()
      time.sleep(100)
  def resolvedImage(self):
    img = self.browser.find_element_by_xpath('//*[@alt="Visual Challenge"]')
    image_url = img.get_attribute('src')
    resp = requests.get(image_url, stream=True)
    local_file = open(self.pathsources+self.prefixFiles+'.jpeg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp