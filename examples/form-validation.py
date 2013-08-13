# -*- coding: utf-8 -*-
import ObjectWeb
import ObjectWeb.exper.forms as forms

def passmatch(form):
    return form.password == form.password2

myform = forms.Form(
    forms.Textbox("username",label="Username"),
    forms.Password("password",label="Password"),
    forms.Password("password2",label="Confirm Password"),
    forms.Button("login",value="Login",type="submit"),
    validators = [
        forms.Validator("Passwords must match.", passmatch)
    ]
)

class MainPage(object):

    def GET (self):
        ObjectWeb.header("Content-Type","text/html;chatset=utf-8")
        return myform.render()

    def POST(self):
        ObjectWeb.header("Content-Type","text/html;chatset=utf-8")
        if not myform.validates():
            return "FAILED: " + str(myform.password) + " " + str(myform.password2)
        else:
            return myform.username + " " + myform.password

ObjectWeb.Application({
    "/": MainPage,
}, debug=True).run(port=8080)
