from html.parser import HTMLParser
import re

class cceHTMLParser(HTMLParser):
  def __init__(self, fname):
    super(cceHTMLParser, self).__init__(convert_charrefs=True)
    # we only care about stuff inside <div id="relblogs">
    self.webPage = cceWebPage(fname)
    self.foundRelBlogs = 0    # 0 if before <div id="relblogs">, 1 if inside it, 2 if after </div>
    self.foundATag = False
    self.foundTitle = False
    self.url = ''
    #self.linkname = ''
  
  def handle_starttag(self, tag, attrs):
    if tag == "div" and attrs == [('id', 'relblogs')]:
      #print ('Found relblogs')
      self.foundRelBlogs = 1
      
    if tag == "a" and self.foundRelBlogs == 1:
      self.foundATag = True
      for name, value in attrs:
        if name=="href":
          #print (value)
          #self.webPage.blogHref.append(value)
          self.url = value
    
    # each page only has one <title> tag, no special checks needed here
    if tag == "title":
      self.foundTitle = True
  
  def handle_data(self, data):
    if self.foundRelBlogs == 1 and self.foundATag:
      #print (data)
      #self.webPage.blogTitle.append(data)
      self.webPage.blogLink.append((self.url, data))
    if self.foundTitle:
      data = data.split(" - ")[0] 
      #print("Title:", data)
      self.webPage.pageTitle = data
      
  def handle_endtag(self, tag):
    if tag == "div" and self.foundRelBlogs == 1:
      self.foundRelBlogs = 2
    if tag == "a" and self.foundRelBlogs == 1:
      self.foundATag = False
    if tag == "title":
      self.foundTitle = False
      
  def getWebPage(self):
    return self.webPage
  
class cceWebPage():
  def __init__(self, fname):
    self.fname = fname        # name of the HTML file
    self.pageTitle = ''
    #self.blogHref = []        # blog post's URL
    #self.blogTitle = []       # blog post's title
    self.blogLink = []         # tuple consisting of the blog post's URL and title
    
  #def getValues(self):
    
#----------------------------------------------------------

class cceBlogParser(HTMLParser):
  def __init__(self, fname):
    super(cceBlogParser, self).__init__(convert_charrefs=True)
    self.foundTitle = False
    self.foundTimestamp = False
    self.foundHeader = 0    # 0 if before <div id="entry-*">, 1 if inside, 2 if after </div>
    self.blogPage = cceBlogPage(fname)
  
  def handle_starttag(self, tag, attrs):
    #if tag == "h1" and attrs == [('class', 'fancy narrow_headline')]:
    # no special checks needed here, each page only has one title
    if tag == "title":
      #print ("Found title")
      self.foundTitle = True
    
    if tag == "div" and self.foundHeader == 0:
      for a in attrs:
        key, value = a
        if key == "id" and re.match("entry-*", value):
          self.foundHeader = 1
    
    if tag == "abbr" and self.foundHeader == 1:
      for a in attrs:
        key, value = a
        if a == ('class', 'published'):
          self.foundTimestamp = True
        if key == 'title' and self.foundTimestamp:
          #print (value)
          self.blogPage.timestamp = value
    
  def handle_data(self, data):
    if self.foundTitle:
      data = data.split(" - ")[0] 
      #print("Title:", data)
      self.blogPage.title = data
      
  def handle_endtag(self, tag):
    if tag == "title":
      self.foundTitle = False
    if tag == "div" and self.foundHeader==1:
      self.foundHeader = 2
      
  def getBlogPage(self):
    return self.blogPage

class cceBlogPage():
  def __init__(self, fname):
    self.fname = fname    #blog post's URL
    self.title = ""       #blog post's title
    self.timestamp = ""
    
  def getValues(self):
    return (self.title, self.fname, self.timestamp)
    
