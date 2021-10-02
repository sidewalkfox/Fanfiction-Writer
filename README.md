# Fanfiction Writer
### Features
- Collects work ids from Archive of Our Own
- Collects works from Archive of Our Own
- Collects tags from works
- Fixes collected work's syntax
- Creates Tensorflow model of the collected works
- Creates a story from the Tensorflow model

**To install**
1. Install Python (This was made in 3.9.5).
2. Install all dependencies from the `requirements.txt` file.
3. Download a trained_model from GitHub. *(Optional)*

**To collect work ids**
1. Specify a search term in the text box. The broader the term, the better.
2. Specify the number of works to collect. Whole numbers only.
3. Press the first button with the ao3 logo and wait for the console to signal completion.

**To collect works**
1. Decide if you want to allow explicit works or not. The default is set to true.
2. Press the book icon to start collecting works.
3. Wait for the console to signal completion.\
*The program may become unresponsive, this is normal, the program will become responsive after collection if finished.*

**To prepare works for AI**
1. Press the check mark button.
2. Wait for the console to signal completion.

**To create a new story from trained_model**
1. Download a trained model from GitHub, extract the files, and copy them into the root directory.
2. Make sure that the "Train new model setting" is False.
3. Press the notepad button and wait for the console to signal completion.\
*The program may become unresponsive, this is normal, the program will become responsive after generation if finished.*

**To create a new story from scratch *(advanced)***
1. Set the "Train new model setting" to True.
2. Open the `createWork.py` file and edit the variables under the "Train model variables" comment to customize your final work.
	- "numGenerate" is the number of characters the output work will contain.
	- "epochs" is the number of training sessions that will run. Higher is more accurate, but will take longer.
	- "startString" will be the first word to be in the finished work. Make sure to include a space after the word.
3. Press the notepad button and wait for the console to signal completion.\
*The program will become unresponsive, this is normal. This process is will take several hours.*

**Info button**\
This button will open the GitHub page.

**Trash button**\
This button will clear the console.

**Troubleshooting**\
Based on the jankiness of Beautiful Soup and the complexity of Tensorflow, there aren't many errors that could be built in. The best way to find an error is always looking at the console. Make sure that the steps are done in order, left to right. If you collect new works, a new model will have to be trained.

**Advanced settings**
- To change the language that works will be collected in, open the `getFanfics.py` file and change the language variable. Make sure that it is capitalized and spelled correctly.
- To change any of output file names, change "csvName" in `workIds.py`, "csvOut" in `getFanfics.py`, and "textOut" in `prepWorks.py`.
- If you want your output files to be more or less predictable, you can change the "temperature" in `createWork.py`. A higher number will result in more random text. This is not recommended.
