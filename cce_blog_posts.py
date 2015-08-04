import sqlite3
from HTMLParser import HTMLParser

DB = 'cbp.db'   #database name

conn = sqlite3.connect(DB)

def createdb(conn):
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS Blog_Posts
            (title text UNIQUE, href text UNIQUE, ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
  c.execute('''CREATE TABLE IF NOT EXISTS Web_Page
            (title text UNIQUE, href text UNIQUE, ID INTEGER PRIMARY KEY AUTOINCREMENT)''')
  c.execute('''CREATE TABLE IF NOT EXISTS Lookup
            (bp_id INTEGER, wp_id INTEGER
            FOREIGN KEY(bp_id) REFERENCES Blog_Posts(ID)
            FOREIGN KEY(wp_id) REFERENCES Web_Page(ID))''')
  
  #c.execute("INSERT INTO Blog_Posts (title, href) VALUES ('Post Title', 'Post Link')")
  conn.commit()
  return

createdb(conn)
c = conn.cursor()
c.execute('SELECT * FROM Blog_Posts')
print(c.fetchall())

conn.close
