from html.parser import HTMLParser
import re

class cceHTMLParser(HTMLParser):
  def __init__(self, fname):
    super(cceHTMLParser(HTMLParser).__init__()
    # we only care about stuff inside <div id="relblogs">
    self.foundRelBlogs = False
    self.foundATag = False
    self.cceWebPage(fname)
  
  def handle_starttag(self, tag, attrs):
    if tag == "div" and attrs == [('id', 'relblogs')]:
      print ('Found relblogs')
      self.foundRelBlogs = True
      
    if tag == "a" and self.foundRelBlogs:
      self.foundATag = True
      for name, value in attrs:
        if name=="href":
          print (value)
          self.cceWebPage.href.append(value)
  
  def handle_data(self, data):
    if self.foundRelBlogs and self.foundATag:
      print (data)
      self.cceWebPage.title.append(data)
      
  def handle_endtag(self, tag):
    if tag == "div" and self.foundRelBlogs:
      self.foundRelBlogs = False
      return self.cceWebPage  #relblog block has ended, return the cceWebPage object
    if tag == "a" and self.foundRelBlogs:
      self.foundATag = False
  
class cceWebPage():
  def __init__(self, fname):
    self.fname = fname    # name of the HTML file
    self.href = []        # blog post's URL
    self.title = []       # blog post's title (TODO: these should probably be part of a named tuple)
    

class cceBlogParser(HTMLParser):
  def __init__(self, fname):
    super(cceBlogParser, self).__init__()
    self.foundTitle = False
    self.foundTimestamp = False
    #self.cceBlogPage(fname)
  
  def handle_starttag(self, tag, attrs):
    if tag == "h1" and attrs == [('class'), ('fancy narrow_headline')]:
      print ("Found title")
      self.foundTitle = True
    if tag == "abbr":
      print (attrs)
    #if tag == "abbr" and attrs(range(0)) == (('class'), ('published'))
    #  for name, value in attrs:
    #    if name=="title"
    
  #def handle_data(self, data):
  #  print()
  #def handle_endtag(self, tag):
  #  print()

class cceBlogPage():
  def __init__(self, fname):
    self.fname = fname    #blog post's URL
    self.title = ""       #blog post's title
    self.timestamp = ""
    
