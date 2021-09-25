from tkinter import *
import tkinter
import webbrowser
import os
import workIds as wi
import getFanfics as gf
import prepWorks as pw
import createWork as cw
#import this

#Variables
explicitTerms = ['True', 'False']
trainTerms = ['False', 'True']

##Functions
#Gets Ids
def getIds():
	#Converts search term to workable url
	url = searchBoxText.get("1.0","end-1c")
	fixUrl = url.replace(' ', '+')
	outUrl = "https://archiveofourown.org/tags/" + fixUrl + "/works"
	wi.url = outUrl

	#Gets the number of requested works, defaults to 0
	numWorks = numWorksText.get("1.0","end-1c")
	if(numWorks == ''):
		numWorks = 0
	else:
		numWorks = int(numWorks)
	if(numWorks < 0):
		numWorks = 0

	wi.requestedFics = numWorks
	wi.main()

#Uses the ids to get works
def getWorks():
	#Tells the program if explicit material should be used
	if(explicitSet.get() == 'True'):
		gf.getExplicit = True
	else:
		gf.getExplicit = False

	gf.main()

#Prepares the collected works to be run by the AI
def prepWork():
	pw.main()

#Uses the prepared works to create a new story
def getFin():
	#Tells the program if it needs to train a new model
	if(trainSet.get() == 'True'):
		cw.training = True
	else:
		cw.training = False

	#cw.reqFics = numWorks
	cw.main()

#Opens the GitHub page
def info():
	print('Opening GitHub')
	webbrowser.open_new("https://github.com/sidewalkchalka/Fan-Fiction-Writer")

#Clears the console
def clearConsole():
	os.system('cls' if os.name=='nt' else 'clear')

##TKinter
root = tkinter.Tk()

#Window settings
root.title("FFW")
icon = PhotoImage(file="images/icon.png")
root.iconphoto(False, icon)
root.resizable(False, False)

#Get Ids button
getIdsImages = PhotoImage(file="images/getIds.png")
getIdsButton = Button(root, image=getIdsImages, command=lambda:getIds())
getIdsButton.grid(row=0,column=0)

#Get Work button
getWorkImages = PhotoImage(file="images/getWorks.png")
getWorkButton = Button(root, image=getWorkImages, command=lambda:getWorks())
getWorkButton.grid(row=0,column=1)

#Prepare Work button
preWorkImages = PhotoImage(file="images/prepWork.png")
preWorkButton = Button(root, image=preWorkImages, command=lambda:prepWork())
preWorkButton.grid(row=0,column=2)

#Get Finished button
getFinImages = PhotoImage(file="images/getFin.png")
getFinButton = Button(root, image=getFinImages, command=lambda:getFin())
getFinButton.grid(row=0,column=3)

#Search term
searchLabel = Label(root, text='Search term')
searchBoxText = Text(root, height=1, width=18)
searchBoxText.insert(END, 'furry')
searchLabel.grid(row=1,column=0)
searchBoxText.grid(row=2,column=0)

#Number of works to collect
numWorksLabel = Label(root, text='Number of works to collect')
numWorksText = Text(root, height=1, width=18)
numWorksText.insert(END, '5')
numWorksLabel.grid(row=1,column=1)
numWorksText.grid(row=2,column=1)

#Allow nsfw works
explicitLabel = Label(root, text='Allow explicit works')
explicitLabel.grid(row=1,column=2)
explicitSet = StringVar(root)
explicitSet.set(explicitTerms[0])
explicitDown = OptionMenu(root, explicitSet, *explicitTerms)
explicitDown.config(width=18,height=1)
explicitDown.grid(row=2,column=2)

#Train new model
trainLabel = Label(root, text='Train new model')
trainLabel.grid(row=1,column=3)
trainSet = StringVar(root)
trainSet.set(trainTerms[0])
trainDown = OptionMenu(root, trainSet, *trainTerms)
trainDown.config(width=18,height=1)
trainDown.grid(row=2,column=3)

#Trash and info button frame
sysFrame = Frame(root)
sysFrame.grid(row=0,column=4)

#Trash button
trashImage = PhotoImage(file="images/trash.png")
trashButton = Button(sysFrame, image=trashImage, command=lambda:clearConsole())
trashButton.pack()

#Info button
infoImage = PhotoImage(file="images/info.png")
infoButton = Button(sysFrame, image=infoImage, command=lambda:info())
infoButton.pack()

#Finishies Tkinter code
root.mainloop()
