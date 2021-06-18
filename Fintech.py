from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException
class crypto_arsenal_crawler():
    def __init__(self, email, pw):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values' :{'notifications' : 2}}
        options.add_experimental_option('prefs',prefs)

        self.__driver = webdriver.Chrome(executable_path='./chromedriver_win32/chromedriver.exe', options = options)    #開啟chrome browser
        self.__driver.maximize_window()
        self.__driver.get('https://crypto-arsenal.io/zh-tw/')
        
#         login = self.__driver.find_element_by_css_selector(".ftTQhZ") # login
        login = self.__driver.find_element_by_xpath("//button[text()='登入']")
        login.click()
        
        account = self.__driver.find_element_by_name("email")# id = "m_login_email"
        account.send_keys(email)
        pwd = self.__driver.find_element_by_name("password")
        pwd.send_keys(pw)
        sumbit = self.__driver.find_element_by_xpath("//button[@type='submit']")
        sumbit.click()
        
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".fxoTKw"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
            pass
        
        later = self.__driver.find_element_by_xpath("//button[text()='Later']")
        later.click()
        
    def openStrategySpace(self):
        url = 'https://crypto-arsenal.io/zh-tw/strategies' 
        self.__driver.get(url)
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".strategy_name"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
            pass
        strategies = self.__driver.find_elements_by_xpath("//span[@class='strategy_name']")
        BackTesting = self.__driver.find_elements_by_xpath("//button[text()='歷史回測']")
        return [i.text for i in strategies]
    def backtesting(self, name, start_date, end_date, exchange="BINANCE", pairs="BTC-USDT", amount=100000):
        print("Period:", start_date, end_date)
        start_date = start_date.split("/")
        end_date = end_date.split("/")
        url = 'https://crypto-arsenal.io/zh-tw/strategies' 
        self.__driver.get(url)
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".strategy_name"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
            
        self.strategies = self.__driver.find_elements_by_xpath("//span[@class='strategy_name']")
        self.BackTesting = self.__driver.find_elements_by_xpath("//button[text()='歷史回測']")
        ind = [i.text for i in self.strategies].index(name)
        print("Strategy"+name,":",ind)
        self.BackTesting[ind].click()
        
        # 回測區間
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".gIPudq"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
            
        tmp = self.__driver.find_element_by_css_selector(".gIPudq")
        
        tmp.click()
        # switching X月X年 (<)
        
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".rdrMonthName"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
        (self.__driver.find_element_by_xpath("//button[@class='rdrNextPrevButton rdrNextButton']")).click() # > first
        while(1):
            tmp = self.__driver.find_elements_by_css_selector(".rdrMonthName")
            s = tmp[0].text
            s = (s).replace(' ','').split('月')
            if s[0]==start_date[1] and s[1]==start_date[0]:
                break
            else:
                (self.__driver.find_element_by_xpath("//button[@class='rdrNextPrevButton rdrPprevButton']")).click() # <
        
        # switching X月X年 (>)
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".rdrDayNumber"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
        
        tmp = self.__driver.find_elements_by_xpath("//button[@type='button']//span[@class='rdrDayNumber']//span[text()="+start_date[2]+"]") 
        indices = [i for i, x in enumerate(tmp) if x.text == start_date[2]]
        tmp[indices[0]].click()
        
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".rdrMonthName"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
        while(1):
            tmp = self.__driver.find_elements_by_css_selector(".rdrMonthName")
            s = tmp[1].text
            s = (s).replace(' ','').split('月')
            if (int(s[0])>int(end_date[1]) and int(s[1])>=int(end_date[0])) or int(s[1])>int(end_date[0]):
                (self.__driver.find_element_by_xpath("//button[@class='rdrNextPrevButton rdrPprevButton']")).click() # <
                tmp = self.__driver.find_elements_by_css_selector(".rdrMonthName")
                s = tmp[1].text
                s = (s).replace(' ','').split('月')
            if s[0]==end_date[1] and s[1]==end_date[0]:
                break
            else:
                (self.__driver.find_element_by_xpath("//button[@class='rdrNextPrevButton rdrNextButton']")).click()
        
        tmp = self.__driver.find_elements_by_xpath("//button[@type='button']//span[@class='rdrDayNumber']//span[text()="+end_date[2]+"]") 
        indices = [i for i, x in enumerate(tmp) if x.text == end_date[2]]
        tmp[indices[-1]].click()
        self.__driver.find_element_by_xpath("//button[text()='確定']").click()
        
        # 交易所
        menu = self.__driver.find_elements_by_xpath("//div[@aria-label='open menu']")
        menu[0].click()
        
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.ID , "downshift-0-item-0")) # downshift-0-item-0
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
        tmp = self.__driver.find_elements_by_xpath("//div[@role='option']")
