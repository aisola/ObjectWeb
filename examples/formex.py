#!/usr/bin/python
###############################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## summary: This document displays the exact markup for a simple form in
##          plain text.
## maintainer: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
###############################################################################

import ObjectWeb
import ObjectWeb.forms as forms

myform = forms.Form(
    forms.Textbox("username", label="Username"),
    forms.Password("password", label="Password"),

    forms.Submit("login", value="Login")
)


class MainPage(object):

    def GET (self):
        frm = myform()
        return frm.render()

    POST = GET
        

ObjectWeb.Application({
    "/": MainPage,
}).run(port=8080)
