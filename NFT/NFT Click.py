from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tkinter import *
import os
import time


with open("phantom.txt") as f:  # This file should be in root folder
    DATA = f.read().split("\n")
    SECRET_PHANTOM = DATA[0]
    PASSWORD = DATA[1]


def interface(text):
    'GUI'
    def callback():
        window.destroy()  # Closing a window after clicking on a button

    window = Tk()
    window.call('wm', 'attributes', '.', '-topmost', '1')  # Lock a window above other programs
    user_input = StringVar()  # Set input as a variable
    window.title("NFT Buyer")
    Label(text=f"{text}", width=30, height=3, font="15").pack()
    e = Entry(window, width=55, textvariable=user_input)  # Input
    e.pack()
    e.focus_set()
    Button(text="ОК", width=10, padx="130", command=callback).pack()
    window.mainloop()
    return user_input


def preset_options():
    'Wallet install'
    chrome_options = Options()
    chrome_options.add_extension("Phantom.crx") # Install Phantom
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='chromedriver.exe')  # Initiate webdriver
    return driver


def click_button(url):
    'Launch browser and clicks'
    driver.get(url)  # Open URL
    time.sleep(2)  # Wait for complite loading
    xpath = activate_phantom(driver)  # Get XPath and activate wallets
    counter = 0
    while True:
        try:
            if counter % 3 == 0:
                driver.find_element_by_xpath(xpath).click()  # Endless clicks
                driver.switch_to.window(driver.window_handles[1]) # Switch to the transaction window
                driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[2]/div/button[2]').click()  # АВТО-ПОДТЕВРЖДЕНИЕ    | Только ОДНА из этих 2х строк должна быть активна, иначе жопа
                #driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[2]/div/button[1]').click() # АВТО-ОТМЕНА           | Чтобы ВЫКЛЮЧИТЬ строку, поставьте перед ней решетку #,
                driver.switch_to.window(driver.window_handles[0])  # Switch to the main window                                       | чтобы ВКЛЮЧИТЬ - уберите решетку перед строкой
            else:
                driver.find_element_by_xpath(xpath).click()
            counter += 1
        except:
            counter += 1


def activate_phantom(driver):
    'Automatic data entry into wallets'
    wait = WebDriverWait(driver, 500)
    driver.switch_to.window(driver.window_handles[0]) # Set Phantom tab active
    driver.find_element_by_xpath('//*[@id="root"]/main/div/div/section/button[2]').click()  # Connect existing wallet
    time.sleep(3)
    imputElement = driver.find_element_by_xpath('//*[@id="root"]/main/div[2]/div/form/div[1]/div/section/div/textarea')
    imputElement.send_keys(SECRET_PHANTOM) # Writing secret phrase
    imputElement.submit()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/div/div/button'))).click()  # Import wallets
    time.sleep(1)
    password = driver.find_element_by_name('password') # Write password
    password.send_keys(PASSWORD)
    password2 = driver.find_element_by_name('confirmPassword') # Confirm password
    password2.send_keys(PASSWORD)
    driver.find_element_by_xpath('//*[@id="root"]/main/div[2]/div/form/div[2]/div[1]/span/input').click()  # Accept policy
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/div/form/div[2]/div[2]/button'))).click() # Continue
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div[2]/div/div[2]/button'))).click()  # Continue
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="root"]/main/div[2]/div/div[2]/button').click() # Close
    driver.switch_to.window(driver.window_handles[0])  # Return active tab to main URL
    os.system('CLS') # Clear console
    xpath = interface("Введите XPath кнопки покупки").get()  # Button XPath input
    return xpath


if __name__ == '__main__':
    url = interface("Введите ссылку на страницу с NFT").get()
    driver = preset_options()
    click_button(url)
    driver.close
    quit