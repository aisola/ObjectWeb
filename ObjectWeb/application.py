#!/usr/bin/python
################################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## @summary: This document creates the Application Object that is 
##           crucial for the Framework.
## maintainer: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
################################################################################

################################################################################
# Import Standard Libraries
################################################################################
import os
import re
import sys
import cgi

from wsgiref.simple_server import make_server
#from wsgiref.handlers import CGIHandler

################################################################################
# Import ObjectWeb
################################################################################
import webapi
import debug

################################################################################
# ObjectWeb Documentation
################################################################################
"""
ObjectWeb is a fast, minimalist, pure-Python web framework that relies on no 
third party libraries. It is designed around using Python as it was originally 
intended to be used: as an Object Oriented Programming language. ObjectWeb 
supports the CGI and WSGI 1.0 standards and has a built-in development server.

Normal Usage of the ObjectWeb library is as follows.

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


ObjectWeb can be used for many things. Feel free to include other libraries like
ORMs or Templating Engines to assist you in your development.

"""

################################################################################
# Classes
################################################################################
class Application(object):
    """
        This is the main interface between the webserver and the application.
    """
    
    def __init__(self,urlmap={},debug=False):
        """
            *THIS METHOD SHOULD NOT BE CALLED MANUALLY.*
            
            Initializes the Application Object.
            
            @param urlmap: *dict* This is a normal python dict who keys are
            python re strings that map to python objects that have at least a 
            function GET that handles the requests. The re strings can capture 
            sections of the urls by enclosing those sections in parentheses ().
            Those sections will be passed as arguments to the handler method 
            function.

            @param debug: *bool* This tells ObjectWeb whether or not to use the
            debugging facility.

            @return: Application Object.
        """
        self.urlmap = urlmap
        self.debug = debug
    
    def _match(self, rpath):
        """
            *THIS METHOD SHOULD NOT BE CALLED MANUALLY.*
             - Called by self.handle()
            
            Matches the request path to the object that should handle the
            requst and returns the object or None if no match exists.

            @param rpath: *str* The webserver request path.

            @return: The matched handler object + a list of prettyurl arguments 
            OR None if there was no match.
        """
        # Check each pattern key against the request path.
        if type(self.urlmap) == type({}):
            for pat, what in self.urlmap.iteritems():
                result = re.compile("^" + str(pat) + "$").match(str(rpath))

                # If there is a result, then we've matched a handler.
                # Return the handler object and the prettyurl arguments.
                if result:
                    return what, [x for x in result.groups()]

        elif type(self.urlmap) == type(()) or type(self.urlmap) == type([]):
            for patwhat in self.urlmap:
                pat    = patwhat[0]
                what   = patwhat[1]
                result = re.compile("^" + str(pat) + "$").match(str(rpath))

                # If there is a result, then we've matched a handler.
                # Return the handler object and the prettyurl arguments.
                if result:
                    return what, [x for x in result.groups()]

        # No match, return None.
        return None
    
    def _handle(self):
        """
            *THIS METHOD SHOULD NOT BE CALLED MANUALLY.*
             - Called by: wsgi()

            This method calls self._match() to find the handler then calls the 
            correct method (GET, POST, etc.) to handle the request.

            @return: The processed request's status and output.
        """
        # Get the HandlerObj
        HandlerObj = self._match(webapi.context["path"])

        # If the HandlerObj is not None then process it.
        if HandlerObj:
            # Create the instance and store the arguments.
            HandlerInst = HandlerObj[0]()
            args = HandlerObj[1]

            # If the HandlerObj has the method function available.
            if hasattr(HandlerInst, webapi.context["method"]):
                # Run the method, passing in the arguments. Capture the output.
                method_func = getattr(HandlerInst,webapi.context["method"])
                webapi.context["output"] = method_func(*args)

            # Otherwise throw an HTTP 405 Method Not Allowed.
            else:
                webapi.status("405 Method Not Allowed")
                # Check if the application has defined a 405 page...
                if "HTTP-405" in self.urlmap:
                    cls = self.urlmap["HTTP-405"]
                    HandlerInst = cls()
                    webapi.context["output"] = HandlerInst.GET()
                # If not, provide one.
                else:
                    webapi.context["output"] = "Method Not Allowed: The method used is not allowed for this resource."

        # The HandlerObj is None.
        else:
            webapi.status("404 Not Found")
            # Check if the application has defined a 405 page...
            if "HTTP-404" in self.urlmap:
                cls = self.urlmap["HTTP-404"]
                HandlerInst = cls()
                webapi.context["output"] = HandlerInst.GET()
            # If not, provide one.
            else:
                webapi.context["output"] = "Not Found: The requested URL was not found."

        # return the status & the output
        return webapi.context["status"], webapi.context["output"]
    
    def _load(self,env):
        """
            *THIS METHOD SHOULD NOT BE CALLED MANUALLY.*
             - Called by: wsgi()
            
            Loads the Application environment.

            @param env: *dict* A regular python dict that is recieved from the 
            webserver and holds the environment variables.

            @return: None
        """
        # Clean the slate.
        webapi.context.clear()

        # Set the default status.
        webapi.context["status"] = "200 OK"
        webapi.status("200 OK")

        # Initiate the headers, output, and environ
        webapi.context["headers"] = []
        webapi.context["output"] = ''
        webapi.context["environ"] = env

        # Set the host
        webapi.context["host"] = env.get('HTTP_HOST')

        # Set the HTTP Scheme.
        if env.get('wsgi.url_scheme') in ['http', 'https']:
            webapi.context["protocol"] = env['wsgi.url_scheme']
        elif env.get('HTTPS', '').lower() in ['on', 'true', '1']:
            webapi.context["protocol"] = 'https'
        else:
            webapi.context["protocol"] = 'http'

        # Set home domain, home path, and home
        webapi.context["homedomain"] = webapi.context["protocol"] + '://' + env.get('HTTP_HOST', '[unknown]')
        webapi.context["homepath"] = os.environ.get('REAL_SCRIPT_NAME', env.get('SCRIPT_NAME', ''))
        webapi.context["home"] = webapi.context["homedomain"] + webapi.context["homepath"]
        webapi.context["realhome"] = webapi.context["home"]

        # Set the Requester's IP, the Method, and the path.
        webapi.context["ip"] = env.get('REMOTE_ADDR')
        webapi.context["method"] = env.get('REQUEST_METHOD')
        webapi.context["path"] = env.get('PATH_INFO')

        # To fix empty-path bug.
        if webapi.context["path"] == None:
            webapi.context["path"] = "/"
        
        # get the requestvars if post/put
        if webapi.context["method"].lower() in ['post', 'put']:
                fp = env.get('wsgi.input')
                webapi.context["requestvars"] = cgi.FieldStorage(fp=fp, 
                                                            environ=env, 
                                                            keep_blank_values=1)
        
        # get the requestvars if get
        if webapi.context["method"].lower() == 'get':
            webapi.context["requestvars"] = cgi.FieldStorage(environ=env,
                                                            keep_blank_values=1)

        
        # convert all string values to unicode values and replace 
        # malformed data with a suitable replacement marker.
        for k, v in webapi.context.iteritems():
            if isinstance(v, str):
                webapi.context[k] = v.decode('utf-8', 'replace')
    
    def getwsgi(self,*middleware):
        """
            Creates a WSGI function that can be passed to a webserver run run. 
            It will add all *middleware to the function as well.
            
            @param *middleware: *object* Python WSGI Middleware-compliant 
            objects that passed as *args that will be applied as middleware to 
            the application.
            
            @return: a function that is callable by an external WSGI Server
            such as Apache + mod_wsgi.
        """
        # Create the function
        def wsgi(env, start_response):
            # Load the environment.
            self._load(env)

            # Handle the request & Recieve status + output
            if self.debug:
                try:
                    code, output = self._handle()
                except:
                    code = "500 Internal Error"
                    output = debug.debugerror()
            else:
                code, output = self._handle()

            # Get headers.
            headers = webapi.getheaders()

            # Send Complete WSGI request
            start_response(str(code),headers)
            return [str(output)]

        # Apply middleware.
        for mid in middleware:
            wsgi = mid(wsgi)

        # Return function
        return wsgi

    def getgoogleapp(self, *middleware):
        wsgiapp = self.getwsgi(*middleware)
        try:
            # check what version of python is running
            version = sys.version_info[:2]
            major   = version[0]
            minor   = version[1]

            if major != 2:
                raise EnvironmentError("Google App Engine only supports python 2.5 and 2.7")

            # if 2.7, return a function that can be run by gae
            if minor == 7:
                return wsgiapp
            # if 2.5, use run_wsgi_app
            elif minor == 5:
                from google.appengine.ext.webapp.util import run_wsgi_app
                return run_wsgi_app(wsgiapp)
            else:
                raise EnvironmentError("Not a supported platform, use python 2.5 or 2.7")
        except ImportError:
            return self.getcgi(*middleware)
    
    def getcgi(self,*middleware):
        """
            Creates a CGI run and producing CGI compatibility. It will add all 
            *middleware to the output as well.
            
            @param *middleware: *object* Python WSGI Middleware-compliant 
            objects that passed as *args that will be applied as middleware to 
            the application.
            
            @return: returns CGI compliant output.
        """
        return webapi.UnicodeCGIHandler().run(self.getwsgi(*middleware))
    
    def run(self,host="localhost",port=8080,*middleware):
        """
            Creates a development server binded to *host* and *port* and 
            producing the output. It will add all *middleware to the output as 
            well.
            
            @param host: *str* The host that the run should be bound to.
            
            @param port: *int* The port that the run should be bound to.
            
            @param *middleware: *object* Python WSGI Middleware-compliant 
            objects that passed as *args that will be applied as middleware to 
            the application.
            
            @return: None
        """
        httpd_wsgi = make_server(host,port,self.getwsgi(*middleware))
        try:
            httpd_wsgi.serve_forever()
        except KeyboardInterrupt:
            pass
