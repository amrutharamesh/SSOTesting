#Make variable names with underscores
import os
import csv
import json
import re
##from pudb import set_trace; set_trace()
from selenium import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhantomJS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from bs4 import NavigableString
from wait_for import wait_for

websites = []


class Search:
    def __init__(self, path, websites):
        self.exec_path = path
        self.driver = webdriver.PhantomJS(executable_path=self.exec_path)
        self.websites = websites
        self.fileExceptionList = []
        self.fileLogList = []
        self.candidates = []
        self.begin_search_for_SSO()

    def begin_search_for_SSO(self):
        for site in self.websites:
            self.driver.set_page_load_timeout(40)
            self.driver.set_window_size(1400,1000)
            self.first_url = "https://www."+site
            self.sso_info = {"url" : self.first_url, "loginSSO" : [], "signupSSO" : []}
            try:
                self.driver.get(self.first_url)
            except (TimeoutException, Exception) as t:
                log_obj = {
                    "url" : self.first_url,
                    "reason" : "An exception occurred during first time page load"
                }
                self.fileLogList.append(log_obj)
                continue
            else:
                first_url_doc = self.parse_web_page()
                self.process_page_for_click_candidates(first_url_doc, "login")
                first_click_doc = self.parse_web_page()
                self.search_for_SSO(first_click_doc, "login")
                self.process_page_for_click_candidates(self.parse_web_page(), "signup")
                self.search_for_SSO(self.parse_web_page(), "signup")
        self.done()
        self.write_to_file()

    def parse_web_page(self):
        self.driver.save_screenshot('screenshot.png')
        html = self.driver.page_source
        parsed = BeautifulSoup(html, "lxml")
        return parsed

    def process_page_for_click_candidates(self, document, ptype):
        if ptype == 'login':
            found_elems = document.find_all(["a", "button", "span", "div", "img"], string=['Log In', 'LogIn', 'Login', 'Log in', 'Sign in', 'Sign In', 'Signin', 'SignIn', 'SIGNIN', 'SIGN IN', 'LOGIN', 'LOG IN', 'login', 'log in', 'signin', 'sign in'])
        elif ptype == 'signup':
            found_elems = document.find_all(["a", "button", "span", "div", "img"], string=['Sign Up', 'Signup', 'SignUp', 'Sign up', 'SIGN UP', 'SIGNUP', 'sign up', 'signup', 'Create account', 'Create Account', 'CREATE ACCOUNT', 'create account'])
        
        found_url = self.extract_url(found_elems)
        print found_url
        if(found_url):
            if found_url.startswith("/"):
                found_url = self.first_url + found_url
            try:
                self.driver.get(str(found_url))
            except (TimeoutException, Exception) as t:
                log_obj = {
                    "url" : self.first_url,
                    "reason" : "An exception occurred during click candidate process"
                }
                self.fileLogList.append(log_obj)
                return
        else:
            if ptype == 'login':
                exception_obj = {
                        "url" : self.first_url,
                        "reason" : "login url extraction failed"
                    }
            else:
                exception_obj = {
                    "url" : self.first_url,
                    "reason" : "Sign up url extraction failed"
                }                     
            self.fileExceptionList.append(exception_obj)
            
    def extract_url(self, elems):
        while(len(elems) > 0):
            each = elems.pop()
            url = each.get('href')
            if url is not None:
                print url
                return url
            else:
                parent = each.find_parent('a') or each.find_parent('button')
                if parent is None:
                    continue
                else:
                    p_url = parent.get('href')
                    if p_url is None:
                        continue
                    else:
                        print p_url
                        return p_url

    def search_for_SSO(self, document, stype):
        stack = []
        stack = document.body.contents
        while(len(stack) > 0):
            current = stack.pop()
            if(not(isinstance(current, NavigableString))):
                children = current.contents
                if len(children) > 0:
                    for child in children:
                        if(not(isinstance(child, NavigableString))):
                            stack.insert(0, child)

                if not(current.name == 'script' or current.attrs == None or current.name == 'embed'):
                    self.process_node(current, stype)

    def process_node(self, node, stype):
        if self.filter_node_on_type(node):
            attrs = node.attrs
            str_to_check = node.string or ''
            for key in attrs:
                try:
                    str_to_check += key+'='+str(attrs[key])+';'
                except UnicodeError:
                    continue
                else:
                    self.check_for_keywords(str_to_check, stype)




    def filter_node_on_type(self, node):
        if (node.name != "a" and node.name != "div" and node.name != "img" and
            node.name != "span" and node.name != "input" and
            node.name != "button"):
            return False
        if (node.name == "input"):
            if (node.type != "button" and node.type != "img" and
            node.type != "submit"):
                return False
        if (node.name == "A"):
            if (node.get('href').toLowerCase().indexOf('mailto:') == 0):
                return False
        return True

            
    def check_for_keywords(self, inputstr, stype):
        sso = [{"site" : 'google', "url" : ["https://accounts.google.com/o/oauth2"]}, {"site" : 'yahoo', "url" : ["https://api.login.yahoo.com/oauth2"]}, 
        {"site" : '500px', "url": ["https://api.500px.com/v1/oauth"]}, {"site" : 'aol', "url" :["https://api.screenname.aol.com/auth"]}, 
        {"site" : 'twitter', "url" : ["https://api.twitter.com/oauth"]}, {"site" : 'vk', "url" : ["https://oauth.vk.com/authorize"]}, 
        {"site" : 'yammer', "url" : ["https://www.yammer.com/oauth2/authorize"]}, {"site" : 'yandex', "url" : ["https://oauth.yandex.com/authorize"]},
        {"site" : 'zendesk', "url" : [".zendesk.com/oauth/tokens"]}, {'amazon'},
        {"site" : 'flickr', "url" : ["https://www.flickr.com/services/oauth"]}, {"site" : 'bitbucket', "url" : ["https://bitbucket.org/site/oauth2", "https://bitbucket.org/api/1.0/oauth"]}, {"site" : 'bitly', "url" : ["https://bitly.com/oauth"]}, 
        {"site" : 'cloud foundry', "url" : ["/uaa/oauth"]}, {"site" : 'dailymotion', "url" : ["https://www.dailymotion.com/oauth"]}, 
        {"site" : 'deviantART', "url" : ["https://www.deviantart.com/oauth2"]}, {"site" : 'discogs', "url" : ["https://api.discogs.com/oauth"]}, 
        {"site" : 'huddle', "url" : ["https://login.huddle.net/request"]}, {"site" : 'netflix', "url" : ["https://api-user.netflix.com/oauth"]}, 
        {"site" : 'openlink data spaces', "url" : ["/OAuth"]}, {"site" : 'openstreetmap', "url" : ["http://www.openstreetmap.org/oauth"]}, 
        {"site" : 'opentable', "url" : ["http://www.opentable.com/oauth"]}, {"site" : 'passport', "url" : ["/dialog/authorize", "oauth2/authorize", "oauth/authorize"]},
        {"site" : 'paypal', "url" : ["paypal.com/v1/oauth2"]}, 
        {"site" : 'plurk', "url" : ["https://www.plurk.com/OAuth/authorize"]}, {"site" : 'sina weibo', "url" : ["http://api.t.sina.com.cn/oauth/authorize"]},
        {"site" : 'stack exchange', "url" : ["https://stackexchange.com/oauth"]}, {"site" : 'statusnet', "url" : ["status.net/api/oauth/authorize"]}, 'ubuntu one', 'viadeo', 'vimeo', 
        'withings', 'xero', 'xing', {"site" : 'goodreads', "url" : ["http://www.goodreads.com/oauth"]}, {"site" : 'google app engine', "url" : ["https://accounts.google.com/o/oauth2/v2/auth"]},
        {"site" : 'groundspeak', "url" : []}, 'intel cloud services', 
        {"site" : 'jive', "url" : "jiveon.com/oauth2"}, {"site" : "linkedin", "url" : "https://www.linkedin.com/oauth/v2"}, {"site" : 'trello', "url" : ["https://trello.com/1/OAuthAuthorizeToken", "https://trello.com/1/authorize"]}, 
        {"site" : 'tumblr', "url" : ["https://www.tumblr.com/oauth/authorize"]}, {"site" : 'microsoft', "url" : "https://login.live.com/oauth20"},
        {"site" : 'mixi', "url" : "api.mixi-platform.com/OAuth"}, {"site" : 'myspace', "url" : "api.myspace.com/authorize"}, {"site" : 'etsy', "url" : ["https://www.etsy.com/oauth"]}, {"site" : 'evernote', "url" : ["https://sandbox.evernote.com/OAuth.action"]},  
        'yelp',  {"site" : 'facebook', "url" : ["fb-login-button"]},
        {"site" : "dropbox", "url" : ["https://www.dropbox.com/1/oauth2", "https://www.dropbox.com/1/oauth"]}, {"site" : "twitch", "url" : ["https://api.twitch.tv/kraken/oauth2/authorize"]}]
        k0 = re.compile('oauth', re.I)
        k1 = re.compile('openid', re.I)
        k2 = re.compile('log[\-\S]?[io]n', re.I)
        k3 = re.compile('sign[\-\S]?[io]n', re.I)
        k4 = re.compile('sign[\-\S]?up', re.I)
        e0 = re.compile('social', re.I)
        e1 = re.compile('subscribe', re.I)
        e2 = re.compile('connect', re.I)
        e3 = re.compile('like', re.I)

        for each in sso:
            compiled = re.compile(each, re.I | re.S)
            if compiled.search(inputstr) is not None:
                if k0.search(inputstr) is not None or k1.search(inputstr) is not None:
                    if stype == 'login':
                        if k2.search(inputstr) is not None or k3.search(inputstr) is not None:
                            if each not in self.sso_info["loginSSO"]:
                                self.sso_info["loginSSO"].append(each)
                                print "2"
                    elif stype == 'signup':
                        if k4.search(inputstr) is not None:
                            if each not in self.sso_info["signupSSO"]:
                                self.sso_info["signupSSO"].append(each)
                else:
                    if e0.search(inputstr) is not None or e1.search(inputstr) is not None or e2.search(inputstr) is not None or e3.search(inputstr) is not None:
                        print "6"

    def write_to_file(self):
        self.candidates.append(self.sso_info)
        file_exception = open("exceptions.txt", "w")
        file_exception.write(json.dumps(self.fileExceptionList))
        file_exception.close()
        
        logFile = open("log.txt", "w")
        logFile.write(json.dumps(self.candidates))
        logFile.close()

        sys_exceptions = open("errors.txt", "w")
        sys_exceptions.write(json.dumps(self.fileLogList))
        sys_exceptions.close()

    def done(self):
        self.driver.quit()



