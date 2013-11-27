# -*- coding: utf-8 -*-
import ObjectWeb
import ObjectWeb.forms as forms

def passmatch(form):
    return form.password.get_value() == form.password2.get_value()

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
        frm = myform()
        return frm.render()

    def POST(self):
        ObjectWeb.header("Content-Type","text/html;chatset=utf-8")
        frm = myform()
        if not frm.validates():
            return "FAILED: " + str(frm.password.get_value()) + " " + str(frm.password2.get_value())
        else:
            return frm.username.get_value() + " " + frm.password.get_value()

ObjectWeb.Application({
    "/": MainPage,
}, debug=True).run(port=8080)
