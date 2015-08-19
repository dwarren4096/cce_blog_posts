import fnmatch
import os
import os.path
import re

#path = "/home/derek/cce/website"
# Goes through the directory tree, returns a list of all the .html files
def HTMLSearch(path):
  #grab only .html files
  include = ['*.html']
  #exclude directories which do not contain html files (blog is a special case)
  exclude = ["blog", ".git", "_notes", "images", "pdf_files", "js", "css"]
  
  #convert glob patterns to regex
  include = r'|'.join([fnmatch.translate(x) for x in include])
  #exclude = r'|'.join([fnmatch.translate(x) for x in exclude])
  
  files = search(path, include, exclude)

  return files
  
# returns a list of all blog posts
def blogSearch(path):
  blogPath = path+"/blog"
  #grab only .html files
  include = ['*.html']
  #directories to exclude
  exclude = [".git", "_notes", "assets_c"]
  
  #convert glob patterns to regex
  include = r'|'.join([fnmatch.translate(x) for x in include])
  #exclude = r'|'.join([fnmatch.translate(x) for x in exclude])
  
  files = search(blogPath, include, exclude)
  
  return files
  
  
def search(path, include, exclude):
  for root, dirs, files in os.walk(path, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    
    print (root)
    #for d in dirs:
    #  print ("Dir:", d)
    
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(include, f)]
    for fname in files:
      print (fname)
    
  return files
