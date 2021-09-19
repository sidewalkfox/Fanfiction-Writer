from tkinter import *
import tkinter
import workIds as wi
import getFanfics as gf
#import this

##Functions
#Rounds to the nearest multiple of 10
def getEstimated():
	numReq = wi.requestedFics
	delay = gf.delay
	total = str(round((numReq * delay)/10)*10)
	return total

#Converts search term to workable url
def getIds():
	url = searchBox.get("1.0","end-1c")
	fixUrl = url.replace(' ', '+')
	outUrl = "https://archiveofourown.org/works/search?utf8=%E2%9C%93&work_search%5Bquery%5D=" + fixUrl
	wi.url = outUrl
	wi.main()

##TKinter
root = tkinter.Tk()

#Stuff
root.title("FFW")
icon = PhotoImage(file="images/paw.png")
root.iconphoto(False, icon)
root.resizable(False, False)

#Get Ids button
getIdsImages = PhotoImage(file="images/getIds.png")
getIdsButton = Button(root, image=getIdsImages, command=lambda:getIds())
getIdsButton.grid(row=0,column=0)

#Get Work button
getWorkImages = PhotoImage(file="images/getWorks.png")
getWorkButton = Button(root, image=getWorkImages, command=lambda:gf.main())
getWorkButton.grid(row=0,column=1)

#Search term
searchBox = Text(root, height=1, width=18)
searchBox.grid(row=1,column=0)

#Estimated time
estimated = Text(root, height=1, width=18, state='disabled')
estimated.insert(END, 'Estimated time: ' + getEstimated())
estimated.grid(row=1,column=1)

#Finishies Tkinter code
root.mainloop()