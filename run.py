from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from argparse import ArgumentParser
from random import randint
import sys, time

SIGNIN = 0
SIGNOUT = 1

class AutoLogin:
    def __init__(self, username, password):
        self.browser = webdriver.Chrome(executable_path='./chromedriver-linux')
        self.uname = username
        self.psswd = password

    def login2page(self):
        self.browser.get( 'https://my.ntu.edu.tw/attend/ssi.aspx' )
        LogInPageButton = self.browser.find_element_by_class_name( 'btn-info' )
        LogInPageButton.click()

        uname = WebDriverWait( self.browser, 10 ).until(
                    EC.presence_of_element_located(
                            (By.NAME, 'user')
                        )
                    )
        uname.send_keys( self.uname )

        psswd = self.browser.find_element_by_name( 'pass' )
        psswd.send_keys( self.psswd )

        SubmitButton = self.browser.find_element_by_name( 'Submit' )
        SubmitButton.click()

class CheckIn(AutoLogin):
    def __init__(self, username, password):
        super().__init__(username, password)

    def signIn(self):
        self.login2page()
        time.sleep( 2 )
        signInButton = self.browser.find_element_by_id( 'btSign' )
        signInButton.click()
        self.browser.quit()

class CheckOut(AutoLogin):
    def __init__(self, username, password):
        super().__init__(username, password)

    def signOut(self):
        self.login2page()
        time.sleep( 2 )
        signOutButton = self.browser.find_element_by_id( 'btSign2' )
        signOutButton.click()
        self.browser.quit()

def parse():
    parser = ArgumentParser()
    parser.add_argument('--username', type=str, required=True, help='username')
    parser.add_argument('--password', type=str, required=True, help='password')
    return parser.parse_args()

# returns time difference in second
def dffTime(cur, ref):
    # cur has to be less than ref
    tmp = list(ref)
    if tmp[2] < cur.tm_sec:
        tmp[2] += 60
        tmp[1] -= 1
    if tmp[1] < cur.tm_min:
        tmp[1] += 60
        tmp[0] -= 1
    if tmp[0] < cur.tm_hour:
        tmp[0] += 24
    return tmp[2]-cur.tm_sec + 60*(tmp[1]-cur.tm_min) + 3600*(tmp[0]-cur.tm_hour)

if __name__ == '__main__':
    args = parse()
    stat = SIGNIN
    action = ['signIn', 'signOut']
    wday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    refTime = [8, randint(0, 20), randint(0, 59)]


    while True:
        sleepTime = dffTime( time.localtime(), refTime )
        print ('{} at {:02d}:{:02d}:{:02d}, sleeping for {}s'.format(action[stat], refTime[0], refTime[1], refTime[2], sleepTime))
        time.sleep(sleepTime)
        curTime = time.localtime()
        print ('[current time] {}'.format(time.strftime("%H:%M:%S", curTime)))
        if curTime.tm_wday == 5 or curTime.tm_wday == 6:
            print ('It is {}, waiting till tomorrow'.format(wday[curTime.tm_wday]))
            time.sleep(2)
            continue

        if stat == SIGNIN:
            cin = CheckIn( args.username, args.password )
            cin.signIn()
            stat = SIGNOUT
            refTime = [17, refTime[1]+randint(0, 10), randint(0, 59)]

        if stat == SIGNOUT:
            cout = CheckOut( args.username, args.password )
            cout.signOut()
            stat = SIGNIN
            refTime = [8, randint(0, 20), randint(0, 59)]
