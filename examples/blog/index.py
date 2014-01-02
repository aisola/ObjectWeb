#!/usr/bin/python
################################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## summary: This document creates a VERY simple blogging software implementation
##          in ObjectWeb. This is NOT for production use.
## maintainer: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
################################################################################

import sys
sys.path.append("../../")

import ObjectWeb
from ObjectWeb import forms

import blogrec # import blog resources

NewPostForm = forms.Form(
    forms.Textbox("title", label="Title"),
    forms.Textarea("content", label="Content"),
    forms.Submit("submit", label="Submit"),
    validators = [
        forms.Validator("Title is Required.", lambda frm: bool(frm.title.get_value())),
        forms.Validator("Content is Required.", lambda frm: bool(frm.content.get_value()))
    ]
)

class MainPage(object):
    
    def GET(self):
        ObjectWeb.header("Content-Type","text/html")
        
        posts = blogrec.get_posts()

        if posts:
            content = ""
            for post in posts:
                content += "<div class='post' style='border: 1px solid #000;'>"
                content += "<h3>"+str(post.title)+"</h3>"
                content += "<section>%s</section>"  % post.content
                content += "</div>"
        else:
            content = "<div>There are no posts.</div>"
                
        return blogrec.display(content)

class NewPage(object):
    
    def GET(self):
        ObjectWeb.header("Content-Type","text/html")
        
        form = NewPostForm()
        return blogrec.display(form.render())

    def POST(self):
        ObjectWeb.header("Content-Type","text/html")
        form = NewPostForm()
        
        if form.validates():
            blogrec.set_post(blogrec.BlogPost(str(form.title),
                                            str(form.content)))
            ObjectWeb.seeother("/")
            return ""
        else:
            return blogrec.display(form.render())

ObjectWeb.Application({
    "/": MainPage,
    "/new": NewPage,
}).run(port=8080)
