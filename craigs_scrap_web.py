#this file will hold all of the functions for scraping info from craigslist
import urllib.request
from bs4 import BeautifulSoup
import datetime
import json
#now put it all together in dict data format.

#get the post ID for item
def get_post_id(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.find_all("p",{'class': 'postinginfo'})
    data = data[1]
    string = str(data.getText())
    return string.replace("post id: ", "")

#get description of product
def get_description(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.find("section",{'id': 'postingbody'})
    string = str(data.getText())
    return string.replace("QR Code Link to This Post","")

#get price of product
def get_price(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.find("span",{'class': 'price'})
    check = str(data)
    if check == "None":
        return "please see listing"
    else:
        string = str(data.getText())
        return string

#get the post date of item
def get_post_date(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    post_time = soup.find("time").get('datetime')
    time = post_time.replace("T"," ")
    time = time.replace("-0600", "")
    return time

#get the update date and item
def get_update_date(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    update_time = soup.find_all("time")
    if len(update_time) > 2:
        update_time = update_time[2].get('datetime')
        time = update_time.replace("T"," ")
        time = time.replace("-0600", "")
        return time
    else:
        return get_post_date(url)

#get the name of the product
def get_name(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = soup.find("span",{'id': 'titletextonly'})
    string = str(data.getText())
    return string

#get img of product (just 1 img)
def get_img(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    data = str(soup.find("img").get("src"))
    return data
