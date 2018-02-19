import urllib.request
from bs4 import BeautifulSoup
import datetime
import json
import craigs_scrap_web 

search = input('What are you looking for? ')
city = input('what city are you looking in? ')
hour = int(input('how many hours old? '))

#open file and set to write
f = open("testfile.txt","w")

#format for datetime
dateFormat = '%Y-%m-%d %H:%M:%S'

#get current time
current_time =datetime.datetime.now()

#time different per customer request.
check_time = current_time - datetime.timedelta(hours=hour);

#msin dictonary object. will hold both recent and all links for said product search.
json_object = {}

#string replacement for url
city = city.replace(" ","")
search = search.replace(" ", "+")

# Open search results, sorted by "newest"
html_doc = urllib.request.urlopen("https://"+city+".craigslist.org/search/sss?query="+search+"&sort=date")

#function below sanatise the '#' out of the above list and also removed duplicates.
def listsanitation(homeInfo):
    i = 1
    while len(homeInfo) > i:
        if homeInfo[i] == homeInfo[i-1]:
            del homeInfo[i]
        i=i+1
    return homeInfo

#function find all links in the user request
def gather_all_links():
    # TODO - This only gets the first page of results, expand to get more pages
    hrefSet = set() # Use a set to remove duplicates
    soup = BeautifulSoup(html_doc, 'html.parser')
    for link in soup.find_all("li", class_="result-row"):
        for href in link.find_all('a'):
            prodLink = href.get('href')
            if prodLink != '#':
                hrefSet.add(prodLink)
    return list(hrefSet)

#checks to see if links are with in users timefram request
#if so, return link
#else return null to filther out.
#Needs to be changed to take array as paramaters to make nested dictonary object.
def product_info(links):
    prod_info = {}
    i = 0
    while len(links) > i:
        print("opening link: [{}]".format(links[i]))
        post_id = craigs_scrap_web.get_post_id(links[i])
        description = craigs_scrap_web.get_description(links[i])
        price = craigs_scrap_web.get_price(links[i])
        time = craigs_scrap_web.get_post_date(links[i])
        name = craigs_scrap_web.get_name(links[i])
        image_link = craigs_scrap_web.get_img(links[i])
        update = craigs_scrap_web.get_update_date(links[i])

        if(datetime.datetime.strptime(update, dateFormat) > check_time):
            item = {
                "name": name,
                "price": price,
                "description": description.replace('\n\n\n\n\n',""),
                "post_date": time,
                "last_update": update,
                "image_link": image_link,
                "link": links[i]
            }
            print("recent item found: {}".format(item))
            prod_info[post_id] = item
            i = i+1
        else:
            i = i+1
    return prod_info

#takes list and converts to json objects.
#this also puts it in its final dict form
def json_convert(all_links):
    json_object['all'] = all_links
    json_object['recent'] = product_info(all_links)
    return json.dumps(json_object)

#write to file and close file.

f.write(json_convert(gather_all_links()))
f.close()
