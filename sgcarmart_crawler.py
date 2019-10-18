from bs4 import BeautifulSoup
import datetime 
import time 
import urllib 
import requests
import random 
import json 

# Function to make soup object
def make_soup(url):
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    read_html = html.read()
    soup = BeautifulSoup(str(read_html, "utf-8"), "html5lib")
    return soup

# Get start time with current date and time 
start_time = datetime.datetime.utcnow()

new_cars_url = "https://www.sgcarmart.com/new_cars/index.php"
web = "https://www.sgcarmart.com/new_cars/"

new_cars_soup = make_soup(new_cars_url)

# next_line = new_cars_soup.find_all(name="div", class_="floatleft")
new_cars_exts = new_cars_soup.select("div.floatleft > a")

car_list = []

# Get the url of each car brand 
new_cars_url_list = []
for ext in new_cars_exts:
    new_cars_url_list.append(web + ext.get('href'))
new_cars_url_list = new_cars_url_list[4:55]

for url in new_cars_url_list:
    sleep_time = random.randint(1,5)
    print(f'Sleeping time {sleep_time}s')
    time.sleep(sleep_time)
    print("crawling brand: ", url)

    brand = url[url.find("=")+1:]

    current_brand_soup = make_soup(url)
    links = current_brand_soup.find_all('div', attrs={'style': 'margin-right:5px;', 'class': 'floatleft'})

    # Get the url for each car from the brand
    for link in links:

        car_dict = {}

        car_link = web + link.find('a').get('href')

        print("crawling model: ", car_link)

        # Create another soup object 
        current_car_soup = make_soup(car_link)
        tabs = current_car_soup.find(name="div", id="submenu")
        tabs_list = tabs.select("ul > li")
        #price = current_car_soup.find(name="div", class_="grayboxborder")
        price = current_car_soup.find(name='span', class_='font_bold')
        price = price.get_text()

        # get review url 
        review_url = web + tabs_list[4].find('a').get('href')
        
        review_soup = make_soup(review_url)

        car = review_soup.find_all('div', attrs={'style': 'width:445px;height:35px;float:left;overflow:hidden;'})
        car_name = car[0].get_text()

        user = review_soup.find_all('td', attrs={'style': 'padding-top:4px;'})
        if len(user) > 1:
            user = user[0].find('strong')
            user_name = user.text
            car_dict['user_name'] = user_name

        review = review_soup.find_all('p', attrs={'style': 'padding-top:15px'})
        if len(review) > 1:
            review = review[0].get_text()
            car_dict['review'] = review

        car_dict['car_name'] = car_name
        car_dict['brand'] = brand
        car_dict['price'] = price
        car_list.append(car_dict)
        
    with open('./SGC_data/%s.json' % brand, 'w') as file:
        json.dump(car_list, file, indent=4, sort_keys=False)
    end_time = datetime.datetime.utcnow()
    print("Total time taken (mins): " +str(((end_time-start_time).total_seconds() / 60)))
        





