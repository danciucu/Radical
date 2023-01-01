from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import shutil
import PyPDF2
import os
import globalvars

def main(driver):
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