import os
import json
import operator
from collections import defaultdict

def print_dict(data):
        for model, info in data.iteritems():
                print 'Model: ' + model
                print 'URL:'+info['url']
                print 'Reviews:',info['reviews']
                for k, v in info['specs'].iteritems():
                        print k,':', v
                        print '------------'
                print '################################'
        return True

def loadfromjson():
	specsFile = "../crawler/cameras.json"
	with open(specsFile,'r+') as fp:
		data = json.load(fp)
		return data

def analyze(data):
        specs_dict = defaultdict(int)
        for model,info in data.iteritems():
                print 'Model:'+model
                #print 'URL:'+info['url']
                #print 'Reviews',info['reviews']
                for k,v in info['specs'].iteritems():
                        specs_dict[k] = specs_dict[k]+1
        sorted_dict = sorted(specs_dict.items(),key=operator.itemgetter(1),reverse = True)
        print sorted_dict
        return sorted_dict

def search(data,query):
        result = dict()
        for model,info in data.iteritems():
                specs = info['specs'] 
                for k,v in query.iteritems():
                        if k in specs and specs[k] >= v[0] and specs[k] <= v[1]:
                                print k,"is satisfied"        
                        else:
                                break
                result[model] = specs
                # Rank based on avg rating         
        return result

def specs(data,sorted_specs):
        for k,v in sorted_specs:
                print k,v
                for model,info in data.iteritems():
                        specs = info['specs']
                        if k in specs:
                                print specs[k]
                                
def add_sentiment_analysis(data):
        sent_data = data
        f = open("Sentiments.txt","rb")
        fl = f.read().split("\n")
        for line in fl[0:]:
                words = line.split(":")
                values = words[1].split(" ")
                sent_data[words[0]]['sent'] = []
                sent_data[words[0]]['sent'].append(values[0])
                sent_data[words[0]]['sent'].append(values[1])
                sent_data[words[0]]['sent'].append(values[2])
                sent_data[words[0]]['sent'].append(values[3])
                sent_data[words[0]]['sent'].append(values[4])
        return sent_data
        
def parse(data):
        parsed_dict = {}
        for model,info in data.iteritems():
                specs = info['specs']
                parsed_dict[model] = {}
                parsed_dict[model]['specs'] = {}
                parsed_dict[model]['url'] = info['url']
                for k,v in specs.iteritems():
                        if k == 'Screen Size':
                                words = v.split(" ")
                                if words[1] == 'Inches':
                                        parsed_dict[model]['specs']['Screen Size'] = float(words[0])
                                elif words[1] == 'Centimeters':
                                        parsed_dict[model]['specs']['Screen Size'] = float(words[0])/2.5
                        elif k == 'Optical Zoom' or k =='Optical Sensor Resolution' or k == 'Min Focal Length' or k == 'Min Shutter Speed' or k == 'Continuous Shooting Speed' or k == 'Max Resolution' or k == 'Resolution' or k == 'Digital Zoom' or k == 'Memory Storage Capacity' or k == 'Min Aperture' or k == 'Max Vertical Resolution':
                                words = v.split(" ")
                                parsed_dict[model]['specs'][k] = float(words[0])
                        elif k == 'Item Weight':
                                words = v.split(" ")
                                if words[1] == 'g':
                                        parsed_dict[model]['specs']['Item Weight'] = float(words[0])
                                elif words[1] == 'Kg':
                                        parsed_dict[model]['specs']['Item Weight'] = float(words[0])*1000
                        elif k == 'Product Dimensions':
                                parsed_dict[model]['specs']['Product Dimensions'] = []
                                words = v.split(" ")
                                parsed_dict[model]['specs']['Product Dimensions'].append(float(words[0]))
                                parsed_dict[model]['specs']['Product Dimensions'].append(float(words[2]))
                                parsed_dict[model]['specs']['Product Dimensions'].append(float(words[4]))
                        elif k == 'Video Capture Resolution':
                                words = v.split('x')
                                parsed_dict[model]['specs']['Video Capture Resolution'] = []
                                parsed_dict[model]['specs']['Video Capture Resolution'].append(int(words[0]))
                                parsed_dict[model]['specs']['Video Capture Resolution'].append(int(words[1]))
                        elif k == 'Display Resolution Maximum':
                                words = v.split(" ")
                                parsed_dict[model]['specs']['Display Resolution Maximum'] = int(words[0][:-1])
                        elif k == 'Number Of Items' or k == 'Memory Slots Available' or k == 'Model Year' or k == 'price':
                                # print v
                                parsed_dict[model]['specs'][k] = int(v)
                        else: 
                                parsed_dict[model]['specs'][k] = v
                parsed_dict[model]['avg rating'] = data[model]['ratings']['avg_rating']
        return parsed_dict                        

def main():
        data = loadfromjson()
        parsed = parse(data)

