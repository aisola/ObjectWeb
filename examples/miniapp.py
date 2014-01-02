#!/usr/bin/python -O 
import ObjectWeb

class MainPage(object):
    
    def GET(self):
        # ObjectWeb.status("200 OK")
        ObjectWeb.header("Content-Type", "text/plain")
        
        return "Hello World!"

class NamePage(object):
    
    def GET(self, name):
        ObjectWeb.header("Content-Type", "text/plain")
        
        age = ObjectWeb.get("age", None)
        
        if age:
            return "Hello "+str(name)+", you are "+str(age[0])+" years old."
        else:
            return "Hello "+str(name)+"!"

class E404Page(object):
    
    def GET(self):
        ObjectWeb.status("404 Not Found")
        ObjectWeb.header("Content-Type", "text/plain")
        
        return "404 Not Found"

app = ObjectWeb.Application({
    "/": MainPage,
    "/([a-zA-Z0-9_]+)": NamePage,
    "HTTP-404": E404Page,
})

if __name__ == "__main__":
    app.run("localhost",8080)
else:
    application = app.getwsgi()