#         print(tmp[[i.text for i in tmp].index(exchange)])
        try:
            tmp[[i.text for i in tmp].index(exchange)].click()
        except:
            tmp = self.__driver.find_elements_by_xpath("//div[@role='option']")
            tmp[[i.text for i in tmp].index(exchange)].click()
        
        # 交易對
        menu[1].click()
        pairs = pairs.split('-')
        tmp = self.__driver.find_elements_by_xpath("//div[@role='option']")
        try:
            tmp[[i.text for i in tmp].index(pairs[0])].click()
        except:
            tmp = self.__driver.find_elements_by_xpath("//div[@role='option']")
            tmp[[i.text for i in tmp].index(pairs[0])].click()
        menu[2].click()
        tmp = self.__driver.find_elements_by_xpath("//div[@role='option']")
        tmp[[i.text for i in tmp].index(pairs[1])].click()
        
        # 投資金額
        tmp = self.__driver.find_element_by_xpath("//input[@name='balance']")
        tmp.clear()
        tmp.send_keys(str(amount))
        
        # button: 歷史回測
        self.__driver.find_element_by_xpath("//button[@data-test-id='launch-button-type-Backtest']").click()
        print("Backtesting start...")
        
    def rm_backtesting_records(self, name):
        url = 'https://crypto-arsenal.io/zh-tw/strategies' 
        self.__driver.get(url)
        try:
            element = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".strategy_name"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
        self.strategies = self.__driver.find_elements_by_xpath("//span[@class='strategy_name']")
        self.surface = self.__driver.find_elements_by_xpath("//div[@class='recharts-wrapper']")
        ind = [i.text for i in self.strategies].index(name)
        print("Strategy"+name,":",ind)
        self.surface[ind].click()
        
        # start removing 
        while(1):
            try:
                wait = WebDriverWait(self.__driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
                elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sc-gsWcmt hugEah']")))
            except:
                print("Waiting too long...")
                print("Sorry, I will shut down your driver!")
                break
            tmp = self.__driver.find_element_by_xpath("//button[@class='sc-gsWcmt hugEah']")
            try:
                tmp.click()
            except:
                tmp = self.__driver.find_elements_by_xpath("//button[@class='sc-gsWcmt hugEah']")
                if len(tmp)==0:
                    break
                else:
                    tmp[0].click()
            try:
                wait = WebDriverWait(self.__driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
                elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='確定']")))
            except:
                print("Waiting too long...")
                print("Sorry, I will shut down your driver!")
                break

            self.__driver.find_element_by_xpath("//button[text()='確定']").click()
        print("Done!")
    def get_backtesting_records(self, name):
        url = 'https://crypto-arsenal.io/zh-tw/strategies' 
        self.__driver.get(url)
        try:
            element = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR , ".strategy_name"))
        )
        except:
            print("Waiting too long...")
            print("Sorry, I will shut down your driver!")
        self.strategies = self.__driver.find_elements_by_xpath("//span[@class='strategy_name']")
        self.surface = self.__driver.find_elements_by_xpath("//div[@class='recharts-wrapper']")
        ind = [i.text for i in self.strategies].index(name)
        
        self.surface[ind].click()
        while(1):
            try:
                wait = WebDriverWait(self.__driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
                elem = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Load More']")))
            except:
                pass
            try:
                tmp = self.__driver.find_element_by_xpath("//button[text()='Load More']")
                tmp.click()
            except:
                tmp = self.__driver.find_elements_by_xpath("//button[text()='Load More']")
                if len(tmp)==0:
                    break
                else:
                    tmp[0].click()
        his = self.__driver.find_elements_by_css_selector('div.ioMpuH')[1:]
        return his
        
    def getDriver(self): # developer option
        return self.__driver