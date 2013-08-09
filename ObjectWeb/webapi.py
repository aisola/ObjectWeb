#!/usr/bin/python
################################################################################
## @author: Abram C. Isola (Head Author)
## @organization: Abram C. Isola Development
## @contact: abram@isola.mn || http://abram.isola.mn/projects/ObjectWeb
## @license: LGPLv3 (See LICENSE)
## @summary: This document creates several helper functions and framework
##           utilities. 
################################################################################

################################################################################
# Import Standard Libraries
################################################################################
import Cookie
import urllib
import itertools

import sys, codecs
from wsgiref.handlers import CGIHandler

# Create the Application config and context
global config, context
config = {}
context = {}

config["debug"] = False

################################################################################
# _safestr function from web.py
################################################################################
def _safestr(obj, encoding='utf-8'):
    r"""
    Converts any given object to utf-8 encoded string. 
    
        >>> safestr('hello')
        'hello'
        >>> safestr(u'\u1234')
        '\xe1\x88\xb4'
        >>> safestr(2)
        '2'
    """
    if isinstance(obj, unicode):
        return obj.encode(encoding)
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, 'next'): # iterator
        return itertools.imap(_safestr, obj)
    else:
        return str(obj)

################################################################################
# Unicode CGI Handler
################################################################################
class UnicodeCGIHandler(CGIHandler):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    _write = sys.stdout.write

################################################################################
# ObjectWeb Helper Functions
################################################################################
def getheaders():
    """
        Helper function that returns headers.
        
        @return: Returns all headers sent from the client.
    """
    return context["headers"]

def header(field, value):
    """
        Sets a header to be sent back to the client.
        
        @param field: *str* The header name.
        
        @param value: *str* The header value.
        
        @return: None
    """
    context["headers"].append((field,value))
    
def status(stat):
    """
        Sets the status to return to the client.
        
        @param stat: ( *str* | *ObjectWeb.response.** ) The response that will 
        be returned to the client.
        
        @return: None
    """
    context["status"] = str(stat)

def setcookie(name, value, expires='', domain=None,
              secure=False, httponly=False, path=None):
    """
        Sets an HTTP Cookie.
        
        @param name: *str* The Cookie name or identifier.
           
        @param value: *str* The Cookie value.
               
        @param expires: *str* The datetime that the Cookie should no longer be 
        valid. Default: ''
        
        @param domain: *str* The domain that the Cookie can be sent to. 
        Default: None
        
        @param secure: *bool* If the Cookie should be secure. Default: None
        
        @param httponly: *bool* IF the Cookie should be accessible solely via 
        HTTP. Default: False
        
        @param path: *str* The path that the Cookie can be sent to. 
        Default: None
                   
        @return: None
    """
    # Create the Cookie Object.
    morsel = Cookie.Morsel()
    # Set name and value.
    name, value = _safestr(name), _safestr(value)
    morsel.set(name, value, urllib.quote(value))

    # Set expiration datetime.
    if expires < 0:
        expires = -1000000000
    morsel['expires'] = expires

    # Set path
    morsel['path'] = path or ""

    # Set domain
    if domain:
        morsel['domain'] = domain
    
    # Set secure
    if secure:
        morsel['secure'] = secure

    # Get Cookie
    value = morsel.OutputString()

    # Set HTTP only
    if httponly:
        value += '; httponly'

    # Set Cookie
    header('Set-Cookie', value)
    
def cookies():
    """
        Gathers all recieved Cookies.
        
        @return: List of Cookies or None if none exist.
    """
    return context["environ"].get("HTTP_COOKIE", None)

def getvar(varname, default=None):
    """
        Returns the given HTTP parameter.

        @param varname: *str* The name of the HTTP parameter that should be 
        returned.
        
        @param default: *object* The object that should be returned if the HTTP 
        parameter does not exist.
        
        @return: The value of the HTTP parameter OR if provided, the value of 
        default OR if default is not provided, None.
    """
    return context["requestvars"].getfirst(varname, default=default)

request_var = getvar

def getvars(*args):
    """
        Returns the given HTTP parameter.
        
        @param *args: *tuple* The (name, default) pairs of the HTTP parameters 
        that should be returned.
        
        @return: The list of values of the HTTP parameter OR if provided, the 
        value of default OR if default is not provided, None.
    """
    # Get the params
    http_params = []
    for paramgrp in args:
        http_params.append(getvar(paramgrp[0]), paramgrp[0] or None)

    # return params
    return http_params
