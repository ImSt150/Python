#write a Python program to use urllib to read the HTML from the data files
#below, and parse the data, extracting numbers and compute the sum of
#the numbers in the file

#to run this, download the BeautifulSoup zip file
#http://www.py4e.com/code3/bs4.zip
#and unzip it in the same dierctory as this file
import urllib.request, urllib.parse, urllib.error

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
#Becasue some URLs have a certificate that's not in Python's official list
# Ignore SSL certificate errors, by creating a context variable ctx
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
#prompting for the user to input his desired url
url = input('Enter - ')
#creating a handle url file from url webpage,and ignoring the SSL cerrtificate
#errors, by adding context variable, and reading that into an html file
html = urlopen(url,context=ctx).read()
#parsing all the data in the html file (and decoding)using BeautifulSoup parser
soup = BeautifulSoup(html,"html.parser")

#Retrieve a list of all of the span tags in the soup (parsed html file)
tags = soup('span')
SumIntContents = 0
for tag in tags: #tag elements from tags list
    #look at the parts of a tag
    #print('Tag:', tag) #debugging
    #return attributes (URL) in each anchor tag. (i.e. href=). getting href or None
    #print('URL:', tag.get('href', None)) #debugging
    #return the first content of each span tag
    #print('Contents:', tag.contents[0]) #debugging
    #return class attributes of each span tag
    #print('Attrs', tag.attrs) #debugging
    #turning the string content[0] into int number
    IntContents = int(tag.contents[0])
    SumIntContents = SumIntContents + IntContents
print(SumIntContents)
