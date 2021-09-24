import re
import getFanfics as gf

#Variables
textFile = gf.csvOut
textOut = 'prepWork.txt'
textContent = ''

##Functions
def main():
	global textContent
	#List of things to replace with the list below them, replaceList[0] with be replaced with replaceTerms[0]
	replaceList = ['(See the end of the chapter for  notes.)', '","', '"New work', '""']
	replaceTerms = ['', '', '\n\n', '"']

	#Opens both text files
	with open(textFile) as txtIn, open(textOut, 'w+') as txtOut:
		#Fixes formating that applies to each line
		x=0
		for line in txtIn:
			#Skips if it's the first time running, removes the first line
			if(x==0):
				x=x+1
				continue
			#Replace List
			i=0
			for word in replaceList:
				line = line.replace(word, replaceTerms[i])
				i = i+1
			#Removes empty lines
			if(line.isspace()):
				line = ''

			textContent = textContent + line

		#Fixes formating that applies to the entire file
		textContent = re.sub("\ +", " ", textContent)
		textContent = re.sub("\\n+", "\n\n", textContent)
		txtOut.write(textContent)
