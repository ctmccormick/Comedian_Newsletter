from selenium import webdriver
from time import sleep
from datetime import datetime

today = datetime.today().strftime("%A")

if today == 'Tuesday':

    driver = webdriver.Chrome(executable_path='chromedriver.exe')

    driver.get("http://pythonanywhere.com/login/?next=/")

    sleep(1)

    user = driver.find_element_by_name("auth-username")
    user.send_keys(username)

    pwd = driver.find_element_by_name("auth-password")
    pwd.send_keys(password)

    pwd.submit()

    sleep(1)

    driver.get("https://www.pythonanywhere.com/user/ctmccorm/files/home/ctmccorm/improv/templates")

    sleep(1)

    driver.find_element_by_name("file").send_keys("wiki_data_bdays.json")
    driver.find_element_by_name("file").send_keys("wiki_data_ddays.json")
    driver.find_element_by_name("file").send_keys("news_dump.json")

    sleep(2)

    driver.get("https://www.pythonanywhere.com/user/ctmccorm/webapps/#tab_id_ctmccorm_pythonanywhere_com")

    sleep(1)

    reload = driver.find_element_by_class_name("btn.btn-large.btn-success")
    reload.click()

    sleep(10)

    driver.quit()

else:
    pass
