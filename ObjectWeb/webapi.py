#!/usr/bin/python
################################################################################
## @author: Abram C. Isola (Head Author)
## @organization: Abram C. Isola Development
## @contact: abram@isola.mn || http://abram.isola.mn/projects/ObjectWeb
## @license: LGPLv3 (See LICENSE)
## @summary: This document creates several helper functions and framework
##           utilities. 
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

#############################################################################
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
############################################################################

#############################################################################
class UnicodeCGIHandler(CGIHandler):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    _write = sys.stdout.write
############################################################################

# Functions
def getheaders():
    """
        Returns all headers sent from the client.
    """
    return context["headers"]

def header(field,value):
    """
        Sets a header to be sent back to the client. both *field* and *value* 
        should be strings.
    """
    context["headers"].append((field,value))
    
def status(stat):
    """
        Sets the status to return to the client. *stat* can be a string or an 
        ObjectWeb response object from ObjectWeb.response.
    """
    context["status"] = str(stat)

def setcookie(name, value, expires='', domain=None,
              secure=False, httponly=False, path=None):
    """Sets a cookie."""
    morsel = Cookie.Morsel()
    name, value = _safestr(name), _safestr(value)
    morsel.set(name, value, urllib.quote(value))
    if expires < 0:
        expires = -1000000000
    morsel['expires'] = expires
    morsel['path'] = path or ""
    if domain:
        morsel['domain'] = domain
    if secure:
        morsel['secure'] = secure
    value = morsel.OutputString()
    if httponly:
        value += '; httponly'
    header('Set-Cookie', value)
    
def cookies():
    """Returns all Cookies."""
    return context["environ"].get("HTTP_COOKIE", "")

def request_var(varname,default=None):
    """
        Returns the HTTP variable *varname* using *default* if *varname* is 
        not present in the HTTP Variables.
    """
    return context["requestvars"].getfirst(varname, default=default)
