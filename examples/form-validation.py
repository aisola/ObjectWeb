# -*- coding: utf-8 -*-
import ObjectWeb
import ObjectWeb.forms as forms

import re

def valid_email(form):
    if re.match(r"^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", form.email) != None:
      return True # this is an email.
    else:
      return False # this is not an email.

def passmatch(form):
    return form.password == form.password2

myform = forms.Form(
    
    forms.Textbox("email",label="Email"),
    forms.Password("password",label="Password"),
    forms.Password("password2",label="Confirm Password"),
    
    forms.Button("login",value="Login",type="submit"),
    validators = [
        forms.Validator("Email must be a valid email", valid_email),
        forms.Validator("Passwords must match.", passmatch)
    ]
    
)

class MainPage(object):
    
    def GET (self):
        ObjectWeb.header("Content-Type","text/html")
        frm = myform()
        return frm.render()
    
    def POST(self):
        ObjectWeb.header("Content-Type","text/html")
        frm = myform()
        if not frm.validates():
            return "FAILED: " + str(frm.password) + " " + str(frm.password2)
        else:
            return str(frm.username) + " " + str(frm.password)

ObjectWeb.Application({
    "/": MainPage,
}).run(port=8080)
