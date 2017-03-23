or k1.search(inputstr) is not None:
                    if stype == 'login':
                        if k2.search(inputstr) is not None or k3.search(inputstr) is not None:
                            if each.site not in self.sso_info["loginSSO"]:
                                self.sso_info["loginSSO"].append(each)
                                print "2"
                    elif stype == 'signup':
                        if k4.search(inputstr) is not None:
                            if each.site not in self.sso_info["signupSSO"]:
                                self.sso_info["signupSSO"].append(each)
                else:
                    if e0.search(inputstr) is not None or e1.search(inputstr) is not None or e2.search(inputstr) is not None or e3.search(inputstr) is not None:
                        print "6"


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