with open('summa.csv') as csvFile:
    reader = csv.reader(csvFile, delimiter=",")
    for data in reader:
        websites.append(data[1])
    csvFile.close()

path ='/Users/amrutharamesh/Desktop/My documents/Semester 4/Masters Final Project/SSOTesting/lib/phantomjs-2.1.1-macosx/bin/phantomjs'
search = Search(path, websites)





##try:
##            loginElem = self.driver.find_elements_by_xpath("//*[text()='Log In'] | //*[text()='LogIn'] | //*[text()='Login'] | //*[text()='Log in'] |  //*[text()='Sign in'] | //*[text()='Sign In'] |  //*[text()='Signin'] | //*[text()='SignIn'] | //*[text()='SIGNIN'] | //*[text()='SIGN IN'] | //*[text()='LOGIN'] |  //*[text()='LOG IN'] |  //*[text()='login'] |  //*[text()='log in'] |  //*[text()='signin'] |  //*[text()='sign in'] | //*[@value='Log In'] | //*[@value='LogIn'] | //*[@value='Login'] | //*[@value='Log in'] |  //*[@value='Sign in'] | //*[@value='Sign In'] |  //*[@value='Signin'] | //*[@value='SignIn'] | //*[@value='SIGNIN'] | //*[@value='SIGN IN'] | //*[@value='LOGIN'] |  //*[@value='LOG IN'] |  //*[@value='login'] |  //*[@value='log in'] |  //*[@value='signin'] |  //*[@value='sign in']")[0].click()
##            old_element = WebDriverWait(self.driver, 40).until(EC.staleness_of(self.driver.find_element_by_tag_name('html')))
##            print old_element
##        except (NoSuchElementException, Exception, TimeoutException) as e:
##            print 'hi3'
##            print e
##            return
##        else:
##            print "hi2"
##            if(old_element):
##                self.filterPageForSSO()
##
##                class wait_for_page_load(object):
##    def __init__(self, browser):
##        self.browser = browser
##
##    def __enter__(self):
##        self.old_page = self.browser.current_url
##
##    def page_has_loaded(self):
##        new_page = self.browser.current_url
##        return new_page != self.old_page
##
##    def __exit__(self, *_):
##        wait_for(self.page_has_loaded)

