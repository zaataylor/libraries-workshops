#!/usr/bin/python
# When run, this script will give a printout of the workshops happening at the NCSU
# libraries that appear on all of the pages

from bs4 import BeautifulSoup
import urllib.request as url
import sys
import re

# visit the upcoming workshops page
rootURL = "https://www.lib.ncsu.edu"
upcomingWkshpsBaseURL = "https://www.lib.ncsu.edu/workshops/upcoming"
#integer value that will indicate page index
i = 0
#boolean indicating if there are more pages to process
morePages = True
while(morePages):
    upcomingWkshpsURL = upcomingWkshpsBaseURL + "?page={}".format(i)
    with url.urlopen(upcomingWkshpsURL) as response:
        # read in page contents
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        #check to make sure the page is valid; don't continue if it isn't
        # a = soup.find(name="main", text = re.compile("There are no workshops.*"))
        # print("Value of a on page {} is {}".format(i, a))
        # if(soup.find(name = "main", text="There are no workshops") == None):
        #     morePages = True
        #     print("Page {} was valid".format(i))
        # else:
        #     morePages = False
        #     print("Page {} was invalid".format(i))
        #     break

        i += 1

        # get title, date, and time of each workshop on the page
        workshopTitles = soup.findAll(class_="evt-title")
        workshopDates = soup.findAll(class_="evt-date")
        workshopTimes = soup.findAll(class_="evt-time")

        # for each workshop, print out title, date, and time
        for (title, date, time) in (zip(workshopTitles, workshopDates, workshopTimes)):
            print("Event Title: " + title.string)
            print("Event Date: " + date.string)
            print("Event Time: " + time.string)
            print(rootURL + title.a.get("href"))

            # get and print out the location, description, and registration link of each workshop
            with url.urlopen(rootURL + title.a.get("href")) as wkshp:
                wkshpHTML = wkshp.read()
                wkshpSoup = BeautifulSoup(wkshpHTML, 'html.parser')
                workshopLocation = wkshpSoup.select(
                    "article #event-node .columns.medium-7 ul:nth-of-type(1) > li:nth-of-type(1)")
                workshopRegistrationLink = wkshpSoup.select(
                    'a[href*="https://reporter.ncsu.edu/"]')
                print("Location: {}".format(
                    workshopLocation[0].get_text().replace("\n", "")))
                # workshop_description = wkshpSoup.select('a[h3="Workshop Description"]')
                # find page element(s) corresponding to the words "Workshop Description" and then
                # find the next element of class field item and get the text from it
                workshop_description = wkshpSoup.find(
                    "h3", text="Workshop Description")
                workshop_description = workshop_description.next_sibling.next_sibling.find_all(
                    "p")
                textBody = ""
                for paragraph in workshop_description:
                    textBody += paragraph.get_text()
                print("Event Description: {}".format(
                    textBody))
                print("Registration Link: {}".format(
                    workshopRegistrationLink[0].get("href")))
                print("\n----------------------------------------\n")
