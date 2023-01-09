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
    # define 2 variables for the loop:
    pdf_count = 0
    name_count = 0
    pdf_name = ''
    pdf_rename = ''

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
            # get the file name
            pdf_name = str(driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/div/div[1]/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/div/fieldset/table/tbody/tr[1]/td[2]/div/fieldset/table/tbody/tr/td/div[1]/input['+ str(k + 1) +']').get_attribute('value'))
            pdf_name = pdf_name[14:]

            if pdf_name == '':
                continue

            else:
                # click on the button to download the file
                plans_driver = driver.find_element(By.NAME, 'ctl00$ctl00$m_cphContentPane$m_cphInspSubModules$ctl101$btnBridgePlan'+ str(k + 1))
                plans_driver.click()
                # scroll down
                scroll_driver = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(1)
                # check if the file downloaded exists
                while not os.path.exists('C:/Users/' + globalvars.user_path + '/Downloads/' + pdf_name + '.pdf'):
                    time.sleep(0.5)
                
                # assign a value to pdf_rename variable
                pdf_rename = pdf_name
                # check if the file already exists
                while True:
                    # set up conditions
                    condition0 = os.path.isfile(globalvars.folders[i]+ '/' + pdf_rename + '.pdf')
                    condition1 = os.path.isfile('C:/Users/' + globalvars.user_path + '/Downloads/' + pdf_rename + '.pdf')
                    # if the file exists in the Downloads or Bridge ID foldder, then increase the count
                    if condition0 or condition1 == True:
                        name_count += 1
                    # if it doesn't, then rename the file
                    else:                    
                        os.rename('C:/Users/' + globalvars.user_path + '/Downloads/' + pdf_name + '.pdf', 'C:/Users/' + globalvars.user_path + '/Downloads/' + pdf_rename + '.pdf')
                        globalvars.error_message = 'Warning: Duplicate Files Exists in Previous Reports Subfolder'
                        break
                    # redefine pdf_rename string variable in function of name_count variable
                    pdf_rename = ''
                    pdf_rename = pdf_name + ' (' + str(name_count) + ')'            

                # move the file to the assigned folder  
                shutil.move('C:/Users/' + globalvars.user_path + '/Downloads/' + pdf_rename + '.pdf', globalvars.folders[i])

                # reset name_count variable for the next file
                name_count = 0
            
        # scroll up 
        scroll_driver = driver.execute_script("window.scrollTo(0,-document.body.scrollHeight)")