#!/usr/bin/python
################################################################################
## @author: Abram C. Isola
## @organization: Abram C. Isola Programming
## @contact: abram@isola.mn || http://abram.isola.mn/python/ObjectWeb
## @copyright: Copyright (C) 2013 Abram C. Isola. All rights reserved.
## @license: Undecided; So currently Closed Source.
## @summary: This document creates several helper functions and framework
##           utilities. 
################################################################################

import Cookie
import urllib
import itertools

# Create the Application config, context, and _getvars
global config, context, _getvars
config = {}
context = {}
_getvars = {}

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


# Functions
def getheaders():
    return context["headers"]

def header(field,value): context["headers"].append((field,value))
def status(stat): context["status"] = str(stat)

def setcookie(name, value, expires='', domain=None,
              secure=False, httponly=False, path=None):
    """Sets a cookie."""
    morsel = Cookie.Morsel()
    name, value = _safestr(name), _safestr(value)
    morsel.set(name, value, urllib.quote(value))
    if expires < 0:
        expires = -1000000000
    morsel['expires'] = expires
    morsel['path'] = path or context.homepath+'/'
    if domain:
        morsel['domain'] = domain
    if secure:
        morsel['secure'] = secure
    value = morsel.OutputString()
    if httponly:
        value += '; httponly'
    header('Set-Cookie', value)
    
def cookies():
    """Returns Cookies."""
    return context["environ"].get("HTTP_COOKIE", "")

def request_var(varname): return _getvars.get(varname)
