import settings
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import time
class EasyCrypto:
    def __init__(self) -> None:
        #options for the browser
        options = Options()
        # set the browser headless
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--headless")
        # get chrome web driver
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
        self.home_url='https://easycrypto.co.za'
        self.driver.get(self.home_url)

    def login(self)-> None:
        home_login_btn=self.driver.find_element_by_class_name('loginbtn')
        home_login_btn.click()
        email_field=self.driver.find_element_by_name('userName')
        email_field.send_keys(settings.setting.email)
        password_field=self.driver.find_element_by_name('password')
        password_field.send_keys(settings.setting.password)
        try:
            btn=self.driver.find_element_by_class_name('close')
            btn.send_keys(Keys.ENTER)
        except:
            pass
        login_btn=self.driver.find_element_by_class_name('login-btn')
        login_btn.send_keys(Keys.ENTER)
    def buy(self,amount):
        try:
            buy_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-user-home/div/div/nav/div/ul[2]/li[3]/ul/li[1]/a')))
            buy_btn.send_keys(Keys.ENTER)
        except:
            pass
        time.sleep(2)
        #get the 
        select=Select(self.driver.find_element_by_xpath('//*[@id="Token"]'))
        select.select_by_value("BTC")
        amount_field=self.driver.find_element_by_id('quantitytoBuy')
        self.driver.execute_script(f"document.getElementById('quantitytoBuy').setAttribute('value',{amount})")
        amount_field.send_keys(str(amount))
        buy_btn=self.driver.find_element_by_xpath('/html/body/app-root/app-user-home/div/div/div/main/app-buy-sell/section[1]/div[2]/form/div[4]/button')
        buy_btn.send_keys(Keys.ENTER)
        try:
            modal_btn=self.driver.find_element_by_xpath('/html/body/modal-container/div/div/div/div[2]/div[2]/button')
            ActionChains(self.driver).click(modal_btn).perform()
        except:
            pass
        try:
            continue_buying = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.text-uppercase:nth-child(2)')))
            continue_buying.click()
        except:
            pass
        self.driver.execute_script("document.getElementsByClassName('cursor-pointer')[0].click()")
    def sell(self,amount):
        try:
            buy_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-user-home/div/div/nav/div/ul[2]/li[3]/ul/li[2]/a')))
            buy_btn.send_keys(Keys.ENTER)
        except:
            pass
        time.sleep(2)
        select=Select(self.driver.find_element_by_xpath('//*[@id="sellToken"]'))
        select.select_by_value("EC10")
        amount_field=self.driver.find_element_by_id('QuantityTosell')
        amount_field.send_keys(str(amount))
        sell_btn=self.driver.find_element_by_xpath('/html/body/app-root/app-user-home/div/div/div/main/app-buy-sell/section[1]/div[2]/form/div[4]/button')
        sell_btn.send_keys(Keys.ENTER)
        try:
            modal_btn=self.driver.find_element_by_xpath('/html/body/modal-container/div/div/div/div[2]/div[2]/button')
            ActionChains(self.driver).click(modal_btn).perform()
        except:
            pass
        try:
            continue_buying = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.text-uppercase:nth-child(2)')))
            continue_buying.click()
        except:
            pass
        self.driver.execute_script("document.getElementsByClassName('cursor-pointer')[0].click()")

        