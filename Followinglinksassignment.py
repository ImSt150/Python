#a Python program that expands on https://www.py4e.com/code3/urllinks.py.
#The program will use urllib to read the HTML from the data files
#extract the href= values from the anchor tags,
#scan for a tag that is in a particular position from the top
# and follow that link, repeat the process a number of times,
#and report the last name you find.

#to run this, download the BeautifulSoup zip file
#http://www.py4e.com/code3/bs4.zip
#and unzip it in the same dierctory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
#Becasue some URLs have a certificate that's not in Python's official list
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#prompting for the user to input his desired url
url = input('Enter URL:')
#prompting for the user to input his desired position in the url
position = input('Enter position:')
#prompting for the user to input his desired number of repetition for the url scraping
count = input('Enter count:')
i=1
while i < int(count)+1:
    #creating a handle url file from url webpage,and ignoring the SSL cerrtificate errors
    #and reading that into an html file
    html = urlopen(url,context=ctx).read()
    #parsing all the data in the html file (and decoding)using BeautifulSoup parser
    soup = BeautifulSoup(html,"html.parser")
    #Retrieve a list of all of the anchor tags in the soup (parsed html file)
    tags = soup('a')
    #assigning the new url (to be scrapped in the next round of loop)based on desired position
    url=tags[int(position)-1].get('href', None)
    i=i+1
    #look at the parts of a tag
    print('Tag:', tags[int(position)-1])
    #return attributes (URL) in each anchor tag. (i.e. href=). getting href or None
    print('URL:', tags[int(position)-1].get('href', None))
    #return the first content of each anchor tag
    print('Contents:', tags[int(position)-1].contents[0])
