import urllib.request, urllib.parse, urllib.error

fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')

counts = dict()
for line in fhand:
    words = line.decode().split()
    for word in words:
        counts[word] = counts.get(word, 0) + 1  #~get word or 0 : get return 0 (dict key's value) the first time it sees the word key or element+1. then with each repetition it adds one to it.
print(counts)
