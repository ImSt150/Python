#Creating a DB and a Counts table in it  using sqlite3 library(from inside python)
#that counts the number of emails sent from each organization (in mbox.txt file) 
#python contains a builtin SQL API (sqlite3) lirary to interact with sqlite RDBMS
import sqlite3
#a 2 step open: 1.connection to DB(checking access to file)
#[cerating a coonection object using connect constructor]
#it is going to create a DB file, orgemaildb, .sqlite,in same directory as of emaildb.py
conn = sqlite3.connect('orgemaildb.sqlite')
#2.creating a curser (a handle) object using cursor method of connection object
cur = conn.cursor()
#cursor(Query) object is used by its methods(e.g.executeto run queries.)(or fetch to fethc data)
#sending SQL command to DB through curser.(and then receiving response from)
#first DROP the Counts table if exists. so we start with a fresh DB.
#writing SQL queries in ' ' as cursor methods' (e.g. execute) parameters.
#excecute is a method of cursor object of sqlite3 API library.
cur.execute('DROP TABLE IF EXISTS Counts')
#using ''' to make it easier to read longer things.
#creating a Counts table & pretending to be dict with 2 attributes (org,count).
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')
#prompting user to enter file name.
fname = input('Enter file name: ')
#if user didnot enter file name.
if (len(fname) < 1): fname = 'mbox.txt'
#creating a file handle using open.
fh = open(fname)
for line in fh:
    if not line.startswith('From: '): continue #back to beginning
    #making a list from each line (starting with From) words
    pieces = line.split()
    #print(pieces)
    #email is the 2nd element of list.
    email = pieces[1]
    #Looking at an email in mbox.txt, e.g. cwen@iupui.edu we see that the part
    # after @ is the organization.So, now we split our email into
    # a list of 2 elements using @. The organization is the 2nd element of it.
    emailcharlst = email.split('@')
    org = emailcharlst[1]
    #print(org) #debugging print

    #following up to commit is like dict part.
    #first selecting int count from our table DB where org could be ?
    #? is a placeholder, ensuring we don't allow SQL injection
    #(org,)tuple means ?placeholder will ultimately replaced with org.
    #this line is not retrieving the data yet.it's looking at SQL & ensuring
    #table name is right or there is any syntax error. it is opening a
    #record set. when true, we read this like a file.
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    #grab first one & give it back in row (the informaton got from DB).
    row = cur.fetchone()
    #print(row)
    #if there are no records that meet this=> row=none
    #like get, 2 columns, and a few rows. if we search through and we got through
    #and there was nothing, then row was None. Then we have to insert it.
    #? placeholder:going to have a value in this tuplbe.count=1 as it's the first time
    #
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    #if we pull back a row that exists.we add that count via Update(as might be multiple applications
    #talking to DB in the same time)
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    #commit(writing inf from memory to disk)(time consuming) each time we run the loop )
    conn.commit()

#By running the above loop we put everything in the DB.
#now want to read the DB, selecting the top 10
# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    #printing tuples of org and count
    print(str(row[0]), row[1])
#fianlly cursor object is closed using close method.
cur.close()
#Connection object is closed using Close () method to free up resources.
conn.close()
