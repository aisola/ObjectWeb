ObjectWeb
=========
OOP Python Web Framework
------------------------

ObjectWeb is a fast, minimalist, pure-Python web framework that relies on no 
third party libraries. It is designed around using Python as it was originally 
intended to be used: as an Object Oriented Programming language. ObjectWeb 
supports the CGI and WSGI standards and has a built-in development server.

The ObjectWeb Framework has only been tested and developed with Python 2.7.

### Features

+ There is currently no reliance on third party libraries.
+ Map your URLS to request paths using regular expressions.
+ Easily extract information from the request.
+ *Experimental* form processing and validation module.

### Known Issues

1. In the *experimental* module `ObjectWeb.exper.form`, validation does not yet 
   work. However, it is still very good at the creation of forms and retrieving 
   data from forms.
2. The debug operation does not really work...
3. There is no real documentation... Yet.

### Documentation
Documentation is currently being developed for ObjectWeb. However there are 
some examples in the examples directory.

### Installation
    git clone https://github.com/aisola/ObjectWeb.git
    cd ObjectWeb
    sudo python setup.py install    
