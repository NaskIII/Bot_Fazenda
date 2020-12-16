import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os
import shutil


class Main(object):
    def __init__(self, count):
        self.count = count
        self.lastCount = self.count
        self.dir_path = os.getcwd()
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=" + self.dir_path + r"\profile\fazenda")
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), chrome_options=options)

    def start(self):
        self.dir_path = os.getcwd()
        options = webdriver.ChromeOptions()
        options.add_argument(r"user-data-dir=" + self.dir_path + r"\profile\fazenda")
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), chrome_options=options)

    def site(self):
        self.driver.get('https://afazenda.r7.com/a-fazenda-12/votacao')
        self.driver.implicitly_wait(3)

    def votar(self):
        lipe = self.driver.find_element_by_xpath(
        '//*[@id="box_5f9b28d14b495515e3000035"]/div/div/div/div/section/div[2]/figure[1]/button')
        lipe.click()
        time.sleep(2)
        button = self.driver.find_element_by_class_name('voting-button')
        button.click()
        self.count += 1
        time.sleep(1)
        
    def votar_modal(self):
        time.sleep(2)
        button = self.driver.find_element_by_class_name('voting-button')
        button.click()
        self.driver.implicitly_wait(3)
        lipe = self.driver.find_element_by_xpath('//*[@id="758"]')
        lipe.click()
        button = self.driver.find_element_by_class_name('voting-button')
        button.click()
        self.count += 1
        self.driver.implicitly_wait(3)
        button = self.driver.find_element_by_class_name('voting-button')
        button.click()
    
    def check(self):
        if self.count == self.lastCount + 50:
            self.lastCount = self.count
            return True
        else:
            return False

    def delete(self):
        shutil.rmtree(self.dir_path + r"\profile\fazenda")

    def close(self):
        self.driver.close()

    def new_tab(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 
        self.driver.switch_to_window(self.driver.window_handles[0])
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
    
    def clear(self):
        self.driver.delete_all_cookies()
        print('Zerado: ')

if __name__ == "__main__":
    main = Main(0)

    main.site()
    main.votar()

    while True:
        if main.check() is True:
            main.clear()

        try:
            main.votar_modal()
            print('Votos: ', main.count, end="\r")
        except:
            main.new_tab()
            main.site()
            main.votar()
    