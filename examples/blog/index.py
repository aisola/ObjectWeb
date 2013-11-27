# -*- coding: utf-8 -*-

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
        ObjectWeb.header("Content-Type","text/html;charset=utf-8")
        
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
        ObjectWeb.header("Content-Type","text/html;charset=utf-8")
        
        form = NewPostForm()
        return blogrec.display(form.render())

    def POST(self):
        ObjectWeb.header("Content-Type","text/html;charset=utf-8")
        form = NewPostForm()
        
        if form.validates():
            blogrec.set_post(blogrec.BlogPost(form.title.get_value(),
                                            form.content.get_value()))
            ObjectWeb.status(ObjectWeb.SeeOther("/"))
            return ""
        else:
            return blogrec.display(form.render())

ObjectWeb.Application({
    "/": MainPage,
    "/new": NewPage,
}).run(port=8080)
