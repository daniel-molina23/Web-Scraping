#Authors: Daniel Molina
#Assignment: Python Code Assignment
#Class: CS 3750-02
#Completed (or last revision): 02/25/2020


# =============================================================================
# This program looks for the cheapest prices on Ebay
# product target: GeForce 2080 Ti GPU
# condition: Brand New
# price search: below user's specified amount
# =============================================================================


from bs4 import BeautifulSoup
import requests


# url to be used from ebay search 'nvidia geforce rtx 2080 ti'
URL = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR8.TRC1.A0.H0.Xnvidia+geforce+rtx+2080+ti.TRS0&_nkw=nvidia+geforce+rtx+2080+ti&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=2080+ti'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

all_items = soup.find_all('li' ,class_ = 's-item')
# all_items: all the items listed on the webpage (50 total)



item_prices = []
brand_new_items = []

for item in all_items:
    if 'Brand New' in item.get_text(): # check if the product is brand new
        instance = item.find(class_='s-item__price').get_text()
        if '$' in instance: # check if item is money or text string
            money_value = float(instance.replace(',','').replace('$',''))
            # money_value: convert prices to float
            brand_new_items.append(item)
            item_prices.append(money_value)


# =============================================================================
# Now, Extract links for certain items cheaper than user's specified amount
# Present that information back to the user
# =============================================================================

max_price = input('What is the max price you are willing to pay for a Brand New \nNvidia Geforce RTX 2080 TI? ')

try:
    max_price = float(max_price)
    
    print('\n\nHere is what I found for prices lower than $%.2f:' % max_price)
    print('----------------------------------------------------------\n')
    
    
    items_found = False # if item found for price range
    item_links = [] # link for found items lower than max_price
    index = 0   # price index
    counter = 0 # number of Options available
    est_price = 0 # sum of prices
    
    # loop find links and prices of products lower than user's max_price
    for price in item_prices:
        if price <= max_price:
            est_price += price
            counter+=1
            print('Option #%d, Price $%.2f, link:' % (counter,price))
            link = brand_new_items[index].find(class_='s-item__link').get('href')
            # extract link for item under $800
            item_links.append(link)
            print(link, end='\n\n')
            items_found = True
        index += 1
    # end of for loop


    if (not items_found):
        print('Sorry .... Unfortunately I couldn\'t find anything cheaper than that.')
        print('Maybe come back for Black Friday?...')
    else:
        print('----------------------------------------------------------')
        print('Total Number of Options: %d, Average price found for results: $%.2f\n' % (counter, (est_price/counter)))
        print('Copy and paste your favorite link on the web for more information')
        print('----------------------------------------------------------\n')


except:
    print('That is not a valid price. Try Again.')


