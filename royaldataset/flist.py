from os import listdir
from os.path import *
import os.path
import shutil
import json


def run(outpath, inpath):
    print("\033[92m------------Starting output directory manipulation-------------")
    if os.path.isdir(outpath):
        print("\033[92mOutput directory exist, cleaning..")
        shutil.rmtree(outpath)
        os.mkdir(outpath)
    else:
        print("\033[92mOutput directory does not exist, creating..")
        os.mkdir(outpath)
    print("------------Output directory manipulation complete-------------\n")
    print("----------------------Starting file listing--------------------")
    folders = [x[0] for x in os.walk(inpath)]
    for elem in folders:
        folders[folders.index(elem)] = (elem.replace(inpath, ''))
    while "" in folders:
        folders.remove("")

    print('Data folder contains the following data:')
    data = {'files': []}
    for x in folders:
        os.mkdir(outpath + x)
        print("   - For site \"" + x + "\": ")
        files = [f for f in listdir(inpath+x) if isfile(join(inpath+x, f))]
        for z in files:
            data['files'].append({'file': str(z), 'site': x})
            print("      - " + z)
    with open(outpath+'files.json', 'a') as f:
        json.dump(data, f, indent=4)
    print("Datafile list exported as : " + outpath + 'files.json')
    print("---------------------File listing complete---------------------\n")
