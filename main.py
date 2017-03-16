import csv
import os
import sys
sys.path.insert(0, 'wait_for/')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import wait_for

class wait_for_page_load(object):
    def __init__(self, driver):
        self.driver = driver
    def __enter__(self):
        self.old_page = self.driver.find_element_by_tag_name('html')
    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id
    def __exit__(self, *_):
        wait_for(self.page_has_loaded)



executable_path = "/Users/amrutharamesh/Desktop/My_software/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path
#executable_path='/usr/local/lib/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs'
chrome_options = Options()
chrome_options.add_extension('/Users/amrutharamesh/Desktop/My documents/Semester 4/Masters Final Project/SSOPhishing.crx')
reader = csv.reader(open('summa.csv', 'rb'), delimiter=",")
mylist = []
for data in reader:
    mylist.append(data[1])

for site in mylist:
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    #   driver = webdriver.PhantomJS(executable_path=executable_path)
    action = ActionChains(driver)
    driver.get("https://www."+site)
    driver.set_page_load_timeout(50)
    #try:
    loginElement = driver.find_element_by_xpath("//*[text()='Log In'] | //*[text()='LogIn'] | //*[text()='Login'] | //*[text()='Log in'] |  //*[text()='Sign in'] | //*[text()='Sign In'] |  //*[text()='Signin'] | //*[text()='SignIn'] | //*[text()='SIGNIN'] | //*[text()='SIGN IN'] | //*[text()='LOGIN'] |  //*[text()='LOG IN'] |  //*[text()='login'] |  //*[text()='log in'] |  //*[text()='signin'] |  //*[text()='sign in']")           
    if loginElement is not None:
        action.move_to_element(loginElement).click().perform()
        with wait_for_page_load(driver):
            signupElement = driver.find_element_by_xpath("//*[text()='Sign Up'] | //*[text()='Signup'] | //*[text()='SignUp'] |  //*[text()='Sign up'] |  //*[text()='SIGN UP'] |  //*[text()='SIGNUP'] |  //*[text()='Create account'] |  //*[text()='Create Account'] |  //*[text()='CREATE ACCOUNT']")
            if signupElement is not None:
                print signupElement




































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
