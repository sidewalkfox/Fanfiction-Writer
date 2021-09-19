import requests
from bs4 import BeautifulSoup
import time
import os
import csv
import sys
from unidecode import unidecode
import workIds as wi

#Variables
ficIds = [wi.csvName + '.csv']
isCsv = (len(ficIds) == 1 and '.csv' in ficIds[0]) 
csvOut = 'works.csv'
includeBookmarks = False

#Work scrape delay, must be 5 or higher to not violate tos
delay = 5

def getTagInfo(category, meta):
	try:
		tagList = meta.find("dd", class_=str(category) + ' tags').find_all(class_="tag")
	except AttributeError as e:
		return []
	return [unidecode(result.text) for result in tagList] 
	
#Gets information about works
def getStats(meta):
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
	if (meta):
		users = []
		## hunt for kudos' contents
		kudos = meta.contents

		# extract user names
		for kudo in kudos:
			if kudo.name == 'a':
				if 'more users' not in kudo.contents[0] and '(collapse)' not in kudo.contents[0]:
					users.append(kudo.contents[0])
		
		return users
	return []

#Gets author(s)
def getAuthors(meta):
	tags = meta.contents
	authors = []

	for tag in tags:
		if tag.name == 'a':
			authors.append(tag.contents[0])

	return authors

#Get bookmarks
def getBookmarks(url, headerInfo):
	bookmarks = []
	headers = {'user-agent' : headerInfo}

	req = requests.get(url, headers=headers)
	src = req.text

	time.sleep(delay)
	soup = BeautifulSoup(src, 'html.parser')

	sys.stdout.write('scraping bookmarks ')
	sys.stdout.flush()

	#Finds all pages
	if (soup.find('ol', class_='pagination actions')):
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
			count+=1
			req = requests.get(url+'?page='+str(count), headers=headers)
			src = req.text
			soup = BeautifulSoup(src, 'html.parser')
			sys.stdout.write('.')
			sys.stdout.flush()
			time.sleep(delay)
	else:
		tags = soup.findAll('h5', class_='byline heading')
		bookmarks += getUsers(tags)

	print('')
	return bookmarks

#Gets user bookmarks
def getUsers (meta):
	users = []
	for tag in meta:
			user = tag.findChildren("a" , recursive=False)[0].contents[0]
			users.append(user)

	return users
	
#Runs if the id is invalid
def accessDenied(soup):
	if (soup.find(class_="flash error")):
		return True
	if (not soup.find(class_="work meta group")):
		return True
	return False

#Writes all information into a csv file
def writeCsv(ficId, includeBookmarks, writer, errorwriter, headerInfo=''):
	print('Scraping ', ficId)
	url = 'http://archiveofourown.org/works/'+str(ficId)+'?view_adult=true'
	headers = {'user-agent' : headerInfo}
	req = requests.get(url, headers=headers)
	src = req.text
	soup = BeautifulSoup(src, 'html.parser')
	if (accessDenied(soup)):
		print('Access Denied')
		errorRow = [ficId] + ['Access Denied']
		errorwriter.writerow(errorRow)
	else:
		meta = soup.find("dl", class_="work meta group")
		author = getAuthors(soup.find("h3", class_="byline heading"))
		tags = getTags(meta)
		stats = getStats(meta)
		title = unidecode(soup.find("h2", class_="title heading").string).strip()
		visibleKudos = getKudos(soup.find('p', class_='kudos'))
		hiddenKudos = getKudos(soup.find('span', class_='kudos_expanded hidden'))
		allKudos = visibleKudos + hiddenKudos

		#Gets bookmarks
		if (includeBookmarks):
			bookmarkUrl = 'http://archiveofourown.org/works/'+str(ficId)+'/bookmarks'
			allBookmarks = getBookmarks(bookmarkUrl, headerInfo)
		else:
			allBookmarks = []
		#Gets the work from ao3
		content = soup.find("div", id= "chapters")
		chapters = content.select('p')
		chaptertext = '\n\n'.join([unidecode(chapter.text) for chapter in chapters])
		row = [ficId] + [title] + [author] + list(map(lambda x: ', '.join(x), tags)) + stats + [allKudos] + [allBookmarks] + [chaptertext]
		try:
			writer.writerow(row)
		except:
			print('Unexpected error: ', sys.exc_info()[0])
			errorRow = [ficId] +  [sys.exc_info()[0]]
			errorwriter.writerow(errorRow)
		print('Done.')

#This is called to start the program
def main():
	os.chdir(os.getcwd())
	with open(csvOut, 'w') as f_out:
		writer = csv.writer(f_out)
		with open(csvOut + "Errors", 'a') as e_out:
			errorwriter = csv.writer(e_out)
			#Writes a header if the csv doesn't exist
			if os.stat(csvOut).st_size == 0:
				print('Writing a header row for the csv.')
				header = ['workId', 'title', 'author', 'rating', 'category', 'fandom', 'relationship', 'character', 'additional tags', 'language', 'published', 'status', 'status date', 'words', 'chapters', 'comments', 'kudos', 'bookmarks', 'hits', 'all_kudos', 'all_bookmarks', 'body']
				writer.writerow(header)
			if isCsv:
				csvFname = ficIds[0]
				with open(csvFname, 'r+') as f_in:
					reader = csv.reader(f_in)
					for row in reader:
						if not row:
							continue
						writeCsv(row[0], includeBookmarks, writer, errorwriter)
						time.sleep(delay)

			else:
				for ficId in ficIds:
					writeCsv(ficId, includeBookmarks, writer, errorwriter)
					time.sleep(delay)
