#!/usr/bin/python
################################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## summary: This document displays an example form with working validation.
## maintainer: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
################################################################################
import ObjectWeb
import ObjectWeb.forms as forms

import re

def valid_email(form):
    if re.match(r"^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", str(form.email)) != None:
      return True # this is an email.
    else:
      return False # this is not an email.

def passmatch(form):
    return form.password == form.password2

myform = forms.Form(
    
    forms.Textbox("email",label="Email"),
    forms.Password("password",label="Password"),
    forms.Password("password2",label="Confirm Password"),
    
    forms.Submit("login",value="Login"),
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
            return "FAILED"
        else:
            return str(frm.email) + " " + str(frm.password)

ObjectWeb.Application({
    "/": MainPage,
}, debug=True).run(port=8080)
