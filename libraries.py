#!/usr/bin/python
# When run, this script will give a printout of the workshops happening at the NCSU
#libraries that appear on the first page

from bs4 import BeautifulSoup
import urllib.request as url

# visit the upcoming workshops page
rootURL = "https://www.lib.ncsu.edu"
upcomingWkshpsURL = "https://www.lib.ncsu.edu/workshops/upcoming"
with url.urlopen(upcomingWkshpsURL) as response:
    #read in page contents
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    #get title, date, and time of each workshop on the page
    workshopTitles = soup.findAll(class_="evt-title")
    workshopDates = soup.findAll(class_="evt-date")
    workshopTimes = soup.findAll(class_="evt-time")

    #for each workshop, print out title, date, and time
    for (title, date, time) in (zip(workshopTitles, workshopDates, workshopTimes)):
        print("Event Title: " + title.string)
        print("Event Date: " + date.string)
        print("Event Time: " + time.string)
        print(rootURL + title.a.get("href"))
        
        #get and print out the location, description, and registration link of each workshop
        with url.urlopen(rootURL + title.a.get("href")) as wkshp:
            wkshpHTML = wkshp.read()
            wkshpSoup = BeautifulSoup(wkshpHTML, 'html.parser')
            workshopLocation = wkshpSoup.select(
                "article #event-node .columns.medium-7 ul:nth-of-type(1) > li:nth-of-type(1)")
            workshopRegistrationLink = wkshpSoup.select(
                'a[href*="https://reporter.ncsu.edu/"]')
            print("Location: {}".format(
                workshopLocation[0].get_text().replace("\n", "")))
            workshop_description = wkshpSoup.select(".field-item p")
            print("Event Description: {}".format(
                workshop_description[0].get_text()))
            print("Registration Link: {}".format(
                  workshopRegistrationLink[0].get("href")))
            print("\n----------------------------------------\n")
