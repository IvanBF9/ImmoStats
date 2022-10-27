from selenium import webdriver
from selenium.webdriver.common.by import By
from db.database import DataBase
import sqlalchemy as db
import numpy as np
import pandas as pd
import time
import random

BASE_URL = 'https://opensea.io/assets?search[resultModel]=ASSETS&search[paymentAssets][0]=ETH&search[categories][0]=photography-category'

base = DataBase()

base.create_table('nfts',
        img = db.String,
        title = db.String,
        author = db.String,
        eth_price = db.String,
    )

    #add_row

def scrap_open_sea(max):
    max += 1
    # Get driver
    DRIVER_PATH = './chromedriver'
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(BASE_URL)

    time.sleep(random.uniform(4, 5))

    len_px = 10

    containers = []
    content = []

    for z in range(1,max):
        containers.append(driver.find_elements(By.TAG_NAME, 'article'))
        
        if z != 1:
            temp = driver.find_elements(By.TAG_NAME, 'article')
            containers[z-1] = [i for i in temp if i not in containers[0]]
            
        while len(containers[z-1]) < 150:
            
            driver.execute_script(f'window.scrollTo(0,{len_px})')
            len_px+=40
            
            if z != 1:
                temp = driver.find_elements(By.TAG_NAME, 'article')
                containers[z-1] = [i for i in temp if i not in containers[0]]
            else:
                containers[z-1] = driver.find_elements(By.TAG_NAME, 'article')

        # Wait loading of images
        time.sleep(random.uniform(4, 5))
        
        if z != 1:
            temp = driver.find_elements(By.TAG_NAME, 'article')
            containers[z-1] = [i for i in temp if i not in containers[0]]
            for item in containers[z-1]:
                containers[0].append(item)
        else:
            containers[z-1] = driver.find_elements(By.TAG_NAME, 'article')

        content.append([
            {
                'img' : containers[z-1][i].find_element(By.TAG_NAME, 'img').get_attribute('src'),
                'title' : containers[z-1][i].find_element(By.CSS_SELECTOR, 'a > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').text,
                'author' : containers[z-1][i].find_element(By.CSS_SELECTOR, 'a > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > div:nth-child(1) > div:nth-child(1)').text,
                'eth_price' : containers[z-1][i].find_element(By.CSS_SELECTOR, 'a > div:nth-child(3) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)').text
            }
            for i in range(100)
        ])

    # Concat lists
    _data = np.concatenate(content)

    # Adding to database

    nft_dataframe = pd.DataFrame(columns=['img', 'title', 'author', 'eth_price'])

    for nft in _data:
        nft_dataframe = nft_dataframe.append(nft, ignore_index=True)
        base.add_row('nfts',
            img = nft['img'],
            title = nft['title'],
            author = nft['author'],
            eth_price = nft['eth_price'],
        )
    
    nft_dataframe.to_csv('nfts.csv', index = False, encoding='utf-8')