##     self.driver.save_screenshot('screenshot.png')
##        html = self.driver.page_source
##        parsed = BeautifulSoup(html, "lxml")
##        print parsed.title
##        try:
##            signupElem = self.driver.find_element_by_xpath("//*[text()='Sign Up'] | //*[text()='Signup'] | //*[text()='SignUp'] |  //*[text()='Sign up'] |   //*[text()='Create account'] | //*[text()='Create Account']  | //*[text()='CREATE ACCOUNT'] | //*[text()='create account'] | //*[@value='Sign Up'] | //*[@value='Signup'] | //*[@value='SignUp'] |  //*[@value='Sign up'] |   //*[@value='Create account'] | //*[@value='Create Account']  | //*[@value='CREATE ACCOUNT'] | //*[@value='create account']")
##        except (NoSuchElementException, Exception) as e:
##            print e



##
##try:
##            loginElems = self.driver.find_elements_by_xpath("//*[text()='Log In'] | //*[text()='LogIn'] | //*[text()='Login'] | //*[text()='Log in'] |  //*[text()='Sign in'] | //*[text()='Sign In'] |  //*[text()='Signin'] | //*[text()='SignIn'] | //*[text()='SIGNIN'] | //*[text()='SIGN IN'] | //*[text()='LOGIN'] |  //*[text()='LOG IN'] |  //*[text()='login'] |  //*[text()='log in'] |  //*[text()='signin'] |  //*[text()='sign in'] | //*[@value='Log In'] | //*[@value='LogIn'] | //*[@value='Login'] | //*[@value='Log in'] |  //*[@value='Sign in'] | //*[@value='Sign In'] |  //*[@value='Signin'] | //*[@value='SignIn'] | //*[@value='SIGNIN'] | //*[@value='SIGN IN'] | //*[@value='LOGIN'] |  //*[@value='LOG IN'] |  //*[@value='login'] |  //*[@value='log in'] |  //*[@value='signin'] |  //*[@value='sign in']")
##            if len(loginElems)>0:
##                extracted_url = self.extract_url_frm_elems(loginElems, 'login')
##                if extracted_url is not None:
##                   self.driver.get(str(extracted_url))
##                   self.parse_web_page()
##                else:
##                    exceptionObj = {
##                         "url" : self.first_url,
##                         "reason" : "url extract failed"
##                        }
##                    self.fileExceptionList.append(json.dumps(exceptionObj, indent=2))
##        except (NoSuchElementException, Exception, TimeoutException) as e:
##            print e
##            return

