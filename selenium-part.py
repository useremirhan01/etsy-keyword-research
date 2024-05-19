from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
import time

"""
1-etsy'ye giriş yapacak✅
2-ürün aratacak✅
3-en alakali 5(inp) ürünü alacak✅
4-ürünün başliklarini, açiklamalarini ve fiyatini alacak column şeklinde yapacak✅
5-fiyatin başlik uzunluğu ile fiyati arasindaki ilişkiyi gösteren tablo hazirlayacak✅
6- bu bir program şeklinde olacak
"""


def get_id(num,browser,list):
    try:
        # Use WebDriverWait to ensure the elements are loaded
        elements = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-listing-id]"))
        )
        # Iterate over the first 5 elements and print their data-listing-id attributes
        for element in elements[:num]:  # Slicing to get the first 5 elements
            listing_id = element.get_attribute("data-listing-id")
            print(listing_id)
            list.append(listing_id)
            
    except Exception as e:
        print("Error:", e)

def get_prices(values,currency_symbol):
    for value in values[:5]: #prints values of prdoucts that showed
        print(value.text + currency_symbol.text)
        price_list.append(value.text)
        symbol_list.append(currency_symbol.text)    
    
def get_titles(titles):
    count_number = 0
    bef_title = str
    for title in titles: #prints titles of prdoucts that showed
        if title.text == "Most Loved":
            pass
        else:
            if count_number < 5:
                if title.text != bef_title:
                    bef_title = title.text
                    print(title.text + "\n")
                    title_list.append(title.text)
                    count_number += 1

browser = webdriver.Firefox()

browser.get("https://www.etsy.com/?ref=lgo")

time.sleep(3)

searchArea = browser.find_element(By.XPATH, "/html/body/div[2]/div/header/div[2]/div/form/div/div[1]/input") # search area object
searchButton = browser.find_element(By.XPATH, "/html/body/div[2]/div/header/div[2]/div/form/div/div[1]/button[2]")



searchArea.send_keys("taylor tshirt")
searchButton.click()


titles = browser.find_elements(By.TAG_NAME, 'h3') #title scrapy
currency_values = browser.find_elements(By.CSS_SELECTOR, 'span.currency-value') #value scraper
currency_symbol = browser.find_element(By.CSS_SELECTOR, 'span.currency-symbol')#symbol scraper
id_list : List[str] = []
price_list : List[str] = []
symbol_list : List[str] = []
title_list : List[str] = []
get_id(5,browser,id_list)
get_titles(titles)
get_prices(currency_values),currency_symbol


    

    
    
df = pd.DataFrame({
    'title': np.array(title_list, dtype=str),
    'price': np.array(price_list, dtype=str),
    'id': np.array(id_list, dtype=str),
    'symbol': np.array(symbol_list, dtype=str)
})

df['title_length'] = df['title'].apply(len)
df['price_integer'] = df['price'].apply(float)


print(df)


plt.figure(figsize=(10, 5))  # Set the figure size
plt.scatter(df['title_length'], df['price_integer'], color='blue')  # Plot data points

# Adding title and labels
plt.title('Relationship Between Title Length and Price')
plt.xlabel('Length of Title')
plt.ylabel('Price')

# Show the plot
plt.grid(True)
plt.show()

plt.savefig('relationship btween price and length.png')
df.to_csv('products.csv')
    

        

time.sleep(5)
browser.quit()