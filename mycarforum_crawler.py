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

# Function to find next page url for pagination 
def find_next_page(soup_object):
    next_page = soup_object.find(name='li', class_='ipsPagination_next')
    next_page = next_page.select('a')
    next_page_url = next_page[0].get('href')
    next_page_no = int(next_page_url[next_page_url.find("page=") + 5:])
    return next_page_no, next_page_url

# Function to retrieve all the thread content
def make_thread_object(thread_soup):
    # accessing soup object 
    page = thread_soup.select('main.ipsLayout_container > div > div > div > div')
    thread_page = page[2]
    all_thread = thread_page.find("div", {"id": "elPostFeed"})

    # Get all the userid URL from the href tag
    userid_url = all_thread.select('article > div > h3 > a')
    comment_url = all_thread.find_all(name='div', class_='ipsType_normal ipsType_richText ipsContained')
    return userid_url, comment_url, thread_page

# Get start time with current date and time 
start_time = datetime.datetime.utcnow()

# url for the thread to crawl 
thread_url_list = ["https://www.mycarforum.com/forums/topic/2715945-mercedes-amg-most-powerful-4-cylinders-engine/",
              "https://www.mycarforum.com/forums/topic/2703413-mercedes-owners-thread/",
              "https://www.mycarforum.com/forums/topic/2668830-new-2nd-generation-mercedes-b-class/",
              "https://www.mycarforum.com/forums/topic/2699114-mercedes-glc/",
              "https://www.mycarforum.com/forums/topic/2717175-2019-mercedes-benz-glb-x247/",
              "https://www.mycarforum.com/forums/topic/2709111-2020-mercedes-benz-maybach-gls-x167/"]

for thread_url in thread_url_list:
    # set counter to track crawling  progress
    count = 1

    # Create comment list to store the crawled data 
    comment_list = []

    topic = thread_url[thread_url.find("topic/") + 6:-1]
    print("Start crawling from", topic)

    # Request from url and convert to BeautifulSoup Object
    thread_soup = make_soup(thread_url)
    userid_url, comment_url, thread_page = make_thread_object(thread_soup)
    next_page_no, next_page_url = find_next_page(thread_page)

    # Find the last page url to stop the loop
    last_page = thread_page.find(name='li', class_='ipsPagination_last')
    last_page = last_page.select('a')
    last_page_url = last_page[0].get('href')
    last_page_no = int(last_page_url[last_page_url.find("page=") + 5:])

    while (next_page_no <= last_page_no):

        sleep_time = random.randint(1,7)
        print(f'Sleeping time {sleep_time}s')
        time.sleep(sleep_time)
        print('Crawling page:', count, 'of', last_page_no)

        # Storing into dictionary 
        for i in range(len(userid_url)):
            comment_dict = {}
            comment_dict['userid'] = userid_url[i].get_text()
            comment_dict['comment'] = comment_url[i].get_text()
            comment_list.append(comment_dict)

        next_page_no, next_page_url = find_next_page(thread_page)
        thread_soup = make_soup(next_page_url)
        userid_url, comment_url, thread_page = make_thread_object(thread_soup)
        count += 1

    with open('./data/%s.json' % topic, 'w') as file:
        json.dump(comment_list, file, indent=4, sort_keys=False)
    end_time = datetime.datetime.utcnow()
    print("Total time taken (mins): " +str(((end_time-start_time).total_seconds() / 60)))