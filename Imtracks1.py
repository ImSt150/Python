#This application will read an iTunes export file in XML and produce a properly
#normalized database
#importing the XML parsing  (decoding) library ElementTree as ET alias
import xml.etree.ElementTree as ET
#SQLite library of python
import sqlite3
#creating the connection object and Imtrackdb database.
conn = sqlite3.connect('Imtrackdb.sqlite')
#creating a cursor object using cursor method from connection object.
cur = conn.cursor()
# throw away the artist table, album table, genre table, and track table,
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')


fname = input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'Library.xml'
#a viw of the XML music track file exported from iTune:
# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
#Defining a lookup of function
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None
#parse (decode) the fname string (XML UTF-8 external world), into an XML ET object (unicode).
stuff = ET.parse(fname)
#findall from XML ET object returns all child tags of 3rd level dict as a list's
# elements.To see all tracks.
all = stuff.findall('dict/dict/dict')
#print how many child tags we got in the 3rd level dict.
print('Dict count:', len(all))
for entry in all:
    #if it goes through all of these and there is not track ID, continue to next loop entry
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    genre = lookup(entry, 'Genre')

    if name is None or artist is None or album is None :
        continue

    print(name, artist, album, genre, count, rating, length)
    ##ignore says if it is already inserted don't blow up. Just do nothing.
    #? is where the artist variable goes.
    cur.execute('''INSERT OR IGNORE INTO Artist (name)
        VALUES ( ? )''', ( artist, ) )
    ##then need to know primary key of this particular Artist row. Sinc it is
    # the FK for Album table.
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    #fetch one row of Artist and pass its first element (id) as artist id
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id)
        VALUES ( ?, ? )''', ( album, artist_id ) )
    #need to know primary key of this particular Album row since it's FK for Track table.
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name)
            VALUES (?)''', ( genre,) )
    #need to know primary key of this particular Genre row since it's FK for Track table.
    cur.execute('SELECT id FROM Genre Where name = ?', (genre,))
    #fetch one row of Genre and pass its first element (id) as genre id
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count)
        VALUES ( ?, ?, ?, ?, ?, ? )''',
        ( name, album_id, genre_id, length, rating, count ) )

    conn.commit()
