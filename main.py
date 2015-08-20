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

def dropDB(conn):
  c = conn.cursor()
  c.execute('DROP TABLE IF EXISTS Blog_Posts')
  c.execute('DROP TABLE IF EXISTS Web_Page')
  c.execute('DROP TABLE IF EXISTS Lookup') 

def resetDB(conn):
  dropDB(conn)
  createDB(conn)
  
#if (os.path.isfile(DB)):
#  conn = sqlite3.connect(DB)
#else:
#  conn = sqlite3.connect(DB)
#  createDB(conn)

conn = sqlite3.connect(DB)
resetDB(conn)
#createDB(conn)
c = conn.cursor()

# traverse CCE website directory, looking for <div id="relblogposts">
path = "/home/derek/cce/website"  #directory's static for now, eventually will be user-changeable

blogPages = []
print("Blog files:")
blogFNames = search.blogSearch(path)
#blogFNames = [path+"/blog/2014/11/discovery-day-viii.html"]
for blogFName in blogFNames:
  #print("Parsing", path + blogFName)
  blogFile = open(path + blogFName)
  blogParser = cceHTMLParser.cceBlogParser(path+blogFName)
  blogParser.feed(str(blogFile.read()))
  blogPages.append(blogParser.getBlogPage())

# we've got our blog pages, now enter them into the db
for blogPage in blogPages:
  values = blogPage.getValues()
  c.execute('INSERT INTO Blog_Posts (title, href, timestamp) VALUES (?,?,?)', values)
#c.execute('SELECT * FROM Blog_Posts')
#print("SELECT * FROM Blog_Posts\n", c.fetchall())

#----------------------------------------------


cceWebPages = []
print("\nWeb pages:")
HTMLFiles = search.HTMLSearch(path)
#HTMLFiles = [path+'/students/index.html']
for HTMLFilename in HTMLFiles:
   print("Parsing", path + HTMLFilename)
   HTMLFile = open(path+HTMLFilename)
   webParser = cceHTMLParser.cceHTMLParser(path+HTMLFilename)
   webParser.feed(str(HTMLFile.read()))
   cceWebPages.append(webParser.getWebPage())
   
# enter web pages into db
for webPage in cceWebPages:
  values = webPage.fname, webPage.pageTitle
  c.execute('INSERT INTO Web_Page (title, href) VALUES (?,?)', values)
  
  #for href in webPage.
  
c.execute('SELECT * FROM Web_Page')
print('SELECT * FROM Web_Page\n', c.fetchall())

conn.close
