import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
# importing XML parsing library ElementTree as alias ET
import xml.etree.ElementTree as ET
#importing SSLcertificate  a file in a website origin server that
#does SSL/TLS encryption, moving the website from HTTP to HTTPS.
# SSL certificate file includes the website's public key and identity.
import ssl

#ignoring SSL certificate errors
ctx=ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#prompting for the user to enter the location, and assigning it to address variable
url = input('Enter location:')
#creating a handle url file (i.e. HTTPResponse object) from url webpage,and ignoring the SSL certificate errors
#and reading (Retrieving)that into an xml data string file (bytes object)(still external)(UTF-8)
xmldata = urlopen(url, context=ctx).read()
print(type(xmldata)) #debugging print result: class 'bytes'
#print(xmldata) #debugging print result : all xml data file is printed (encoded=UTF-8)
#calling ET's fromstring method on data XML string (outside world) to return a
#pyton inside world information element tree
commentinfotree = ET.fromstring(xmldata)
#print(type(commentinfotree))#debugging print result: class 'xml.etree.ElementTree.Element'
#print(commentinfotree) #debugging print result: <Element 'commentinfo' at 0x000001BF2C5D87C0> :That is right.
#parsing the commentinfo element tree and extracting a list of comment tag (elements)
lst = commentinfotree.findall('comments/comment')
#print(lst)
countnumbersum=0
count=0
#Item element (comment tag) iterates through the comments list
for item in lst:
    #print(item.find('count').text) #it prints all the count tag item texts(i.e.numbers)
    #counting the number of iterations (i.e. the number item element (comment tag) inside element tree)
    count=count+1
    #finding item element's (comment tag) child tag (count), and then returning its
    #text content(numeric text) and then converting it into an integer.
    #So, it is added to the sum of numbers.
    countnumbersum = countnumbersum + int(item.find('count').text)
print('Retrieving', url)
#print all the characters in the retrieved (i.e. read) url, upon being read into
# a data xml string (UTF-8 bytes object )
print('Retrieved', len(xmldata),'characters')
print('Count:', count)
print('Sum:', countnumbersum)
