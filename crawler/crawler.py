import requests
import json
import re
from bs4 import BeautifulSoup

ROOT_URL = "http://imaging.nikon.com/lineup/dslr/"
AMAZON_SEARCH_URL = "http://www.amazon.in/s/ref=nb_sb_noss_1?url=search-alias%3Delectronics&field-keywords="

FILENAME = "cameras.json"

def get_camera_names(url):

    camera_names = []
    
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html)
    css_class = "mod-goods1"

    for link in soup.find_all("a", class_= css_class):
        href = link.get('href')
        idx = href.split("/").index("dslr") + 1
        camera_names.append(href.split("/")[idx].lower())

    return camera_names

def get_search_url(model_name):
    return AMAZON_SEARCH_URL + str("nikon+" + model_name + "+dslr+camera")        

def is_nikon_camera(url):
    return url.split("/")[3].split("-")[0] == "Nikon"

def get_product_url(model):
    r = requests.get(get_search_url(model))
    soup = BeautifulSoup(r.text)
    class_listing = "a-link-normal s-access-detail-page  a-text-normal"
    results = soup.find_all("a", class_ = class_listing)
    product_url = None
    if len(results) > 0:
        if is_nikon_camera(results[0].get("href")):
            product_url = results[0].get("href")
    return product_url

def get_specs(product_url):
    r = requests.get(product_url)
    soup = BeautifulSoup(r.text)
    class_lbl = "label"
    class_val = "value"
    lbls = soup.find_all("td", class_=class_lbl)
    vals = soup.find_all("td", class_=class_val)
    specs = {}
    for i in xrange(len(lbls)):
        if lbls[i].text != "Best Sellers Rank":
            specs[lbls[i].text] = vals[i].text

    id_price = "priceblock_"
    class_price = "a-color-price"
    if len(soup.find_all("span", id = re.compile(id_price))) > 0:
        specs['price'] = float(soup.find_all("span", id = re.compile(id_price))[0].text.encode('ascii', 'ignore').replace(",", ""))
    elif len(soup.find_all("span", class_ = re.compile(class_price))) > 0:
        specs['price'] = float(soup.find_all("span", class_ = re.compile(class_price))[0].text.encode('ascii', 'ignore').replace(",", ""))
    else:
        specs['price'] = 100000

    alt_img = "Nikon"
    imgs = soup.find_all("img", attrs={"alt": re.compile(alt_img)})
    if len(imgs) > 0:
        specs['img'] = imgs[0].get("src")
    else:
        specs['img'] = None
    return specs
    
def get_reviews_url(product_url):
    product_id = product_url.split("/")[-1]
    return "/".join(product_url.split("/")[0:4]) + "/product-reviews/" + product_id


def get_reviews(product_url):
    reviews_url = get_reviews_url(product_url)
    # print 'reviews_url = ', reviews_url
    r = requests.get(reviews_url)
    soup = BeautifulSoup(r.text)

    reviews = {}
    
    class_ratings = "s_star_"
    ratings = soup.find_all("span", class_ = re.compile(class_ratings))
    if len(ratings) > 0:
        reviews['avg_rating'] = float(ratings[0].text.split()[0])
    else:
        reviews['avg_rating'] = 4.0
    
    reviews['reviews'] = []
    reviews_div = soup.find_all("div", attrs={"style": "margin-left:0.5em;"})

    for review_div in reviews_div:
        text = review_div.text
        text = [line.rstrip().lstrip() for line in text.split("\n") if len(line.rstrip()) > 0]
        text = text[0:text.index("Help other customers find the most helpful reviews")]
        text = [line.encode('ascii', 'ignore') for line in text if line != "Verified Purchase(What is this?)"]
        # print 'text:'
        # for i, line in enumerate(text):
        #     print i, line
        # print '~~~~~~~~'
        
        ratingsIdx = -1
        titleIdx = -1
        bodyIdx = -1
        usefulnessIdx = -1
        for i, line in enumerate(text):
            if "out of 5 stars" in line:
                ratingsIdx = i
            if "found the following review helpful" in line:
                usefulnessIdx = i
            if "This review is from" in line:
                bodyIdx = i + 1
            if line.startswith("By") and titleIdx == -1:
                titleIdx = i - 1
                
        rating = title = body = usefulness = None
        if ratingsIdx >= 0:
            rating = float(text[ratingsIdx].split()[0])
        if titleIdx >= 0:
            title = text[titleIdx]
        if bodyIdx >= 0:
            body = "".join(text[bodyIdx:])
        if usefulnessIdx >= 0:
            usefulness = float(text[usefulnessIdx].split()[0]) / float(text[usefulnessIdx].split()[2])

        review = {'title': title, 'rating': rating, 'body': body, 'usefulness': usefulness}
            
        reviews['reviews'].append(review)

    return reviews
        
def get_camera_info():
    camera_names = get_camera_names(ROOT_URL)
    cameras = {}
    for model in camera_names:
        product_url = get_product_url(model)
        if product_url is None:
            continue
        print 'fetching info for ' + model + ' from ' + product_url + '...'
        cameras[model] = {}
        cameras[model]['url'] = product_url
        cameras[model]['specs'] = get_specs(product_url)
        cameras[model]['reviews'] = get_reviews(product_url)
        print 'done!'
    print '\n#### finished fetching info for all cameras! ####\n'
    return cameras

def main():
    cameras = get_camera_info()
    print ''
    for model, info in cameras.iteritems():
        print 'Model: ' + model
        for k, v in info.iteritems():
            print k, ":", v
            print '-----------------------'
            
        print '######################################'

    with open(FILENAME, 'w') as outfile:
        json.dump(cameras, outfile)
        print 'wrote data to file: ' + FILENAME + "!"
        
main()
