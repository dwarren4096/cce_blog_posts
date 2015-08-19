import sqlite3
#from HTMLParser import HTMLParser
import os
import search
import cceHTMLParser


# set up SQLite database, create it if it doesn't exist
DB = 'cbp.db'   #database name

if (os.path.isfile(DB)):
  conn = sqlite3.connect(DB)
else:
  conn = sqlite3.connect(DB)
  createDB(conn)

def createDB(conn):
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS Blog_Posts
            (title text UNIQUE, href text UNIQUE, ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
  c.execute('''CREATE TABLE IF NOT EXISTS Web_Page
            (title text UNIQUE, href text UNIQUE, ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
  c.execute('''CREATE TABLE IF NOT EXISTS Lookup
            (bp_id INTEGER, wp_id INTEGER
            FOREIGN KEY(bp_id) REFERENCES Blog_Posts(ID)
            FOREIGN KEY(wp_id) REFERENCES Web_Page(ID))''')
  
  #c.execute("INSERT INTO Blog_Posts (title, href) VALUES ('Post Title', 'Post Link')") #insert test data
  conn.commit()
  return

#createDB(conn)
c = conn.cursor()
#c.execute('SELECT * FROM Blog_Posts')
#print(c.fetchall())

# traverse CCE website directory, looking for <div id="relblogposts">
path = "/home/derek/cce/website"  #directory's static for now, eventually will be user-changeable

#blogFNames = search.blogSearch(path)
blogFNames = [path+"/blog/2014/11/discovery-day-viii.html"]
print("Parsing", blogFNames[0])
blogFile = open(blogFNames[0])
blogParser = cceHTMLParser.cceBlogParser(blogFNames[0])
blogParser.feed(str(blogFile.read()))

#HTMLFiles = search.HTMLSearch(path)

#cceWebPages = []
#cceWebPages.append(cceHTMLParser.cceWebPage(HTMLFiles[0]))

#parser = cceHTMLParser.cceHTMLParser()
#print ("Parsing", HTMLFiles[0])
#parserFile = open(HTMLFiles[0])
#parserFile = open(path+'/students/index.html')  #for testing purposes, use one that we know has relblog
#cceWebPages[0] = parser.feed(parserFile.read())

conn.close
