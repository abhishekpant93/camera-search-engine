import requests
import json
import re
from bs4 import BeautifulSoup

ROOT_URL = "http://imaging.nikon.com/lineup/dslr/"
FILENAME = "specs.json"

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

def get_specs_url(model_name):
    return "http://imaging.nikon.com/lineup/dslr/%s/spec.htm" % model_name

def get_img_url(model_name):
    return "http://imgsv.imaging.nikon.com/lineup/dslr/img/product_%s.png" % model_name
    
def filter_keys(old_keys):
    return [key for key in old_keys if len(key.get("class")) == 1]

def filter_vals(old_vals):
    return [val for val in old_vals if len(val.get("class")) == 1]
    
def get_specs(html):

    soup = BeautifulSoup(html)

    class_spec = "first-cell"
    class_val = "last-cell"
    
    keys = filter_keys(soup.find_all("th", class_= class_spec))
    vals = filter_vals(soup.find_all("td", class_= class_val))

    if len(keys) != 0:
        return keys, vals

    class_spec = "mod-table1-subHeading"
    class_val = "mod-table1-item"

    keys = filter_keys(soup.find_all("th", class_= class_spec))
    vals = filter_vals(soup.find_all("td", class_= class_val))

    return keys, vals

def get_cameras(root_url):
    camera_names = get_camera_names(root_url)
    camera_specs = {}
    for name in camera_names:
        print 'fetching info for ' + name + '...'
        camera_specs[name] = {}
        camera_specs[name]['img'] = get_img_url(name)
        url = get_specs_url(name)
        r = requests.get(url)
        html = r.text
        keys, vals = get_specs(html)
        specs = zip(keys, vals)
        for key, value in specs:
            k = key.text.encode('ascii', 'ignore')
            v = value.text.encode('ascii', 'ignore')
            camera_specs[name][k] = v
            if "accessories" in key.text:
                break
        print 'done'

    print 'finished fetching all slr camera info!'
    return camera_specs
        
def main():
    cameras = get_cameras(ROOT_URL)
    print ''
    for model, specs in cameras.iteritems():
        print 'Model: ' + model
        for k, v in specs.iteritems():
            print k,':', v
            print '------------'
        print '################################'
            
    with open(FILENAME, 'w') as outfile:
        json.dump(cameras, outfile)
        
main()
