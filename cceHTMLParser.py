from html.parser import HTMLParser

class cceHTMLParser(HTMLParser):
  foundRelBlogs = False
  foundATag = False
  
  
  def handle_starttag(self, tag, attrs):
    if tag == "div" and attrs == [('id', 'relblogs')]:
      print ('Found relblogs')
      self.foundRelBlogs = True
      
    if tag == "a" and self.foundRelBlogs:
      self.foundATag = True
      for name, value in attrs:
        if name=="href":
          print (value)
      
  
  def handle_data(self, data):
    if self.foundRelBlogs and self.foundATag:
      print (data)
      
  def handle_endtag(self, tag):
    if tag == "div" and self.foundRelBlogs:
      self.foundRelBlogs = False
    if tag =="a" and self.foundRelBlogs:
      self.foundATag = False
  
#  class cceWebPage():
    