##if not(current.attrs is None or current.name == 'SCRIPT' or current.name == 'EMBED'):
##                self.process_node(current)
##for current in sso:
##            print current
##
##            if (current.name != "A" and current.name != "DIV" and current.name != "IMG" and
##            current.name != "SPAN" and current.name != "INPUT" and current.name != "BUTTON"):
##            return False
##        if (current.name == "INPUT"):
##            if (current.type != "button" and current.type != "img" and current.type != "submit"):
##                return False
##        if (current.name == "A"):
##            if (current.href.toLowerCase().indexOf('mailto:') == 0):
##                return False
##        return True
##
##if(self.filter_node(node)):
##            attrs = node.attrs
##            for key in attrs:
##                str_to_check = key +"=" +attrs[key] +";"
##                self.check_for_keywords(str_to_check)
##def run_prelim_srch(self):
##
##    def search_for_SSO(self, document):
##        stack = []
##
##
##
##
##    def filter_node(self, node):
##
##
##    def process_node(self, node):
##
##
##    def check_for_keywords(self, input_str):
##        sso = ['/google/gi', '/yahoo/gi', '/500px/gi', '/amazon/gi', '/aol/gi', '/box/gi', '/basecamp/gi', '/battle\.net/gi', '/bitbucket/gi', '/bitly/gi',
##               '/foursquare/gi', '/cloud foundry/gi', '/dailymotion/gi', '/deviantART/gi', '/discogs/gi', '/dropbox/gi', '/etsy/gi', '/evernote/gi',
##               '/facebook/gi', '/fitbit/gi', '/flickr/gi', '/formstack/gi', '/github/gi', '/goodreads/gi', '/google app engine/gi', '/groundspeak/gi',
##               '/huddle/gi', '/imgur/gi', '/instagram/gi', '/intel cloud services/gi', '/jive/gi', '/linkedin/gi', '/microsoft/gi', '/mixi/gi', '/myspace/gi',
##               '/netflix/gi', '/openlink/gi', '/openstreetmap/gi', '/opentable/gi', '/passport/gi', '/paypal/gi', '/plurk/gi', '/reddit/gi', '/salesforce/gi',
##               '/sina weibo/gi', '/stack exchange/gi', '/statusnet/gi', '/strava/gi', '/stripe/gi', '/trello/gi', '/tumblr/gi', '/twitch/gi', '/twitter/gi',
##               '/ubuntu one/gi', '/viadeo/gi', '/vimeo/gi', '/vk/gi', '/withings/gi', '/xero/gi', '/xing/gi', '/yammer/gi', '/yandex/gi', '/yelp/gi',
##               '/zendesk`/gi']
##
##
##
##    def extract_url_frm_elems(self, elems, etype):
##        if etype == 'login':
##            for each in elems:
##                url = each.get_attribute('href')
##                if url is None:
##                    parent = each.find_element_by_xpath('..')
##                    if parent is not None:
##                        p_url = parent.get_attribute('href')
##                        if p_url is None:
##                            continue
##                        else:
##                            return p_url
##                    continue
##                else:
##                    return url
##        elif etype == 'sign in':
##            print 'hi'


## while len(all_relevant_tags) > 0:
##            current = all_relevant_tags.pop()
##            print current
##            print "----------------------------"
##            if not(isinstance(current, NavigableString)):
##                attrs = current.attrs
##                str_to_check = current.string or ''
##                for key in attrs:
##                    try:
##                        str_to_check += key+"="+str(attrs[key])+";"
##                    except UnicodeError as u:
##                        continue
##                self.check_for_keywords(str_to_check, stype)



# if compiled.search(inputstr) is not None:
#                 if keywords[0].search(inputstr) is not None or keywords[1].search(inputstr) is not None:
#                     if stype == 'login':
#                             if keywords[2].search(inputstr) is not None or keywords[3].search(inputstr) is not None:
#                                     self.sso_info["loginSSO"].append(each)
#                                     print "2"
#                             else:
#                                 print "3"
#                     elif stype == 'signup':
#                         if keywords[4].search(inputstr) is not None:
#                             print "4"
#                             self.sso_info["signupSSO"].append(each)
#                         else:
#                             print "5"
                        
#                 else:
#                     if elimination[0].search(inputstr) is not None or elimination[1].search(inputstr) is not None or elimination[2].search(inputstr) is not None or elimination[3].search(inputstr) is not None:
#                         print "6"
