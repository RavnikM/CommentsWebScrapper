from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re
import csv

driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920x1080")

url = 'https://www.rtvslo.si/svet/evropa/jansa-fiala-in-morawiecki-ob-19-uri-z-zelenskim-ki-izgublja-upanje-na-clanstvo-ukrajine-v-natu/615722'
driver.get(url)

elem = driver.find_element(by=By.CLASS_NAME, value='btn-show-comments')
elem.send_keys(Keys.RETURN)


pagination_cont = driver.find_element(By.CSS_SELECTOR,'#appcomments > main > div > div:nth-child(4)')
pagination_elems = pagination_cont.find_elements(By.CLASS_NAME, 'page-item')

comment_data = []
#for pagination_elem in pagination_elems:
for x in range(len(pagination_elems) - 1):
    if pagination_elems[x].text.isnumeric():
        pagination_elems[x].click()
        element_present = EC.invisibility_of_element_located((By.CLASS_NAME, 'loader'))
        WebDriverWait(driver, 10).until(element_present)

        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'comment'))
        WebDriverWait(driver, 10).until(element_present)

        comments_elems = driver.find_elements(by=By.CLASS_NAME, value='comment')
        for comment_web_elem in comments_elems:
            try:
                print(comment_web_elem.text)
                _text = comment_web_elem.text
                _text = _text.splitlines()
                _text[1] = _text[1].replace('# ', '')
                username = _text[0]
                date = datetime.strptime(_text[1], '%d. %m. %Y, %H:%M')
                # če vrne regex rezultat potem je v tej vrstici "{št komentarjev} {zvezdice}" sicer je username komentatorja na na kateraga post odgovarja
                # to pomeni da je naslednja vrstica kometar
                rx_res = re.match('^[0-9]{1,6} [0-9]{1,6}$', _text[3])

                comment =
                record = [username, date, comment]
                comment_data.append(record)
            except:
                pass

