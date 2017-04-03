import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


executable_path = "/Users/amrutharamesh/Desktop/My_software/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path
chrome_options = Options()
chrome_options.add_extension('/Users/amrutharamesh/Desktop/My documents/Semester 4/Masters Final Project/SSOPhishing.crx')
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)

reader = csv.reader(open('top-80k.csv', 'rt'), delimiter=",")
mylist = []
for data in reader:
    mylist.append(data[1])

for site in mylist:
    action = ActionChains(driver)
    driver.set_page_load_timeout(50)
    driver.get("https://www."+site)
    try:
        loginElement = driver.find_element_by_xpath("//*[text()='Log In'] | //*[text()='LogIn'] | //*[text()='Login'] | //*[text()='Log in'] |  //*[text()='Sign in'] | //*[text()='Sign In'] |  //*[text()='Signin'] | //*[text()='SignIn'] | //*[text()='SIGNIN'] | //*[text()='SIGN IN'] | //*[text()='LOGIN'] |  //*[text()='LOG IN'] |  //*[text()='login'] |  //*[text()='log in'] |  //*[text()='signin'] |  //*[text()='sign in']")           
        if loginElement is not None:
            action.move_to_element(loginElement).click().perform()
           
            signupElement = driver.find_element_by_xpath("//*[text()='Sign Up'] | //*[text()='Signup'] | //*[text()='SignUp'] |  //*[text()='Sign up'] |  //*[text()='SIGN UP'] |  //*[text()='SIGNUP'] |  //*[text()='Create account'] |  //*[text()='Create Account'] |  //*[text()='CREATE ACCOUNT']")
            if signupElement is not None:
                action.move_to_element(loginElement).click().perform()
    except (Exception, TimeoutException) as e:
        continue



































##    if loginElements is not None:
##        if len(loginElements) > 0:
##            print 
##            action.move_to_element(loginElements[0]).key_down(Keys.COMMAND).click().key_up(Keys.COMMAND)
##            action.perform()
##    if signupElements is not None:
##        if len(signupElements) > 0:
##            action.move_to_element(signupElements[0]).key_down(Keys.COMMAND).click().key_up(Keys.COMMAND)
##            action.perform()
    #driver.quit()


##driver.set_window_size(1024, 768)
