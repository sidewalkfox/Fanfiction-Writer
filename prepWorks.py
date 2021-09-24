import re
import getFanfics as gf

#Variables
textFile = gf.csvOut
textOut = 'prepWork.txt'

##Functions
def main():
	#List of things to replace with nothing
	deleteList = ['(See the end of the chapter for  notes.)', '","', '\n']

	#List of things to replace with the list below them
	#For example, replaceList[0] with be replaced with replaceTerms[0]
	replaceList = ['"New work', '""']
	replaceTerms = ['\n\n', '"']

	#Opens text file
	with open(textFile) as txtIn, open(textOut, 'w+') as txtOut:
		#For every line in the text file
		x=0
		for line in txtIn:
			#Skips if it's the first time running
			if(x==0):
				x=x+1
				continue
			#Delete List
			for word in deleteList:
				line = line.replace(word, '')
			#Replace List
			i=0
			for word in replaceList:
				line = line.replace(word, replaceTerms[i])
				i = i+1

			#Replaces multiple spaces with a single space
			line = re.sub("\ +", " ", line)

			txtOut.write(line)
