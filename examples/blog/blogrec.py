#!/usr/bin/python
###############################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## summary: Non-ObjectWeb resources for the blog. Enjoy.
## maintainer: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
###############################################################################

import time
import pickle


def display(content):
    return """
        <html>
            <head>
                <title>ObjectWeb Blog</title>
            </head>
            <body>
                <header>
                    <h1>ObjectWeb Blog</h1>
                    <a href="/" target="_self">Home</a> |
                    <a href="/new" target="_self">New</a>
                </header>
                <div id="content">
    """ + str(content) + """
                </div>
                <footer>
                    This "Blog Software" is completely GPLv3 and not
                    recommended for production use.
                </footer>
            </body>
        </html>
    """


class BlogPost(object):
    
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created = time.time()
        

def get_posts(limit=None):
    try:
        datfile = open("blog.dat", "rb")
        pickled = datfile.read()
        datfile.close()
        
        posts = pickle.loads(pickled)
    
        if limit:
            return posts[:limit]
        else:
            return posts
    except:
        return None


def set_post(postobj):
    datfile = open("blog.dat", "wb+")
    try:
        pickled = datfile.read()
        posts = [postobj] + pickle.loads(pickled)
    except:
        posts = [postobj]
    
    datfile.write(pickle.dumps(posts))
    datfile.close()
