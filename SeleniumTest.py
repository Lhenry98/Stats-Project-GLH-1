import time
import settings
import shutil
import os.path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

while(True):
   
    for i in settings.CompList:
        CompName = i
    
        #create Chrome instance
        service = Service(executable_path=r"C:\Users\LEEMU\Anaconda\envs\GianniProject\Chrome.exe")
        options = Options()
        #True means browser is invisible
        options.headless = False
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options = options)
      
        driver.get("https://app.ticketutils.com/")
        delay = 180 #seconds
        
        #get username and password elements
        SiteUsername = driver.find_element_by_name('Email')
        SitePassword = driver.find_element_by_name('Password')
        
        #submit login info
        SiteUsername.send_keys(settings.TU_Username)
        SitePassword.send_keys(settings.TU_Password)
        #click login button
        driver.find_element_by_xpath("/html/body/div[2]/div/div/form/div/div[3]/button").click()
        
        #click "Reports" button
        try:
            Reportsbutton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, "POS_Reports")))
            driver.find_element_by_id("POS_Reports").click()
            print("Reports: Success!")
        except TimeoutException:
            print("Reports: Loading took too much time!")
        
        #click "Profit/Loss" button
        PLFrame = driver.find_element_by_css_selector("#WorkArea > div > div.Active > iframe")
        try:
            PLbutton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#WorkArea > div > div.Active > iframe")))
            driver.switch_to.frame(PLFrame)
            driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/div[1]/div/div/div[2]/ul/li[3]/div/div[1]/a").click()
            print("P/L: Success!")
            driver.switch_to.default_content()
        except TimeoutException:
            print("P/L: Loading took too much time!")
        
        #filter results
        FilterFrame = driver.find_element_by_css_selector("#WorkArea > div > div.Active > iframe")
        try:
            #click next tab
            driver.find_element_by_xpath("/html/body/div[2]/nav/div[2]/div[3]/span[3]").click()
            #wait for iframe to load in
            ListFrame = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#WorkArea > div > div.Active > iframe")))
            driver.switch_to.frame(FilterFrame)
            #wait for list of data to load in
            ListData = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="load_List"][contains(@style, "display: none;")]')))
            #click filter button
            driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/ul/li[1]/a").click()
            #enter filter data
            CustomerFilter = driver.find_element_by_name("Event.Value")
            CustomerFilter.click()
            CustomerFilter.send_keys(CompName)
            #need to click autocomplete for some reason
            time.sleep(1)
            #driver.find_element_by_xpath("/html/body/div[4]/ul/li").click()
            #click search when page is loaded
            driver.find_element_by_id("Search").click()
            print("Filter: Success!")
        except TimeoutException:
            print("Filter: Loading took too much time!")
        
        #download excel sheet
        try:
            ListData = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="load_List"][contains(@style, "display: none;")]')))
            driver.find_element_by_id("MoreActions").click()
            driver.find_element_by_xpath("/html/body/div[4]/ul/li[2]").click()
            print("Export: Success!")
        except TimeoutException:
            print("Export: Loading took too long!")
            
        #move new file to correct directory and replace old file
        while os.path.isfile("C:/Users/LEEMU/Downloads/Profit_Loss.xlsx") == False:
            time.sleep(1)
        if os.path.isfile("C:/Users/LEEMU/Downloads/Profit_Loss.xlsx"):
            shutil.move("C:/Users/LEEMU/Downloads/Profit_Loss.xlsx", "C:/Users/LEEMU/Anaconda/envs/GianniProject/App/" + CompName + ".xlsx")
        else:
            print("File couldn't be found!")
        
        #convert file to csv
        read_file = pd.read_excel(CompName + ".xlsx")
        read_file.to_csv(CompName + ".csv", index = None, header = True)
        #SLLayer = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/iframe")))
        #driver.switch_to.frame(SLLayer)
        #quit webdriver
        driver.close()
        #wait 5 minutes then run again
        time.sleep(300)
