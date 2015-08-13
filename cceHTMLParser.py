from html.parser import HTMLParser

class cceHTMLParser(HTMLParser):
  foundRelBlogs = False
  def handle_starttag(self, tag, attrs):
    if tag=="div":
      print (attrs)
    
  #def handle_endtag(self, tag):
    #stuff
    
  #def handle_data(self, data):
    #stuff
    
  
