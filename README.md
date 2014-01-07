ObjectWeb: OOP Python Web Framework
-----------------------------------

ObjectWeb is a fast, minimalist, pure-Python web framework that relies on no 
third party libraries. It is designed around using Python as it was originally 
intended to be used: as an Object Oriented Programming language. ObjectWeb 
supports the CGI and WSGI standards and has a built-in development server.

The ObjectWeb Framework has only been tested and developed with Python 2.7.

**ObjectWeb is BETA SOFTWARE and should be treated as such. Please use with caution and care.**
Make sure to read the LICENSE.

[![Build Status](https://travis-ci.org/aisola/ObjectWeb.png?branch=master)](https://travis-ci.org/aisola/ObjectWeb)

### Features
+ Pure Python 2.6/2.7 with reliance on third party libraries.
+ Supports CGI and WSGI standards. (&& Google App Engine... Maybe.)
+ A nice debug feature to help with 500 Internal Errors.
+ Allows the use of external libraries without interfering.
+ Map your URLS to request paths using regular expressions.
+ Easily extract information from the request.
+ Form API - form processing and validation module.
+ Built-in **development** server.

### Documentation
Documentation is ready! I must admit it is pretty terrible documentation, but it 
does the trick for most Python developers. As always contact me if you have 
suggestions for the documentation *OR* better yet, how about contributing to the 
documentation!

The documentation, for development purposes is not included in the library itself.

Get the documentation from [ObjectWebDocs](https://github.com/aisola/ObjectWebDocs)

### ObjectWeb in a Nutshell
General Usage of the ObjectWeb library is as follows.

    import ObjectWeb  # import the library.

    class MainPage(object): # Any object can be a handler
        "The main page hadler."

        def GET(self):
            "The GET method handler."
            return "Output content here..."

        # Make the POST method mimic the GET method.
        POST = GET
        
    # Create the Application Object.
    app = ObjectWeb.Appliation({
        "/": MainPage,              # Point the / path to be handled by MainPage
    }, debug=False)                 # Set debug to False for production.

### Installation
    git clone https://github.com/aisola/ObjectWeb.git
    cd ObjectWeb
    sudo python setup.py install

### Legal

Object Web is licensed under the GNU Lesser General Public License v3.
    
    ObjectWeb Python Web Framework
    Copyright (C) 2013, Abram C. Isola.

    This library is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    GNU Lesser General Public License for more details.
	
    You should have received a copy of the GNU Lesser General Public 
    License along with this library.  If not, see 
    <http://www.gnu.org/licenses/>.
