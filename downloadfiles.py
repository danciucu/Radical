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
import globalvars



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
            self.download_pictures(driver)
        # download inspection plans
        if globalvars.cb2var == 1:
            self.download_plans(driver)
        # download inspection reports
        if globalvars.cb3var == 1:
            self.download_reports(driver)
        # download inspection reports
        if globalvars.cb4var == 1:
            self.download_prev_reports(driver)


    def wait_display(self, driver, time, id_var):
        try:
            element = WebDriverWait(driver, time).until(
                EC.presence_of_element_located((By.ID, id_var))
            )
        except:
            driver.quit()


    def download_pictures(self, driver):
        # define 3 variables for loops
        folder_count = 0
        xpath_count = ''
        download_count = 0
        pdf_count = 0

        for i in range(len(globalvars.bridgeID)):
            # reset count, download_count, pdf_count
            folder_count = 0
            download_count = 0
            pdf_count = 0

            # only for the first element
            if i == 0:
                # click on INSPECTION tab
                time.sleep(10)
                inspection_driver = driver.find_element(By.XPATH, '//*[@id="ctl00_m_cphLeftPane_m_ucTaskBar_m_TaskBarMenu_divMenuItems"]/div[3]/h3[2]')
                inspection_driver.click()
                # click on MULTIMEDIA subtab
                time.sleep(2)
                multimedia_driver = driver.find_element(By.XPATH, '//*[@id="ctl00_m_cphLeftPane_m_ucTaskBar_m_TaskBarMenu_divMenuItems"]/div[3]/div[2]/div/h3[6]')
                multimedia_driver.click()

            
            # search bridges IDs by the box from multimedia
            time.sleep(2)
            bridgebox_driver = driver.find_element(By.XPATH, '//*[@id="divflexbox_input"]')
            bridgebox_driver.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
            bridgebox_driver.send_keys(globalvars.bridgeID[i])
            time.sleep(5)
            bridgebox_driver.send_keys(Keys.ENTER)

            # loop over all directories to find the correct Inspection file
            while True:
                # dynamically change xpath based on folder number and click on it
                time.sleep(2)
                xpath_count = '//*[@id="multimediaManagerForm"]/div[2]/div[1]/ul/li['+str(folder_count + 2 )+']/a'
                prev_inspection_driver = driver.find_element(By.XPATH, xpath_count)
                prev_inspection_driver.click()
                time.sleep(5)
                # if folder is empty then go back and restart loop
                if ('No records to display' in driver.page_source):
                    multimedia_return_driver = driver.find_element(By.XPATH, '//*[@id="multimediaManagerForm"]/div[1]/div[1]/nav/ol/li[1]')
                    multimedia_return_driver.click()
                    folder_count += 1
                    continue
                
                time.sleep(5)

                # loop over all files to check if the file is a pdf document
                ## NEED TO SCROLL DOWN TO FIND THE PDF FILE SINCE MIGHT BE AT THE BOTTOM OF THE PAGE
                while True:
                    text_file_inspection_driver = driver.find_element(By.XPATH, '//*[@id="multimediaManagerForm"]/div[2]/div/div[2]/div[1]/table/tbody/tr['+ str(pdf_count + 1) +']/td[1]')
                    # if it's a pdf file, then download the new file
                    if ".pdf" in text_file_inspection_driver.text:
                        down_inspection_driver = driver.find_element(By.XPATH, '//*[@id="multimediaManagerForm"]/div[2]/div/div[2]/div[1]/table/tbody/tr['+ str(pdf_count + 1) +']/td[7]/i[3]')
                        down_inspection_driver.click()
                        break
                    # if not, move on to the next element and scroll
                    else:
                        pdf_count += 1
                        if pdf_count == 5:
                            scroll_driver = driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

                # check if the file downloaded exists
                while not os.path.exists('C:/Users/' + globalvars.user_path + '/Downloads/' + str(text_file_inspection_driver.text)):
                    time.sleep(0.5)
                
                # move the file to the assigned folder
                shutil.move('C:/Users/' + globalvars.user_path + '/Downloads/' + str(text_file_inspection_driver.text), globalvars.folders[i])
                # check if downloaded file contains the word Inspection
                pdf_file = PyPDF2.PdfFileReader(globalvars.folders[i] + "/" + str(text_file_inspection_driver.text))
                pdf_page1 = pdf_file.getPage(0)
                pdf_text = pdf_page1.extractText()

                # check if the document has more than one page - if it doesn't, delete it
                if pdf_file.numPages == 1:
                    os.remove(globalvars.folders[i] + "/" + str(text_file_inspection_driver.text))
                    multimedia_return_driver = driver.find_element(By.XPATH, '//*[@id="multimediaManagerForm"]/div[1]/div[1]/nav/ol/li[1]')
                    multimedia_return_driver.click()
                
                # if it has more than a page is an inspection
                else:
                    download_count += 1
                    # go back to the folder menu
                    scroll_driver = driver.execute_script("window.scrollTo(0,-document.body.scrollHeight)")
                    multimedia_return_driver = driver.find_element(By.XPATH, '//*[@id="multimediaManagerForm"]/div[1]/div[1]/nav/ol/li[1]')
                    multimedia_return_driver.click()
                    if download_count == 2:
                        break                    
                
                folder_count += 1


    def download_plans(self, driver):
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


    def download_reports(self, driver):
        # set two variables for count and date
        count = 0
        date =""
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
            # reset count and date
            count = 0
            date = ""
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
            # rename the file
            os.rename('C:/Users/' + globalvars.user_path + '/Downloads/ReportInFrame.pdf', 'C:/Users/' + globalvars.user_path + '/Downloads/' + str(globalvars.bridgeID[i]) + ' BrM Report_' +  date + '.pdf')
            # move the file to the required folder
            shutil.move('C:/Users/' + globalvars.user_path + '/Downloads/' + str(globalvars.bridgeID[i]) + ' BrM Report_' + date + '.pdf', globalvars.folders[i])
            # refresh the page and go back to the previous page
            driver.refresh()
            time.sleep(5)
            presstab_driver = ActionChains(driver).send_keys(Keys.TAB).perform()
            time.sleep(1) 
            pressenter_driver = ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(30)

        def download_prev_reports(self, driver):
            return