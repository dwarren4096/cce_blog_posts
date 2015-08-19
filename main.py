import sqlite3
#from HTMLParser import HTMLParser
import os
import search
import cceHTMLParser


# set up SQLite database, create it if it doesn't exist
DB = 'cbp.db'   #database name

def createDB(conn):
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS Blog_Posts
            (title TEXT, href TEXT UNIQUE, timestamp TEXT, ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
  c.execute('''CREATE TABLE IF NOT EXISTS Web_Page
            (title TEXT, href TEXT UNIQUE, ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
  c.execute('''CREATE TABLE IF NOT EXISTS Lookup
            (bp_id INTEGER, wp_id INTEGER,
            FOREIGN KEY(bp_id) REFERENCES Blog_Posts(ID),
            FOREIGN KEY(wp_id) REFERENCES Web_Page(ID))''')
  
  #c.execute("INSERT INTO Blog_Posts (title, href) VALUES ('Post Title', 'Post Link')") #insert test data
  conn.commit()
  return

if (os.path.isfile(DB)):
  conn = sqlite3.connect(DB)
else:
  conn = sqlite3.connect(DB)
  createDB(conn)

#createDB(conn)
c = conn.cursor()
#c.execute('SELECT * FROM Blog_Posts')
#print(c.fetchall())

# traverse CCE website directory, looking for <div id="relblogposts">
path = "/home/derek/cce/website"  #directory's static for now, eventually will be user-changeable

blogPages = []
blogFNames = search.blogSearch(path)
#i=0
#blogFNames = [path+"/blog/2014/11/discovery-day-viii.html"]
for blogFName in blogFNames:
  print("Parsing", blogFName)
  blogFile = open(blogFName)
  blogParser = cceHTMLParser.cceBlogParser(blogFName)
  blogParser.feed(str(blogFile.read()))
  blogPages.append(blogParser.getBlogPage())

# we've got our blog pages, now enter them into the db
for blogPage in blogPages:
  values = blogPage.getValues()
  print (values)
  c.execute('INSERT INTO Blog_Posts (title, href, timestamp) VALUES (?,?,?)', values)
c.execute('SELECT * FROM Blog_Posts')
print(c.fetchall())

#HTMLFiles = search.HTMLSearch(path)

#cceWebPages = []
#cceWebPages.append(cceHTMLParser.cceWebPage(HTMLFiles[i]))

#parser = cceHTMLParser.cceHTMLParser()
#print ("Parsing", HTMLFiles[i])
#parserFile = open(HTMLFiles[i])
#parserFile = open(path+'/students/index.html')  #for testing purposes, use one that we know has relblog
#cceWebPages[i] = parser.feed(parserFile.read())

conn.close
