from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

class AutoCheckInNOut:
    def __init__(self):
        self.browser = None

    def signIn(self):
        self.restartDriver()
        self.login2page()
        signInButton = self.browser.find_element_by_id( 'btSign' )
        signInButton.click()
        self.quitDriver()

    def signOut(self):
        self.restartDriver()
        self.login2page()
        signOutButton = self.browser.find_element_by_id( 'btSign2' )
        signOutButton.click()
        self.quitDriver()

    def restartDriver(self):
        self.browser = webdriver.Chrome(executable_path='./chromedriver-mac')

    def quitDriver(self):
        self.browser.quit()

    def login2page(self):
        self.browser.get( 'https://my.ntu.edu.tw/attend/ssi.aspx' )
        LogInPageButton = self.browser.find_element_by_class_name( 'btn-info' )
        LogInPageButton.click()

        uname = WebDriverWait( self.browser, 10 ).until(
                    EC.presence_of_element_located(
                            (By.NAME, 'user')
                        )
                    )
        uname.send_keys( USERNAME )

        psswd = self.browser.find_element_by_name( 'pass' )
        psswd.send_keys( PASSWORD )

        SubmitButton = self.browser.find_element_by_name( 'Submit' )
        SubmitButton.click()

if __name__ == '__main__':
    bot = AutoCheckInNOut()
