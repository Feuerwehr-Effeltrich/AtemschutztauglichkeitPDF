from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from os import getenv, getcwd, listdir, path, remove
from time import sleep

def iterate_pdf(callback):
    for item in listdir(getcwd()):
        if item.endswith('.pdf'):
            callback(item)

# user and pass can also be passed as environment in docker
if not (getenv('FW_USER') and getenv('FW_PASS')):
    from dotenv import load_dotenv
    load_dotenv()

# read environment
username = getenv('FW_USER')
password = getenv('FW_PASS')
assert username and password
print('Retrieved username and password')

# configure firefox
profile = webdriver.FirefoxOptions()
profile.add_argument('--headless')
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', getcwd())

# open website
driver = webdriver.Firefox(options=profile)
driver.get('https://live.fwportal.de/')
print('Opened FWPortal')

# login
username_field = driver.find_element(By.ID, 'UserName')
username_field.send_keys(username)
password_field = driver.find_element(By.ID, 'Password')
password_field.send_keys(password)
login_button = driver.find_element(By.ID, 'GENERIC_ID_0_btn_submit')
login_button.click()
print('Sent login request')

# wait for full login
wait = WebDriverWait(driver, 10)
wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '.fwportal-ui-button-caption')))
print('Login done')

# get pdf and close browser
driver.execute_script(f'window.open("/Atemschutz/TauglichkeitAsPdf","_blank");')
pdf = ''
def cb(item):
    global pdf
    pdf = path.join(getcwd(), item)
while not pdf:
    iterate_pdf(cb)
    sleep(1)
driver.close()
print('Got pdf')

# print
# TODO
print('Printed pdf')

# clean
iterate_pdf(lambda item: remove(path.join(getcwd(), item)))
print('Cleaned workdir')

