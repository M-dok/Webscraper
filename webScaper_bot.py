import json
import csv
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException, ElementNotInteractableException, StaleElementReferenceException
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


class WebBot:
    def __init__(self, url, email, password):
        # Class Attributes
        self._url = url #The url for the website
        self._email = email#email for login 
        self._password = password#password for login
        self.proxies = ["List of proxy IPs to avoid automation detection"]

        self._page = 1 #page number that program is currently on 

        # Set up Chrome options
        self.chrome_options = Options()

        # Enables logging for Chrome, which can be helpful for troubleshooting by providing detailed information about browser operations.
        self.chrome_options.add_argument("--enable-logging")

        # Disables Blink features related to automation control to reduce detection as an automated browser. This can help in avoiding bot detection.
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Sets the Accept-Encoding heatarget_url to gzip and deflate to compress the response data, which can improve performance.
        self.chrome_options.add_argument("--accept-encoding=gzip, deflate")

        # Disables the search engine choice screen, which prevents the browser from displaying the search engine setup page after installation.
        self.chrome_options.add_argument("--disable-search-engine-choice-screen")

        #Starts the browser window in max
        self.chrome_options.add_argument("--start-maximized")

        # Allows the ChromeDriver to continue running after the script finishes, keeping the browser open for manual inspection or debugging.
        self.chrome_options.add_experimental_option("detach", True)

        # "excludeSwitches": ["enable-automation"] - Prevents the "Chrome is being controlled by automated test software" banner from being displayed.
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        #"useAutomationExtension": False - Disables the use of the Chrome automation extension, which can make the browser more easily detectable as being automated.
        self.chrome_options.add_experimental_option('useAutomationExtension', False)


        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        self.chrome_options.add_argument(f"user-agent={user_agent}")

        # Set Accept-Language and Referer
        self.chrome_options.add_argument("accept-language=en-US,en;q=0.9")
        #self.chrome_options.add_argument("--auto-open-devtools-for-tabs")
    
        # Initialize WebDriver
        proxy = random.choice(self.proxies)
        
        self.browser = webdriver.Chrome(options=self.chrome_options,seleniumwire_options={'enable_har': True,
                                                                                          'disable_encoding': True,     
                                                                                          'connection_timeout': None,
                                                                                          'suppress_connection_errors': False,
                                                                                          
                                                                                                            })
        #Add this code to the seleniumwire_options to use proxies (optional)
        '''"proxy":{
                                                                                              "http":proxy,
                                                                                              "https":proxy
                                                                                          }'''

        self.action = ActionChains(self.browser) #Initialise ActionChain object 
                                                #Allows you to create complex user interactions, like mouse movements, clicks, keyboard actions, and other events.
    
    #This method takes the url given in the class attributes and goes to the website 
    def open_site(self):
        try:
            self.browser.get(self._url)  # Attempt to open the site
            for cookie in self.browser.get_cookies():
                self.browser.add_cookie(cookie)
    
        
        except Exception as e:
            print(f"Failed to open site with proxy {self.browser.proxy}: {e}")
            self.close_browser()  # Close the current browser instance


        
    #This method is used to accept cookies on the website 
    def accept_cookies(self): #Clicks button accepting cookies 
        try:
            time.sleep(random.uniform(3,10)) #These random pauses in the program are attempts to "simulate" human behaviour to avoid any automation detection tools of the website 
            accept_cookies_button = WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "[[ XPATH of accept cookies button ]]")) #Waits 5s to find a clickable element with matching XPATH. Will fail if not found in time frame
            ) #Is a conditional that waits 5 sec for an element that is clickable with matching XPATH provided 
            
            accept_cookies_button.click()#Clicks element 
            

            # Loop through all the cookies currently stored in the browser session
            # For each cookie retrieved by self.browser.get_cookies(), add it back to the browser session using add_cookie()
            # This might be done to ensure that all cookies are re-added or persisted between different browsing sessions   
            for cookie in self.browser.get_cookies():
                self.browser.add_cookie(cookie)
    
        except Exception as e:
            print("No cookie button found:", e)
            self.close_browser()

    def login(self):#Presses login button
        try:
            login_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-password-login/div/div/app-login-form/div/div[1]/div/div[2]/form/p/app-basic-button/button"))
            )
            login_button.click()
        except Exception as e:
            print("Login button not found:", e)
            self.close_browser()
    
    def enter_email(self):#enters in email into the email form 
        try:
            time.sleep(random.uniform(3,10))
            email_form = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located((By.ID, "email"))
            )# waits will it finds email form
            email_form.send_keys(self._email) #Types email into email form
            time.sleep(random.uniform(1,10))
            self.login() #used to press the login button, submitting the information 

        except Exception as e:
            print("Couldn't enter email:", e)
            self.close_browser()

    def enter_password(self):#enters in password into password field 
        try:
            time.sleep(random.uniform(3,10))
            password_form = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            password_form.send_keys(self._password) #Types password into password form
            self.login()

        except Exception as e:
            print("Couldn't enter password:", e)
            self.close_browser()

    #This method goes to the nav bar to click a link 
    # that brings us to the list attendees at the event
    def access_attendees(self): #Goes to attendees list 
        try:
            
            time.sleep(random.uniform(3,10))
            nav = WebDriverWait(self.browser,15).until(
                EC.element_to_be_clickable((By.XPATH,'//*[@id="main-container"]/div/app-home/app-home-feed/div/div[2]/div[3]/div[2]/div/div'))
            )#finds the link 
            self.action.move_to_element(nav).click().perform()
            time.sleep(random.uniform(5,10))
            self.extract_specific_request_data()
            
        except Exception as e:
            print("Navigation error:",e)
            self.close_browser()
  
    def load_more(self):
        try:
            time.sleep(random.uniform(3,10))
            load_more_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "[[ XPATH of button to load more ]]"))
            )# finds a clickable element that has matching XPATH 
           
            self.action.move_to_element(load_more_button).click().perform()   #Uses action chain to move to element and click it to load more names to list 
            
        except TimeoutError as e:
            print("'Load More' button not found:", e)
            input("program failed") #Pauses program for debugging purposes 

        except (NoSuchElementException, TimeoutException) as e:
            print("End of Content")
            self.close_browser()
    
        self.browser.implicitly_wait(10)    
        time.sleep(random.uniform(5,15))
        self.extract_specific_request_data() 


    # Goes through the HAR file of this browser session
    # and searches for the request URL of the targeted data from network request made by the browser  
    def extract_specific_request_data(self):
        try:
            # The base part of the target URL without the 'page' parameter
            target_url = "[[ request URL of data to be examined ]]"
            found = False
            print("Starting search")

            #Iterates through requests made by the browser 
            for request in self.browser.requests:
                if request.response and request.response.status_code == 200:  # Check if the response is valid
                    # Check if the base URL is in the request URL
                    if target_url ==  request.url:
                        # Log the request URL for debugging purposes
                        print(f"Found URL: {request.url}")
                        
                        data = json.loads(request.response.body.decode("utf-8"))  # Convert the response body to JSON
                        with open("data.json", "w") as outfile:
                                print("Data Transfer")
                                found = True
                                json.dump(data, outfile, indent=4)
                        break  # Stop the search once the correct request is found
            
            if found == False:
                print("data isn't in HAR")
                self.close_browser()
            else:
                self._page += 1  # Increment the page number for the next request. This is used for an f string to create the request url for next page of data
                print("page number: ",self._page)
                self.write_data_csv()

        except json.JSONDecodeError as e:
            print("Error in finding data:", e)
            # self.close_browser()  # Close the browser if an error occurs


    #Extracts data that was placed in data.json 
    # And extracts relevant info and places it into a csv file 
    def write_data_csv(self):
        with open('data.json', 'r',encoding='utf-8') as openfile: #Opens data from 'data.json'
            json_object = json.load(openfile) #Places data into json_object

        fields = ["Name","Company","Title","Location", "Exhibitor/Attendee"] #fields in csv file 
        rows =[] #Stores the data in rows 
        #iterates through data and places all the relevant info into rows array 
        for entry in json_object["data"]:
            data = {}
            data["Name"] = entry["name"]
            data["Company"] = entry["company_name"]
            data["Title"] = entry["job_title"]
            data["Location"] = entry["location"]
            data["Exhibitor/Attendee"] = entry["type_key_translation"]
            rows.append(data)

        try:
            filename = "attendee_records.csv" 
            with open(filename,"a",newline='',encoding='utf-8') as csvfile: #Places the data into a csv file 
                # creating a csv writer object
                writer  = csv.DictWriter(csvfile,fieldnames=fields)
                # writing the fields
                if csvfile.tell() == 0:
                    writer.writeheader()
                # writing the data rows
                writer.writerows(rows)
            
            time.sleep(random.uniform(3,15))
            self.load_more() #Pressed to load more content 
        
        except FileExistsError as e:
            print("File not found: ", e)
        except json.JSONDecodeError as e:
            print("Error decoding JSON: ", e)
        except Exception as e:
            print("An error occurred: ", e)
        



    def close_browser(self):
        try:
            if self.browser:
                self.browser.quit()
                print("Browser closed")
        except Exception as e:
            print("Error quitting browser:", e)

    
    def har_data(self):
        har_data = self.browser.har  # This contains all HTTP transactions
        
        #Write the HAR data to a file in a readable format
        with open('har_data.json', 'w') as har_file:
            har_data = json.loads(har_data)
            json.dump(har_data, har_file, indent=4)

        print("HAR is gone to data.json")






if __name__ == "__main__":
    # Example usage
    email = "*********"
    password = "*********"
    url = "[[ Website URL ]]"
    bot = WebBot(url, email, password)
    bot.open_site()
    time.sleep(5)  # Adjust sleep time as needed or use explicit waits instead
    bot.accept_cookies()
    bot.login()
    bot.enter_email()
    bot.enter_password()
    bot.access_attendees()
   
    input("End the program: ")  #Pauses Program for debugging use only 
   
    bot.close_browser()
