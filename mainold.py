# @Author: amrutharamesh
# @Date:   2017-02-23T09:22:00-06:00
# @Last modified by:   amrutharamesh
# @Last modified time: 2017-03-02T10:53:56-06:00



import os
import csv
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

executable_path = "/Users/amrutharamesh/Desktop/My_software/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path

chrome_options = Options()
chrome_options.add_extension('/Users/amrutharamesh/Desktop/My documents/Semester 4/Masters Final Project/SSOPhishing.crx')

reader = csv.reader(open('summa.csv', 'rb'), delimiter=",")
mylist = []
for data in reader:
    mylist.append(data[1])

driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)


##    buttons = driver.find_elements_by_xpath("//button[text()='Log In'] | //button[text()='LogIn'] | //button[text()='Login'] |  //button[text()='Sign in'] | //button[text()='Sign In']")
##    inputs = driver.find_elements_by_xpath("//input[text()='Log In'] | //input[text()='LogIn'] | //input[text()='Login'] |  //input[text()='Sign in'] | //input[text()='Sign In']")
##    anchors = driver.find_elements_by_xpath("//a[text()='Log In'] | //a[text()='LogIn'] | //a[text()='Login'] |  //a[text()='Sign in'] | //a[text()='Sign In']")
##    if len(buttons) > 0:
##        action.move_to_element(buttons[0]).click()
##        action.perform()
##    elif len(inputs) > 0:
##        action.move_to_element(inputs[0]).click()
##        action.perform()
##    elif len(anchors) > 0:
##        action.move_to_element(anchors[0]).click()
##        action.perform()

for i in mylist:
    action = ActionChains(driver)
    try:
        driver.get("https://www.google.com")
        driver.set_page_load_timeout(50)
        loginElements = driver.find_elements_by_xpath("//*[text()='Log In'] | //*[text()='LogIn'] | //*[text()='Login'] | //*[text()='Log in'] |  //*[text()='Sign in'] | //*[text()='Sign In'] |  //*[text()='Signin'] | //*[text()='SignIn'] | //*[text()='SIGNIN'] | //*[text()='SIGN IN'] | //*[text()='LOGIN'] |  //*[text()='LOG IN'] |  //*[text()='login'] |  //*[text()='log in'] |  //*[text()='signin'] |  //*[text()='sign in']")
        #signupElements = driver.find_elements_by_xpath("//*[text()='Sign Up'] | //*[text()='Signup'] | //*[text()='SignUp'] |  //*[text()='Sign up']")
        if loginElements is not None:
            if len(loginElements) > 0:
                action.move_to_element(loginElements[0]).click()
                #if len(signupElements) > 0:
                #action.move_to_element(signupElements[0]).send_keys(Keys.COMMAND).click()
                action.perform()
        else:
            continue
    except Exception as ex:
        continue
