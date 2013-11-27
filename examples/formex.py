import ObjectWeb
import ObjectWeb.form as forms

myform = forms.Form(
    forms.Textbox("username",label="Username"),
    forms.Password("password",label="Password"),
    forms.Button("login",value="Login",type="submit")
)

class MainPage(object):

    def GET (self):
        frm = myform()
        return frm.render()

    def POST(self):
        frm = myform()
        if not frm.validates():
            return "FAILED"
        else:
            print frm.username.get_value(), frm.password.get_value()
            return frm.username.get_value() + " " + frm.password.get_value()
        

ObjectWeb.Application({
    "/": MainPage,
}).run(port=8080)
