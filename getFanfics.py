from bs4 import BeautifulSoup
from unidecode import unidecode
import requests
import csv
import time
import sys
import os
import workIds as wi

#Variables
ficIds = [wi.csvName + '.csv']
csvOut = 'works.txt'
language = 'English'
getExplicit = False

#Work scrap delay obtained from workIds file
delay = wi.delay

##Functions
def getTagInfo(category, meta):
	try:
		tagList = meta.find("dd", class_=str(category) + ' tags').find_all(class_="tag")
	except AttributeError:
		return []
	return [unidecode(result.text) for result in tagList] 
	
#Gets information about works
def getStats(meta):
	#Defines work categories
	categories = ['language', 'published', 'status', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits'] 
	stats = list(map(lambda category: meta.find("dd", class_=category), categories))

	if not stats[2]:
		stats[2] = stats[1]
	try:		
		stats = [unidecode(stat.text) for stat in stats]
	except AttributeError as e:
		newStats = []
		for stat in stats:
			if stat: newStats.append(unidecode(stat.text))
			else: newStats.append('null')
		stats = newStats

	stats[0] = stats[0].rstrip().lstrip()
	status = meta.find("dt", class_="status")
	if not status: status = 'Completed' 
	else: status = status.text.strip(':')
	stats.insert(2, status)

	return stats      

#Defines tags and gets their value from function
def getTags(meta):
	tags = ['rating', 'category', 'fandom', 'relationship', 'character', 'freeform']
	return list(map(lambda tag: getTagInfo(tag, meta), tags))

#Gets kudos
def getKudos(meta):
	if(meta):
		#Gets kudos from work
		users = []
		kudos = meta.contents

		#Extracts users from kudos variable
		for kudo in kudos:
			if kudo.name == 'a':
				if 'more users' not in kudo.contents[0] and '(collapse)' not in kudo.contents[0]:
					users.append(kudo.contents[0])
		
		return users
	return []

#Gets bookmarks
def getBookmarks(url, headerInfo):
	bookmarks = []
	headers = {'user-agent' : headerInfo}

	req = requests.get(url, headers=headers)
	src = req.text

	time.sleep(delay)
	soup = BeautifulSoup(src, 'html.parser')

	sys.stdout.write('Scraping bookmarks ')
	sys.stdout.flush()

	#Finds all pages
	if(soup.find('ol', class_='pagination actions')):
		pages = soup.find('ol', class_='pagination actions').findChildren("li" , recursive=False)
		maxPages = int(pages[-2].contents[0].contents[0])
		count = 1
	
		sys.stdout.write('(' + str(maxPages) + ' pages)')
		sys.stdout.flush()

		while count <= maxPages:
			#Extracts bookmarks
			tags = soup.findAll('h5', class_='byline heading')
			bookmarks += getUsers(tags)

			#Goes to next page
			count += 1
			req = requests.get(url+'?page='+str(count), headers=headers)
			src = req.text
			soup = BeautifulSoup(src, 'html.parser')
			sys.stdout.write('.')
			sys.stdout.flush()
			time.sleep(delay)
	else:
		tags = soup.findAll('h5', class_='byline heading')
		bookmarks += getUsers(tags)

	return bookmarks

#Gets users from meta data
def getUsers(meta):
	users = []
	for tag in meta:
			user = tag.findChildren("a" , recursive=False)[0].contents[0]
			users.append(user)

	return users
	
#Runs if the id is invalid
def accessDenied(soup):
	if(soup.find(class_="flash error")):
		return True
	if(not soup.find(class_="work meta group")):
		return True
	return False

#Writes all information into a csv file
def writeCsv(ficId, language, writer, headerInfo=''):
	print('Scraping ', ficId)
	url = 'http://archiveofourown.org/works/'+str(ficId)+'?view_adult=true'
	headers = {'user-agent' : headerInfo}
	req = requests.get(url, headers=headers)
	src = req.text
	soup = BeautifulSoup(src, 'html.parser')
	if(accessDenied(soup)):
		print('Access Denied')
		errorRow = ' '.join(ficId) + ' Access Denied'
		print('ERROR: ' + errorRow)
	else:
		meta = soup.find("dl", class_="work meta group")
		tags = getTags(meta)
		stats = getStats(meta)

		#Checks if work is in the correct language
		if language != False and language != stats[0]:
			print('This work is not in ' + language + ', skipping...')
		elif((getExplicit == False) and (tags[0][0] == 'Explicit' or tags[0][0] == 'Mature' or tags[0][0] == 'Not Rated')):
			print('This work is explicit, skiping...')
		else:
			#Gets the work from ao3
			content = soup.find("div", id= "chapters")
			chapters = content.select('p')
			chaptertext = '\n\n'.join([unidecode(chapter.text) for chapter in chapters])
			row = [chaptertext]
			try:
				writer.writerow(row)
			except:
				print('Unexpected error: ', sys.exc_info()[0])
				errorRow = ' '.join(ficId) + ' ' + ' '.join([sys.exc_info()[0]])
				print('ERROR: ' + errorRow)
			print('Done.')

#This is called to start the program
def main():
	os.chdir(os.getcwd())
	with open(csvOut, 'w') as f_out:
		writer = csv.writer(f_out)
		csvFname = ficIds[0]
		with open(csvFname, 'r+') as f_in:
			reader = csv.reader(f_in)
			for row in reader:
				if not row:
					continue
				writeCsv(row[0], language, writer)
				time.sleep(delay)
