from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import shutil
import os
import globalvars

def main(driver):
    # click on KYTC tab
    time.sleep(10)
    kytc_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[3]/h3[3]')
    kytc_driver.click()
    # click on WEIGHTS tab
    time.sleep(5)
    weights_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[3]/div[3]/div/h3[4]')
    weights_driver.click()

    for i in range(len(globalvars.bridgeID)):
        # scroll up 
        scroll_driver = driver.execute_script("window.scrollTo(0,-document.body.scrollHeight)")
        # insert bridges IDs in the bridge box
        time.sleep(2)
        bridgebox_driver = driver.find_element(By.XPATH, '//*[@id="divflexbox_input"]')
        bridgebox_driver.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
        bridgebox_driver.send_keys(globalvars.bridgeID[i])
        time.sleep(5)
        bridgebox_driver.send_keys(Keys.ENTER)

        # download files
        for k in range(4):
            # scroll down
            scroll_driver = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            # click on the button to download the file
            plans_driver = driver.find_element(By.NAME, 'ctl00$ctl00$m_cphContentPane$m_cphInspSubModules$ctl101$btnBridgePlan'+ str(k + 1))
            plans_driver.click()
            # scroll down
            scroll_driver = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            # get the file name
            plans_name_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/div/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/div/fieldset/table/tbody/tr[1]/td[1]/div/fieldset/table/tbody/tr['+ str(k + 1) +']/td/table/tbody/tr/td[2]/input')
            #print('a = ', str(plans_name_driver.get_attribute('value')))

            if str(plans_name_driver.get_attribute('value')) == '':
                continue
                
            else:
                while not os.path.exists('C:/Users/' + globalvars.user_path + '/Downloads/' + str(plans_name_driver.get_attribute('value')) + '.pdf'):
                    time.sleep(0.5)
                    
                shutil.move('C:/Users/' + globalvars.user_path + '/Downloads/' + str(plans_name_driver.get_attribute('value')) + '.pdf', globalvars.folders[i])
            
        # scroll up 
        scroll_driver = driver.execute_script("window.scrollTo(0,-document.body.scrollHeight)")