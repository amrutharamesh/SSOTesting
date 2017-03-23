#Make variable names with underscores
import os
import csv
import json
import re
##from pudb import set_trace; set_trace()
from selenium import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhantomJS
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from bs4 import NavigableString
from urllib2 import URLError

websites = []


class Search:
    def __init__(self, path, websites):
        self.exec_path = path
        self.driver = PhantomJS(executable_path=self.exec_path)
        self.websites = websites
        self.fileExceptionList = []
        self.fileLogList = []
        self.candidates = []
        self.begin_search_for_SSO()

    def begin_search_for_SSO(self):
        for site in self.websites:
            print site
            self.driver.set_page_load_timeout(60)
            self.first_url = "https://www."+site
            self.sso_info = {"url" : self.first_url, "loginSSO" : [], "signupSSO" : []}
            try:
                self.driver.get(self.first_url)
            except URLError as u:
                log_obj = {
                    "url" : self.first_url,
                    "reason" : "An exception occurred during first time page load url error"
                }
                self.fileLogList.append(log_obj)
                continue
            except (TimeoutException, Exception) as t:
                log_obj = {
                    "url" : self.first_url,
                    "reason" : "An exception occurred during first time page load timeout exception"
                }
                self.fileLogList.append(log_obj)
                continue
            else:
                first_url_doc = self.parse_web_page()
                self.process_page_for_click_candidates(first_url_doc, "login")
                self.search_for_SSO(self.parse_web_page(), "login")
                self.process_page_for_click_candidates(self.parse_web_page(), "signup")
                self.search_for_SSO(self.parse_web_page(), "signup")
                self.candidates.append(self.sso_info)
                print self.candidates
        self.write_to_file()
        self.done()

    def parse_web_page(self):
        html = self.driver.page_source
        parsed = BeautifulSoup(html, "lxml")
        return parsed

    def process_page_for_click_candidates(self, document, ptype):
        if ptype == 'login':
            found_elems = document.find_all(["a", "button", "span", "div", "img"], string=['Log In', 'LogIn', 'Login', 'Log in', 'Sign in', 'Sign In', 'Signin', 'SignIn', 'SIGNIN', 'SIGN IN', 'LOGIN', 'LOG IN', 'login', 'log in', 'signin', 'sign in'])
        elif ptype == 'signup':
            found_elems = document.find_all(["a", "button", "span", "div", "img"], string=['Sign Up', 'Signup', 'SignUp', 'Sign up', 'SIGN UP', 'SIGNUP', 'sign up', 'signup', 'Create account', 'Create Account', 'CREATE ACCOUNT', 'create account'])
        
        found_url = self.extract_url(found_elems)
        
        if(found_url):
            if found_url.startswith("/"):
                found_url = self.first_url + found_url
            try:
                self.driver.get(found_url)
            except URLError as u:
                log_obj = {
                    "url" : self.first_url,
                    "reason" : "An exception occurred during click candidate process url error"
                }
                self.fileLogList.append(log_obj)
                return
            except (TimeoutException, Exception) as t:
                log_obj = {
                    "url" : self.first_url,
                    "reason" : "An exception occurred during click candidate process timeout exception"
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
                        return p_url

    def search_for_SSO(self, document, stype):
        stack = []
        if document is not None and document.body is not None:
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
        sso = [{"site" : 'google', "url" : ["https://accounts.google.com/o/oauth2/auth"]}, 
        {"site" : 'yahoo', "url" : ["https://api.login.yahoo.com/oauth2/request_auth"]}, 
        {"site" : '500px', "url": ["https://api.500px.com/v1/oauth"]}, 
        {"site" : 'aol', "url" :["https://api.screenname.aol.com/auth"]}, 
        {"site" : 'twitter', "url" : ["https://api.twitter.com/oauth"]}, 
        {"site" : 'vk', "url" : ["https://oauth.vk.com/authorize"]}, 
        {"site" : 'yammer', "url" : ["https://www.yammer.com/oauth2/authorize"]}, 
        {"site" : 'yandex', "url" : ["https://oauth.yandex.com/authorize"]},
        {"site" : 'zendesk', "url" : [".zendesk.com/oauth/authorizations/new"]}, 
        {"site" : 'amazon', "url" : ["http://g-ecx.images-amazon.com/images/G/01/lwa/btnLWA", "https://images-na.ssl-images-amazon.com/images/G/01/lwa/btnLWA"]},
        {"site" : 'flickr', "url" : ["https://www.flickr.com/services/oauth"]}, 
        {"site" : 'bitbucket', "url" : ["https://bitbucket.org/site/oauth2", "https://bitbucket.org/api/1.0/oauth"]}, 
        {"site" : 'bitly', "url" : ["https://bitly.com/oauth"]}, 
        {"site" : 'cloud foundry', "url" : ["/uaa/oauth"]}, 
        {"site" : 'dailymotion', "url" : ["https://www.dailymotion.com/oauth"]}, 
        {"site" : 'deviantART', "url" : ["https://www.deviantart.com/oauth2"]}, 
        {"site" : 'discogs', "url" : ["https://api.discogs.com/oauth"]}, 
        {"site" : 'huddle', "url" : ["https://login.huddle.net/request"]}, 
        {"site" : 'netflix', "url" : ["https://api-user.netflix.com/oauth"]}, 
        {"site" : 'openlink data spaces', "url" : ["/OAuth"]}, 
        {"site" : 'openstreetmap', "url" : ["http://www.openstreetmap.org/oauth"]}, 
        {"site" : 'opentable', "url" : ["http://www.opentable.com/oauth"]}, 
        {"site" : 'passport', "url" : ["/dialog/authorize", "oauth2/authorize", "oauth/authorize"]},
        {"site" : 'paypal', "url" : ["paypal.com/v1/oauth2"]}, 
        {"site" : 'plurk', "url" : ["https://www.plurk.com/OAuth/authorize"]},
        {"site" : 'sina weibo', "url" : ["http://api.t.sina.com.cn/oauth/authorize"]},
        {"site" : 'stack exchange', "url" : ["https://stackexchange.com/oauth"]}, 
        {"site" : 'statusnet', "url" : ["status.net/api/oauth/authorize"]}, 
        {"site" : 'ubuntu one', "url" : ["https://login.ubuntu.com/api/1.0/authentications"]},
        {"site" : 'viadeo', "url" : ["https://partners.viadeo.com/oauth/authorize"]},
        {"site" : 'vimeo', "url" : ["https://api.vimeo.com/oauth/authorize"]}, 
        {"site" : 'withings', "url" : ["https://oauth.withings.com/account/authorize"]},
        {"site" : 'xero', "url" : ["https://api.xero.com/oauth/Authorize"]},
        {"site" : 'xing', "url" : ["https://api.xing.com/v1/authorize"]}, 
        {"site" : 'goodreads', "url" : ["http://www.goodreads.com/oauth"]}, 
        {"site" : 'google app engine', "url" : ["https://accounts.google.com/o/oauth2/v2/auth"]},
        {"site" : 'groundspeak', "url" : ["groundspeak.com/oauth"]}, 
        {"site" : 'intel cloud services', "url" : []}, 
        {"site" : 'jive', "url" : ["jiveon.com/oauth2"]}, 
        {"site" : "linkedin", "url" : ["https://www.linkedin.com/oauth/v2/authorization"]}, 
        {"site" : 'trello', "url" : ["https://trello.com/1/OAuthAuthorizeToken", "https://trello.com/1/authorize"]}, 
        {"site" : 'tumblr', "url" : ["https://www.tumblr.com/oauth/authorize"]}, 
        {"site" : 'microsoft', "url" : ["https://login.live.com/oauth20"]},
        {"site" : 'mixi', "url" : ["api.mixi-platform.com/OAuth"]}, 
        {"site" : 'myspace', "url" : ["api.myspace.com/authorize"]}, 
        {"site" : 'etsy', "url" : ["https://www.etsy.com/oauth"]}, 
        {"site" : 'evernote', "url" : ["https://sandbox.evernote.com/OAuth.action"]},  
        {"site" : 'yelp', "url" : ["https://api.yelp.com/oauth2"]},  
        {"site" : 'facebook', "url" : ["fb-login-button", "https://www.facebook.com/v2.0/dialog/oauth"]},
        {"site" : "dropbox", "url" : ["https://www.dropbox.com/1/oauth2/authorize", "https://www.dropbox.com/1/oauth/authorize"]}, 
        {"site" : "twitch", "url" : ["https://api.twitch.tv/kraken/oauth2/authorize"]},
        {"site" : "stripe", "url" : ["https://connect.stripe.com/oauth/authorize"]},
        {"site" : 'basecamp', "url" : ["https://launchpad.37signals.com/authorization/new"]},
        {"site" : "box", "url" : ["https://account.box.com/api/oauth2/authorize"]},
        {"site" : "formstack", "url" : ["https://www.formstack.com/api/v2/oauth2/authorize"]},
        {"site" : "github", "url" : ["https://github.com/login/oauth/authorize"]},
        {"site" : "reddit", "url" : ["https://www.reddit.com/api/v1/authorize"]},
        {"site" : "instagram", "url" : ["https://api.instagram.com/oauth/authorize"]},
        {"site" : "foursquare", "url" : ["https://foursquare.com/oauth2/authorize"]},
        {"site" : "fitbit", "url" : ["https://www.fitbit.com/oauth2/authorize"]},
        {"site" : "imgur", "url" : ["https://api.imgur.com/oauth2/authorize"]},
        {"site" : "salesforce", "url" : ["https://login.salesforce.com/services/oauth2/authorize"]},
        {"site" : "strava", "url" : ["https://www.strava.com/oauth/authorize"]},
        {"site" : "battle.net", "url" : ["https://us.battle.net/oauth/authorize"]}]
        k0 = re.compile('oauth', re.I)
        k1 = re.compile('openid', re.I)
        k2 = re.compile('log[\-\S]?[io]n', re.I)
        k3 = re.compile('sign[\-\S]?[io]n', re.I)
        k4 = re.compile('Sign\S?up', re.I)
        e0 = re.compile('social', re.I)
        e1 = re.compile('subscribe', re.I)
        e2 = re.compile('connect', re.I)
        e3 = re.compile('like', re.I)

        

        for each in sso:
            compiled = re.compile(each['site'], re.I | re.S)
            if compiled.search(inputstr) is not None:
                if k0.search(inputstr) is not None:
                    if len(each['url']) > 0:
                        for url in each['url']:
                            c_url = re.compile(url, re.I)
                            if c_url.search(inputstr) is not None:
                                if stype == 'login':
                                    if k2.search(inputstr) is not None or k3.search(inputstr) is not None:
                                        if each['site'] not in self.sso_info["loginSSO"]:
                                            self.sso_info["url"] = self.first_url
                                            self.sso_info["loginSSO"].append(each['site'])
                                elif stype == 'signup':
                                    if each['site'] not in self.sso_info["signupSSO"]:
                                        self.sso_info["url"] = self.first_url
                                        self.sso_info["signupSSO"].append(each['site'])
                    else:
                        if stype == 'login':
                            if k2.search(inputstr) is not None or k3.search(inputstr) is not None:
                                if each['site'] not in self.sso_info["loginSSO"]:
                                    self.sso_info["url"] = self.first_url
                                    self.sso_info["loginSSO"].append(each['site'])
                        elif stype == 'signup':
                            if each['site'] not in self.sso_info["signupSSO"]:
                                self.sso_info["url"] = self.first_url
                                self.sso_info["signupSSO"].append(each['site'])
                elif k1.search(inputstr) is not None:
                    if stype == 'login':
                        if k2.search(inputstr) is not None or k3.search(inputstr) is not None:
                            if each['site'] not in self.sso_info["loginSSO"]:
                                self.sso_info["url"] = self.first_url
                                self.sso_info["loginSSO"].append(each['site'])
                    elif stype == 'signup':
                        if each['site'] not in self.sso_info["signupSSO"]:
                            self.sso_info["url"] = self.first_url
                            self.sso_info["signupSSO"].append(each['site'])
        

    def write_to_file(self):
        for each in self.candidates:
            if not(len(each['loginSSO']) > 0 or len(each['signupSSO']) > 0):
                i = self.candidates.index(each)
                del self.candidates[i]
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
