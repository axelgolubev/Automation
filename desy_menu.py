# The Selenium script is taking data from two canteens on the DESY campus and create a file with menu and prices.
# The data is collected once per day using cron jobs. 

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def scrape_cfel(file):
    '''Get the menu from CFEL cantine with prices'''
    cfel_URL = "https://www.stwhh.de/gastronomie/mensen-cafes-weiteres/mensa/cafe-cfel"
    driver.get(cfel_URL)
    time.sleep(5)
   
    # accept Cookies
    cookie_button = driver.find_element(By.CLASS_NAME, 'sg-cookie-optin-box-button-accept-all')
    cookie_button.click()
    time.sleep(2)
    
    # open the prices sections
    buttons = driver.find_elements(By.CLASS_NAME, 'togglebutton--top')
    for button in buttons:
        button.click()
        time.sleep(2)
    
    # Scrape Dishes
    main = driver.find_elements(By.CLASS_NAME, 'singlemeal__top')
    cfel_dishes = []
    for content in main:
        current_dish = content.text 
        cfel_dishes.append(current_dish[:-3])
    print(cfel_dishes)

    # Scrape Prices
    time.sleep(3)
    price = driver.find_elements(By.XPATH, "//span[@class='singlemeal__info']")
    cfel_prices_students = []
    cfel_prices_normal = []
    for content in price:
        if 'Studierende' in content.text:
            print(content.text)
            cfel_prices_students.append(content.text)
        elif 'Bedienstete' in content.text:
            print(content.text)
            cfel_prices_normal.append(content.text)
    print(cfel_prices_students)
    print(cfel_prices_normal)

    # Piece all together and print to the file
    for dish, price_students, price_normal in zip(cfel_dishes, cfel_prices_students, cfel_prices_normal):
        file.write(dish + price_students  + '\n' + price_normal + '\n'+ '\n')


def scrape_desy(file):
    '''Get the menu from DESY cantine with prices'''
    desy_URL = "https://desy.myalsterfood.de/#!"
    driver.get(desy_URL)
    time.sleep(5)
    dishes = driver.find_elements(By.XPATH, "//div[@class='min-height-rem2-5']")
    prices = driver.find_elements(By.XPATH, "//div[@class='price-text']")
    desy_prices = []
    desy_dishes = []
    for dish in dishes:
        if dish.text != '':
            print(dish.text)
            desy_dishes.append(dish.text)
    for price in prices:
        if price.text != '':
            print(price.text)
            desy_prices.append(price.text)
    print(desy_dishes)
    print(desy_prices)

    for dish, price in zip(desy_dishes, desy_prices):
        file.write(dish + '\n' + price  + '\n' + '\n')

    
options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

with open('scraped_data.txt', 'w') as f:
    f.write('CFEL...\n')
    scrape_cfel(f)
    f.write('DESY...\n')
    scrape_desy(f)
    driver.quit()
