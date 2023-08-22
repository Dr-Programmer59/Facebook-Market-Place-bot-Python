from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialog,QApplication,QWidget
import threading,sys
import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from selenium.webdriver.chrome.options import Options
import os
import json
import undetected_chromedriver as uc
import csv
import random
from datetime import datetime
import uuid
import pyperclip as cp


time_start="20/8/2023" #day/month/year
time_end="25/8/2023" #day/month/year
mac_address="2c:41:38:9f:dc:6a"




date_format = "%d/%m/%Y"
start_date = datetime.strptime(time_start, date_format).date()
end_date = datetime.strptime(time_end, date_format).date()


working=False

def PostProduct(csvfile,status,email,password):
    global working
    products=[]
    try:
        with open(csvfile,"r",encoding="utf-8") as f:
            for i in csv.reader(f):
                products.append(i)
    except:
        status.setText("Csv Path Error")
        working=False
        return 0

    
    status.setText("Login...")
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.facebook.com/")
    driver.find_element(By.ID,"email").send_keys(email)
    driver.find_element(By.ID,"pass").send_keys(password)
    time.sleep(2)
    driver.find_element(By.TAG_NAME,"button").click()
    time.sleep(2)

    if ("facebook.com/login"  in driver.current_url):
        status.setText("Check username or password..")
        working=False
        return 0
    
    

    for i, product in enumerate(products):
       
            status.setText(f"Setting Product {i+1}")
            time.sleep(1)
            driver.get("https://www.facebook.com/marketplace/create/items")
            time.sleep(1)
            images=driver.execute_script("""
            const fileInputs = document.getElementsByTagName("input");

            for (const input of fileInputs) {
                if (input.type === "file") {
                // Handle the file input element
                    return input
                    break
                }
            }
            """)
            images_path=[product[3]]
            for path in images_path:
                images.send_keys(f"{path}")
                time.sleep(1)
            try:
                driver.find_elements(By.TAG_NAME,"textarea")[0].send_keys(product[2])
            except:
                driver.execute_script("""document.querySelector('div[role="main"]').querySelectorAll('div[data-visualcompletion="ignore-dynamic"]')[1].querySelector('div[role="button"]').click()""")
                time.sleep(1)
            labels=driver.find_elements(By.TAG_NAME,"label")



            for label in labels:
                try:
                    if label.get_attribute("aria-label") in "Title":
                        cp.copy(product[0])
                        label.find_element(By.TAG_NAME,"input").send_keys(Keys.CONTROL,"v")
                    if label.get_attribute("aria-label") in "Price":
                        
                        label.find_element(By.TAG_NAME,"input").send_keys(product[1])
                    if label.get_attribute("aria-label") in "Category":
                        label.click()
                        time.sleep(2)
                        element=driver.execute_script("""
                    let a=document.querySelectorAll('div[role="dialog"]'); 
                    let b=a[a.length-1]                      
                    return  b.querySelectorAll('div[style="padding-left: 8px; padding-right: 8px;"]')[2]
                                                    
            """)
                        element.click()
                        time.sleep(1)
                        
                    if label.get_attribute("aria-label") in "Condition":
                        label.click()
                        time.sleep(1)
                        for i in range(1):
                            label.send_keys(Keys.DOWN)
                            label.send_keys(Keys.ENTER)

                        
                    
                    
                except Exception as err:
                    print(err)
                    pass

            time.sleep(1)
            try:
                cp.copy(product[2])
                driver.find_elements(By.TAG_NAME,"textarea")[0].send_keys(Keys.CONTROL,"v")
            except:
                driver.execute_script("""document.querySelector('div[role="main"]').querySelectorAll('div[data-visualcompletion="ignore-dynamic"]')[1].querySelector('div[role="button"]').click()""")
                time.sleep(1)
                driver.find_elements(By.TAG_NAME,"textarea")[0].send_keys(product[2])
                
            tags=product[5]
            cp.copy(tags)
           
            driver.find_elements(By.TAG_NAME,"textarea")[1].send_keys(Keys.CONTROL,"v")
                
               
            location_input=driver.execute_script("""return document.querySelectorAll('input[role="combobox"]')[1]""")

            location_input.send_keys(Keys.CONTROL,"a")

            location_input.send_keys(Keys.BACK_SPACE)

            location_input.send_keys(product[4])

            location_input.send_keys(product[4])
            time.sleep(1)
            location_input.send_keys(Keys.DOWN)
            time.sleep(0.5)
            location_input.send_keys(Keys.ENTER)
            time.sleep(0.5)

            driver.execute_script("""document.querySelector('div[role="checkbox"]').click()""")
            time.sleep(0.1)
            driver.execute_script("""document.querySelector('div[role="switch"]').click();""")
            time.sleep(1)
            
            driver.execute_script("""document.querySelector('div[aria-label="Next"]').click();""")
            time.sleep(3)
            
            driver.execute_script("""document.querySelector('div[aria-label="Publish"]').click();""")

            time.sleep(random.randint(5,10))
        
        
           
class MainScreen(QDialog):
    def __init__(self):
        global working
        super(MainScreen, self).__init__()
        loadUi("main.ui",self)
        current_date = datetime.now().date()

        # Compare the dates
        mac_AddressChk=':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
        for ele in range(0,8*6,8)][::-1])
        if end_date < current_date or start_date>current_date:
            self.status.setText("Your Date is Expired...")
        elif mac_AddressChk!=mac_address:
            self.status.setText("Your are not Allowed to Use this software..")
        else:
           
            self.start.clicked.connect(self.startProcess)
    def startProcess(self):
        
        global working
        if working==False:
            working=True
            print(working)
            t=threading.Thread(target=lambda:PostProduct(self.csvFile.text(),self.status,self.email.text(),self.password.text()))
            t.daemon=True
            t.start()


app=QApplication(sys.argv)   
widget= QtWidgets.QStackedWidget()
main=MainScreen()
widget.addWidget(main)
widget.setFixedWidth(695)
widget.setFixedHeight(440)
widget.show()
try:
    sys.exit(app.exec_())
except Exception as err:
    print(err)
    print('exiting')
   