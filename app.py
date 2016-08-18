from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from bs4 import BeautifulSoup
import json
from urllib2 import urlopen

app = Flask(__name__)
api = Api(app)
BASE = "https://www.princeton.edu/~ota/"
reports = []
links = []

def main():                                #main method
    for x in range(74,96):                 #cycles through all years 
        get_all_reports("https://www.princeton.edu/~ota/ns20/caty"+str(x)+"_n.html") 

class Reports(Resource):
    def get(self):
        return {reports[k]: links[k] for k in range (0,721)}

def get_all_reports(source_url):           #populates array of links with a year's report links
    html = urlopen(source_url).read()      #finds the report pages for the given year
    soup = BeautifulSoup(html)
    l = soup.findAll("a")
    links = []                             
    for x in l:
        links.append(str(x))               #longwinded way but it makes them str
    for link in links:
        get_report_link(link) 

def get_report_link(page_link):            #converts one report link into a document link and file name
    year = page_link[18:22]  
    doc = page_link[23:27]
    bob = year+"_"+doc+"_"+page_link[36:len(page_link)-4]
    global reports
    global links
    reports.append(bob) 
    links.append(BASE+page_link[12:27]+page_link[22:27]+".PDF")
    
api.add_resource(Reports, '/reports/')

if __name__ == '__main__':
    main()
    app.run()