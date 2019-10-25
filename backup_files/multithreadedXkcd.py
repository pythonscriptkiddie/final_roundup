#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:12:28 2019

@author: thomassullivan
"""

#downloads XKCD comics using multiple threads

import requests, os, bs4, threading

os.makedirs('xkcd', exist_ok=True)

def downloadXkcd(startComic, endComic):
    for urlNumber in range(startComic, endComic):
        #download the page.
        print('Downloading page http://xkcd.com/%s...' % (urlNumber))
        res = requests.get('http://xkcd.com/%s...' % (urlNumber))
        res.raise_for_status()
        
        soup = bs4.BeautifulSoup(res.text)
        #find the url of the comic image.
        
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print('Could not find comic image.')
        else:
            comicUrl = comicElem[0].get('src')
            #Download the image
            res = requests.get(comicUrl)
            res.raise_for_status()
            
            #save the image to ./xkcd
            
            imageFile=open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        
#create and start the thread objects
downloadThreads = []
for i in range(1, 1400, 100):
    downloadThread = threading.Thread(target=downloadXkcd, args=(i, i + 99))
    downloadThreads.append(downloadThread)
    downloadThread.start()