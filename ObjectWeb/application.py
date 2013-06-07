#!/usr/bin/python
################################################################################
## @author: Abram C. Isola
## @organization: Abram C. Isola Programming
## @contact: abram@isola.mn || http://abram.isola.mn/python/ObjectWeb
## @copyright: Copyright (C) 2013 Abram C. Isola. All rights reserved.
## @license: Undecided; So currently Closed Source.
## @summary: This document creates the Application Object that is 
##           crucial for the Framework.
################################################################################
import os
import re
import cgi

import webapi
import response
from wsgiref.simple_server import make_server
#from wsgiref.handlers import CGIHandler

class Application(object):
    
    def __init__(self,urlmap={},debug=False):
        self.urlmap = urlmap
        self.debug = debug
    
    def _match(self, value):
        for pat, what in self.urlmap.iteritems():
            result = re.compile("^" + str(pat) + "$").match(str(value))
            
            if result: # it's a match
                return what, [x for x in result.groups()]
        
        return None
    
    def handle(self):
        urlmatch = self._match(webapi.context["path"])
        
        if urlmatch:
            inst = urlmatch[0]()
            args = urlmatch[1]
            if hasattr(inst, webapi.context["method"]):
                func = getattr(inst,webapi.context["method"])
                webapi.context["output"] = func(*args)
            else:
                webapi.status(response.MethodNotAllowed())
                if "HTTP-405" in self.urlmap:
                    cls = self.urlmap["HTTP-405"]
                    inst = cls()
                    webapi.context["output"] = inst.GET()
                else:
                    webapi.context["output"] = "Method Not Allowed: The method used is not allowed for this resource."
        else:
            webapi.status(response.NotFound())
            if "HTTP-404" in self.urlmap:
                cls = self.urlmap["HTTP-404"]
                inst = cls()
                webapi.context["output"] = inst.GET()
            else:
                webapi.context["output"] = "Not Found: The requested URL was not found."
        return webapi.context["status"], webapi.context["output"]
    
    def load(self,env):
        ctx = webapi.context
        ctx.clear()
        ctx["status"] = "200 OK"
        webapi.status(response.OK())
        ctx["headers"] = []
        ctx["output"] = ''
        ctx["environ"] = env
        ctx["host"] = env.get('HTTP_HOST')
        
        if env.get('wsgi.url_scheme') in ['http', 'https']:
            ctx["protocol"] = env['wsgi.url_scheme']
        elif env.get('HTTPS', '').lower() in ['on', 'true', '1']:
            ctx["protocol"] = 'https'
        else:
            ctx["protocol"] = 'http'
        
        ctx["homedomain"] = ctx["protocol"] + '://' + env.get('HTTP_HOST', '[unknown]')
        ctx["homepath"] = os.environ.get('REAL_SCRIPT_NAME', env.get('SCRIPT_NAME', ''))
        ctx["home"] = ctx["homedomain"] + ctx["homepath"]
        ctx["realhome"] = ctx["home"]
        ctx["ip"] = env.get('REMOTE_ADDR')
        ctx["method"] = env.get('REQUEST_METHOD')
        ctx["path"] = env.get('PATH_INFO')
        
        if ctx["path"] == None:
            ctx["path"] = "/"
        
        # get the requestvars if post/put
        if ctx["method"].lower() in ['post', 'put']:
                fp = env.get('wsgi.input')
                ctx["requestvars"] = cgi.FieldStorage(fp=fp, environ=env, keep_blank_values=1)
        
        # get the requestvars if get
        if ctx["method"].lower() == 'get':
            ctx["requestvars"] = cgi.FieldStorage(environ=env, keep_blank_values=1)
        
        for k, v in ctx.iteritems():
            # convert all string values to unicode values and replace 
            # malformed data with a suitable replacement marker.
            if isinstance(v, str):
                ctx[k] = v.decode('utf-8', 'replace')
    
    def getwsgi(self,*middleware):
        
        def wsgi(env,start_response):
            self.load(env)
            code, output = self.handle()
            headers = webapi.getheaders()
            start_response(str(code),headers)
            return [output]
        
        for mid in middleware:
            wsgi = mid(wsgi)
        
        return wsgi
    
    def getcgi(self,*middleware):
        """
        Return a CGI handler.
        """
        return webapi.UnicodeCGIHandler().run(self.getwsgi(*middleware))
    
    def run(self,host="localhost",port=80,*middleware):
        httpd_wsgi = make_server(host,port,self.getwsgi(*middleware))
        try:
            httpd_wsgi.serve_forever()
        except KeyboardInterrupt:
            pass
