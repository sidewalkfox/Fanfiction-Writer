from bs4 import BeautifulSoup
import requests
import csv
import time

#Variables
pageEmpty = False
baseUrl = ""
url = ''
requestedFics = 0
recordedFics = 0
csvName = "workIds"

#Keeps track of all work ids to not repeat
seenIds = []

#Must be over 5
delay = 5

##Functions
def getIds(header_info=''):
    global pageEmpty
    headers = {'user-agent' : header_info}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    works = soup.select("li.work.blurb.group")

    #See if we collected all available work
    if(len(works) == 0):
        pageEmpty = True

    #Creates list of ids
    ids = []
    for tag in works:
        t = tag.get('id')
        t = t[5:]
        if not t in seenIds:
            ids.append(t)
            seenIds.append(t)
    return ids

def updateNextPage():
    global url
    key = "page="
    start = url.find(key)

    #Checks for a page indicator
    if(start != -1):
        #Finds the indicator in the url
        pageStartIndex = start + len(key)
        pageEndIndex = url.find("&", pageStartIndex)
        #Runs if the indicator is in the middle of the url
        if(pageEndIndex != -1):
            page = int(url[pageStartIndex:pageEndIndex]) + 1
            url = url[:pageStartIndex] + str(page) + url[pageEndIndex:]
        #Runs if the indicator is at the end of the url
        else:
            page = int(url[pageStartIndex:]) + 1
            url = url[:pageStartIndex] + str(page)

    #Since there is no page indicator, we must be on page 1
    else:
        #If there are other modifiers
        if(url.find("?") != -1):
            url = url + "&page=2"
        #If there are no modifiers
        else:
            url = url + "?page=2"

#Writes ids and url to .csv file
def writeIds(ids):
    global recordedFics
    with open(csvName + ".csv", 'a') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        for id in ids:
            if(notFinished()):
                wr.writerow([id, url])
                recordedFics = recordedFics + 1
            else:
                break

#Checks if we have too many files or if the page is empty
def notFinished():
    if(pageEmpty):
        return False

    if(requestedFics == 0):
        return True
    else:
        if(recordedFics < requestedFics):
            return True
        else:
            return False

#Runs functions to get the work ids
def processIds(headerInfo=''):
    while(notFinished()):
        #Delay between requests as per AO3's terms of service
        time.sleep(delay)
        ids = getIds(headerInfo)
        writeIds(ids)
        updateNextPage()

#Gets called to start the program
def main():
    #Clears the workIds file
    idFile = open(csvName + ".csv", "w")
    idFile.truncate()
    idFile.close()

    #Checks if the number of requested works has been set
    if(requestedFics == 0):
        print('WARNING! Number of requested works not set. Will collect all available works.\nprocessing...')
    else:
        print ("processing...")
        
    processIds()
    print ("Finished processing")
