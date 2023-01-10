from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller
import time
import shutil
import os
import PyPDF2
import globalvars

def main(driver):
    # set 2 variables for count and date
    count = 0
    date =""
    # define 4 variables for the loop:
    pdf_count = 0
    name_count = 0
    pdf_name = ''
    pdf_rename = ''
    # set up a variable to control keyboard
    keyboard = Controller()
    # click REPORTS tab
    time.sleep(5)
    reports_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[3]/h3[5]')
    reports_driver.click()
    # click GENERATE
    time.sleep(2)
    generate_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/div/div[3]/div[5]')
    generate_driver.click()
    # selection box variable
    report_box_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/div/fieldset/table/tbody/tr[1]/td[2]/select')
    report_box_driver.click()
    time.sleep(2)
    # select "Batch Current Standard Inspection Report"
    report_box_driver.send_keys(Keys.DOWN, Keys.ENTER)
    # select "Specific structure"
    time.sleep(5)
    select_key_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/div/fieldset/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td/input')
    select_key_driver.click()
        
    for i in range(len(globalvars.bridgeID)):
        # reset count, date and name_count
        count = 0
        date = ""
        name_count = 0
        # click on selection box
        time.sleep(2)
        # input bridges IDs in the bridge box
        bridgebox_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/div/fieldset/table/tbody/tr[3]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/table/tbody/tr/td[3]/div/input[2]')
        bridgebox_driver.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
        bridgebox_driver.send_keys(globalvars.bridgeID[i])
        time.sleep(5)
        bridgebox_driver.send_keys(Keys.ENTER)
        # select all tick boxes
        time.sleep(2)
        notestick_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/div/fieldset/table/tbody/tr[3]/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/span/input')
        notestick_driver.click()
        element_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/div/fieldset/table/tbody/tr[3]/td/table/tbody/tr[4]/td/table/tbody/tr/td[2]/span/input')
        element_driver.click()
        history_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/div/fieldset/table/tbody/tr[3]/td/table/tbody/tr[5]/td/table/tbody/tr/td[2]/span/input')
        history_driver.click()
        candidates_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/div[1]/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td/div/fieldset/table/tbody/tr[3]/td/table/tbody/tr[6]/td/table/tbody/tr/td[2]/span/input')
        candidates_driver.click()
        # click on "Generate Report" button
        generate_report_driver = driver.find_element(By.XPATH, '/html/body/form/div[3]/div/input')
        generate_report_driver.click()
        time.sleep(2)

        # download report
        for j in range(9):
            presstab_driver = ActionChains(driver).send_keys(Keys.TAB).perform()
            time.sleep(1) 
        pressenter_driver = ActionChains(driver).send_keys(Keys.ENTER).perform()

        # save the file
        time.sleep(2)
        keyboard.press(Key.enter)
        
        # check if the file was downloaded
        while not os.path.exists('C:/Users/' + globalvars.user_path + '/Downloads/ReportInFrame.pdf'):
            time.sleep(0.5)

        # find the date of the document
        pdf_file = PyPDF2.PdfFileReader('C:/Users/' + globalvars.user_path + '/Downloads/ReportInFrame.pdf')
        pdf_page1 = pdf_file.getPage(0)
        pdf_text = pdf_page1.extractText()

        for char in pdf_text:
            count += 1
            if char == "/":
                date = pdf_text[(count - 3):(count + 7)]
                break

        # change the date format
        date = date[6:] + "-" + date[:2] + "-" + date[3:5]

        pdf_name = str(globalvars.bridgeID[i]) + ' BrM Report_' +  date
        pdf_rename = pdf_name

        # check if the file already exists
        while True:
            # set up conditions
            condition0 = os.path.isfile(globalvars.folders[i]+ '/' + pdf_rename + '.pdf')
            condition1 = os.path.isfile('C:/Users/' + globalvars.user_path + '/Downloads/' + pdf_rename + '.pdf')
            # if the file exists in the Downloads or Bridge ID foldder, then increase the count
            if ((condition0 or condition1 == True) and name_count!= 0) or (condition0 == True and name_count == 0):
                name_count += 1
            # if it doesn't, then rename the file
            # Need to fix the naming problem - the default name is constant and the loop breaks before the renaming part gets through
            else:                    
                globalvars.error_message = 'Warning: Duplicate Files Exists in Previous Reports Subfolder'
                break
            # redefine pdf_rename string variable in function of name_count variable
            pdf_rename = ''
            pdf_rename = pdf_name + ' (' + str(name_count) + ')' 

        os.rename('C:/Users/' + globalvars.user_path + '/Downloads/ReportInFrame.pdf', 'C:/Users/' + globalvars.user_path + '/Downloads/' + pdf_rename + '.pdf')
        # move the file to the required folder
        shutil.move('C:/Users/' + globalvars.user_path + '/Downloads/' + pdf_rename + '.pdf', globalvars.folders[i])
        # refresh the page and go back to the previous page
        driver.refresh()
        time.sleep(5)
        presstab_driver = ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(1) 
        pressenter_driver = ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(30)