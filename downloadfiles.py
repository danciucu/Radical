from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from pynput.keyboard import Key, Controller
import selenium
import time
import shutil
import PyPDF2
import os
import globalvars, download_pictures, download_plans, download_reports



class previous_reports():
    def __init__(self):

        # import global variables
        globalvars.init()

        # simuate a chrome browser
        driver = selenium.webdriver.Chrome(ChromeDriverManager().install())
        # access BrM website
        driver.get('https://brm.kytc.ky.gov/BrM6/Login.aspx?ReturnUrl=%2fBrM6')
        # login into the website
        username_driver = driver.find_element(By.ID, "userid")
        username_driver.send_keys(globalvars.username)
        password_driver = driver.find_element(By.ID, "password")
        password_driver.send_keys(globalvars.password)
        login_driver = driver.find_element(By.ID, "btnSignIn")
        login_driver.click()
        # download inspection pictures
        if globalvars.cb1var == 1:
            download_pictures.main(driver)
        # download inspection plans
        if globalvars.cb2var == 1:
            download_plans.main(driver)
        # download inspection reports
        if globalvars.cb3var == 1:
            download_reports.main(driver)
        # download inspection reports
        if globalvars.cb4var == 1:
            self.download_prev_reports(driver)


    def download_prev_reports(self, driver):
        return