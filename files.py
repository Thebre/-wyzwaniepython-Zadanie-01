#! python3

# Reads files from a given path
# checks dates of modyfing and sorts them to year and month folders
# while putting duplicates to separate folder.

import os, datetime, shutil

# internals
database = {} # {file's text : (file's path, year of last modify, month of last modify)}
is_duplicate = False

# input path
PATH = r'.\tst'

# paths for new folders
newPath = PATH + ' sorted'
duplicates = os.path.join(newPath, 'duplicates')


# database filling loop
print('Scaning directory...')
for root, dirs, files in os.walk(PATH):
    for file in files:
        totalPath = os.path.join(PATH, file)
        oFile = open(totalPath)
        text = oFile.read() # database key
        oFile.close()
        date = datetime.datetime.fromtimestamp(os.path.getmtime(totalPath))
        tFile = (totalPath, date.year, date.month) # database value
        check = database.setdefault(text, tFile) # check is tFile if text key was created
        if check != tFile and (check[1] > tFile[1] or (check[1] == tFile[1] and check[2] > tFile[2])): # if check != tFile than key was already created before AND year, month comparison
            database[text] = tFile # executed when key was already in database before AND date of modyfing is older at that key
            # marking duplicate existance and securing folder for putting duplicates in
            if not is_duplicate:
                is_duplicate = True
                if not os.path.isdir(duplicates):
                    os.makedirs(duplicates)


# sorting to folders
print('Sorting files...')
if not os.path.isdir(newPath):
    os.makedirs(newPath)

for key in database:
    sortedPath = os.path.join(newPath, str(database[key][1]), str(database[key][2]))
    if not os.path.isdir(sortedPath):
        os.makedirs(sortedPath)
    shutil.move(database[key][0], sortedPath)

if is_duplicate:
	for file in os.listdir(PATH):
	    shutil.move(os.path.join(PATH, file), duplicates)
       

input('Done!')
