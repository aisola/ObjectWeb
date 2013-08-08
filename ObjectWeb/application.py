#!/usr/bin/python
################################################################################
## @author: Abram C. Isola (Head Author)
## @organization: Abram C. Isola Development
## @contact: abram@isola.mn || http://abram.isola.mn/projects/ObjectWeb
## @license: LGPLv3 (See LICENSE)
## @summary: This document creates the Application Object that is 
##           crucial for the Framework.
################################################################################
import os
import re
import cgi
import cgitb

import webapi
import response
from wsgiref.simple_server import make_server
#from wsgiref.handlers import CGIHandler

class Application(object):
    """
        Creates the main interface from the server to the Python code.
    """
    
    def __init__(self,urlmap={},debug=False):
        """
            *urlmap* should be a normal dict that maps a string that contains the
            path (regular expression) as a key that maps to the name of a normal 
            object that has HTTP Methods as functions that will be called on each
            method.
            
            EXAMPLE:
                import ObjectWeb
                
                class MainPage(object):
                    def GET(self):
                        ObjectWeb.header("Content-Type","text/html;charset=utf-8")
                        return "<p>Hello, World!</p>"
                
                urls = {"/":MainPage}
                
                application = ObjectWeb.Application(urlmap=urls, debug=False)
                application.run()
            
            *debug* when set to True, debug mode will be activated.
        """
        self.urlmap = urlmap
        self.debug = debug
        
        if self.debug == True:
            cgitb.enable()
    
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
        """
            Returns a function that is callable by an external WSGI Server such as
            Apache + mod_wsgi. It will add all *middleware to the function as well.
        """
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
            Creates a CGI run and producing CGI compatibility. It will add all 
            *middleware to the output as well.
        """
        return webapi.UnicodeCGIHandler().run(self.getwsgi(*middleware))
    
    def run(self,host="localhost",port=80,*middleware):
        """
            Creates a development server binded to *host* and *port* and producing 
            the output. It will add all *middleware to the output as well.
        """
        httpd_wsgi = make_server(host,port,self.getwsgi(*middleware))
        try:
            httpd_wsgi.serve_forever()
        except KeyboardInterrupt:
            pass
