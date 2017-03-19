#package imports
import urllib3
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import re
import urllib3
#GET-request from website
#http = urllib3.PoolManager()
import requests


def find_voucher(loc, query):
    query = query.replace(" ", "&").lower()
    requesturl = "https://www.groupon.de/browse/" + loc + "?address=" + loc.title() + "?query=" + query + "&hasLocCookie=true&locale=de_DE"
    response = requests.get(requesturl)

    soup = BeautifulSoup(response.text,"html.parser")

    #find all tiles
    tiles = soup.find_all("figure")

    merchantName = []
    description = []
    image_url = []
    redirect_url = []
    originalPrice = []
    newPrice = []
    location = []
    distance = []
    #parse all information in the tiles
    for t in tiles:
        #search for merchant
        merchantName_string = t.find_all("div", class_="cui-merchant-name c-txt-gray-dk cui-truncate")
        if(len(merchantName_string)):
            merchantName_i = re.findall(r"\n\s+(.*)\n", str(merchantName_string))[0]
        else:
            merchantName_i = "NA"
        merchantName.append(merchantName_i)

        #search for description
        description_string = t.find_all("p", class_ = "cui-deal-title c-txt-black ")
        if(len(description_string)>0):
            description_i = re.findall(r">(.*)<", str(description_string))[0]
        else:
            description_i = "NA"
        description.append(description_i)

        #search for the image URL
        image_url_string = t.find_all("img", class_= "cui-image lazy-load ")
        if(len(image_url_string)>0):
            image_url_i = re.findall(r"//(.*) data",str(image_url_string))[0]
            image_url_i = image_url_i[:-1]
        else:
            image_url_i = "NA"
        image_url.append(image_url_i)

        #search for the redirect url
        redirect_url_string = t.find_all('div', class_= "cui-content c-bg-gray-bg")
        if(len(redirect_url_string)>0):
            redirect_url_i = re.findall(r"<a href=(.*)>",str(redirect_url_string))[0]
            redirect_url_i = redirect_url_i[1:-1]
        else:
            redirect_url_i = "NA"
        redirect_url.append(redirect_url_i)

        #search for original price
        originalPrice_string = t.find_all("s")
        if(len(originalPrice_string)>0):
            originalPrice_i = re.findall(r"\d+\s+", str(originalPrice_string))[0]
            #originalPrice_i = re.findall(r">(.*)<", str(originalPrice_string))[0]
        else:
            originalPrice_i = "NA"
        originalPrice.append(originalPrice_i)

        #search for the new price
        newPrice_string = t.find_all("div", class_ = "cui-price")
        if(len(newPrice_string)>0):
            #newPrice_i = re.findall(r"span>(\d+([,.]\d+)?)\s+", str(newPrice_string))#[0][0]
            newPrice_i = re.findall(r">(.*)</s",str(newPrice_string))[0]
            newPrice_i = re.findall(r"(\d+([,.]\d+)?)", str(newPrice_i))[0][0]
        else:
            newPrice_i = "NA"
        newPrice.append(newPrice_i)


        #search for the location
        location_string = t.find_all("span", class_ = "cui-location-name")
        if(len(location_string)>0):
            location_i = re.findall(r"\n\s+(.*)\n", str(location_string))[0]
        else:
            location_i = "NA"
        location.append(location_i)

        #serch for distance
        distance_string = t.find_all("span", class_= "cui-location-distance")
        if(len(distance_string)>0):
            distance_i = re.findall(r"(\d+([,.]\d+)?)", str(distance_string))[0][0]
        else:
            distance_i = "NA"
        distance.append(distance_i)

    data = pd.DataFrame(
        {'description': description,
         'distance': distance,
         'merchant_name': merchantName,
         'originalPrice':originalPrice,
         'new_price': newPrice,
         'location': location,
         'imageUrl': image_url,
         'redirectUrl':redirect_url
        })

    remove_rows = data.isin(["NA"]).any(1)
    data = data[remove_rows==False]
    #data = data.drop(0, axis=0)

    return data