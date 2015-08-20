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
            (title TEXT, url TEXT UNIQUE, timestamp TEXT, ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
  c.execute('''CREATE TABLE IF NOT EXISTS Web_Page
            (title TEXT, url TEXT UNIQUE, ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
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
website_url = "http://www.sonoma.edu/cce"

blogPages = []
#print("Blog files:")
blogFNames = search.blogSearch(path)
#blogFNames = [path+"/blog/2014/11/discovery-day-viii.html"]
for blogFName in blogFNames:
  #print("Parsing", path + blogFName)
  blogFile = open(path + blogFName)
  blogParser = cceHTMLParser.cceBlogParser(website_url+blogFName)
  blogParser.feed(str(blogFile.read()))
  blogPages.append(blogParser.getBlogPage())

# we've got our blog pages, now enter them into the db
for blogPage in blogPages:
  values = blogPage.getValues()
  c.execute('INSERT INTO Blog_Posts (title, url, timestamp) VALUES (?,?,?)', values)
c.execute('SELECT * FROM Blog_Posts')
print("SELECT * FROM Blog_Posts\n", c.fetchall())

#----------------------------------------------


cceWebPages = []
#print("\nWeb pages:")
HTMLFiles = search.HTMLSearch(path)
#HTMLFiles = [path+'/students/index.html']
for HTMLFilename in HTMLFiles:
   #print("Parsing", path + HTMLFilename)
   HTMLFile = open(path+HTMLFilename)
   webParser = cceHTMLParser.cceHTMLParser(website_url+HTMLFilename)
   webParser.feed(str(HTMLFile.read()))
   webPage = webParser.getWebPage()
   if len(webPage.blogLink) != 0:
     cceWebPages.append(webPage)
   
# enter web pages into db
for webPage in cceWebPages:
  values = (webPage.pageTitle, webPage.fname)
  print('INSERT INTO Web_Page (title, url) VALUES ('+webPage.pageTitle+','+webPage.fname+')')
  c.execute('INSERT INTO Web_Page (title, url) VALUES (?,?)', values)
  
  # build references between web pages and blog posts
  print('SELECT ID FROM Web_Page WHERE url='+webPage.fname)
  c.execute('SELECT ID FROM Web_Page WHERE url=?', webPage.fname)
  wp_id = c.fetchone()
  for link in webPage.blogLink:
    url, title = link
    print('SELECT ID FROM Blog_Posts WHERE url='+url)
    c.execute('SELECT ID FROM Blog_Posts WHERE url=?', url)
    bp_id = c.fetchone()
    c.execute('INSERT INTO Lookup (bp_id, wp_id) VALUES (?,?)', (bp_id, wp_id))
  
#c.execute('SELECT * FROM Web_Page')
#print('SELECT * FROM Web_Page\n', c.fetchall())
# get all web pages that link to http://www.sonoma.edu/cce/blog/2014/11/top-ten-tips-simple-ways-to-save-your-health-your-money-and-your-planet.html
c.execute('SELECT * FROM Blog_Posts JOIN Lookup ON Blog_Posts.ID=Lookup.bp_id JOIN Web_Pages ON Lookup.wp_id=WebPages.ID WHERE Blog_Posts.url=\'http://www.sonoma.edu/cce/blog/2014/11/top-ten-tips-simple-ways-to-save-your-health-your-money-and-your-planet.html\'')
print('SELECT * FROM Blog_Posts JOIN Lookup ON Blog_Posts.ID=Lookup.bp_id JOIN Web_Pages ON Lookup.wp_id=WebPages.ID WHERE Blog_Posts.url=\'http://www.sonoma.edu/cce/blog/2014/11/top-ten-tips-simple-ways-to-save-your-health-your-money-and-your-planet.html\'\n', c.fetchall())

conn.close
