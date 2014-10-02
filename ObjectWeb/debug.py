# -*- coding: utf-8 -*-

import sys, pprint
from cgi import escape

import webapi

page_css = """html * {padding:0; margin:0;} body * {padding:10px 20px;} body * * {padding:0;} body {font:small sans-serif;}
body>div {border-bottom:1px solid #ddd;} h1 {font-weight:normal;} h2 {margin-bottom:.8em;} h2 span {font-size:80%;
color:#666; font-weight:normal;} h3 { margin:1em 0 .5em 0; } h4 {margin:0 0 .5em 0; font-weight: normal;} table {border:1px solid #ccc;
border-collapse: collapse; background:white;} tbody td, tbody th {vertical-align:top; padding:2px 3px;} thead th {padding:1px 6px 1px 3px;
background:#fefefe; text-align:left; font-weight:normal; font-size:11px; border:1px solid #ddd;} tbody th { text-align:right;
color:#666; padding-right:.5em;} table.vars {margin:5px 0 2px 40px;} table.vars td, table.req td {font-family:monospace;}
table td.code {width:100%;} table td.code div {overflow:hidden;} table.source th {color:#666;} table.source td {font-family:monospace;
white-space:pre; border-bottom:1px solid #eee;} ul.traceback {list-style-type:none;} ul.traceback li.frame {margin-bottom:1em;}
div.context {margin: 10px 0;} div.context ol {padding-left:30px; margin:0 10px; list-style-position: inside;}
div.context ol li {font-family:monospace; white-space:pre; color:#666; cursor:pointer;} div.context ol.context-line li {color:black;
background-color:#ccc;} div.context ol.context-line li span {float: right;} div.commands {margin-left: 40px;}
div.commands a {color:black; text-decoration:none;} #summary {background: #ffc;} #summary h2 {font-weight: normal;
color: #666;} #explanation {background:#eee;} #template, #template-not-exist {background:#f6f6f6;}
#template-not-exist ul {margin: 0 0 0 20px;} #traceback {background:#eee;} #requestinfo {background:#f6f6f6;
padding-left:120px;} #summary table {border:none; background:transparent;} #requestinfo h2, #requestinfo h3 {position:relative;
margin-left:-100px;} #requestinfo h3 {margin-bottom:-1em;} .error {background: #ffc;} .specific {color:#cc3300; font-weight:bold;}
"""

page_js = """
function getElementsByClassName(oElm, strTagName, strClassName){var arrElements = (strTagName == "*" && document.all)? document.all :
oElm.getElementsByTagName(strTagName);var arrReturnElements = new Array();strClassName = strClassName.replace(/\-/g, "\\-");
var oRegExp = new RegExp("(^|\\s)" + strClassName + "(\\s|$$)");var oElement;for(var i=0; i<arrElements.length; i++){
oElement = arrElements[i];if(oRegExp.test(oElement.className)){arrReturnElements.push(oElement);}}return (arrReturnElements)}
function hideAll(elems) {for (var e = 0; e < elems.length; e++) {elems[e].style.display = 'none';}}
window.onload = function() {hideAll(getElementsByClassName(document, 'table', 'vars'));
hideAll(getElementsByClassName(document, 'ol', 'pre-context'));hideAll(getElementsByClassName(document, 'ol', 'post-context'));}
function toggle() {for (var i = 0; i < arguments.length; i++) {var e = document.getElementById(arguments[i]);
if (e) {e.style.display = e.style.display == 'none' ? 'block' : 'none';}} return false;}
function varToggle(link, id) {toggle('v' + id);var s = link.getElementsByTagName('span')[0];var uarr = String.fromCharCode(0x25b6);
var darr = String.fromCharCode(0x25bc);s.innerHTML = s.innerHTML == uarr ? darr : uarr;return false;}
"""

error_template_start = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta name="robots" content="NONE,NOARCHIVE" />
  <title>ObjectWeb Internal Error Debugging</title>
  <style type="text/css">
        %s
  </style>
  <script type="text/javascript">
  //<!--
        %s
    //-->
  </script>
</head>
<body>""" % (page_css, page_js)

error_template_end = """
<div id="explanation">
  <p>
    You're seeing this error because you have your <code>Application</code> 
    instance's debug option set to <code>True</code>. Set that to 
    <code>False</code> if you don't want to see this.
  </p>
</div>

</body>
</html>
"""


def _get_lines_from_file(filename, lineno, context_lines):
    """
    Returns context_lines before and after lineno from file.
    Returns (pre_context_lineno, pre_context, context_line, post_context).
    """
    try:
        source = open(filename).readlines()
        lower_bound = max(0, lineno - context_lines)
        upper_bound = lineno + context_lines

        pre_context = [line.strip('\n') for line in source[lower_bound:lineno]]
        context_line = source[lineno].strip('\n')
        post_context = [line.strip('\n')
                        for line in source[lineno + 1:upper_bound]]

        return lower_bound, pre_context, context_line, post_context
    except (OSError, IOError, IndexError):
        return None, [], None, []    


def prettify(x):
    try: 
        out = pprint.pformat(x)
    except Exception, e: 
        out = '[could not display: <' + e.__class__.__name__ + ': '+str(e)+'>]'
    return out


def dicttable_items(items, kls="req"):
    if items:
        out = '<table class="%s"><thead><tr><th>Variable</th>' \
              '<th>Value</th>' % kls
        out += '</tr></thead><tbody>'

        for k, v in items:
            out += '<tr><td>%s</td>' % escape(k)
            out += '<td class="code"><div>%s</div></td></tr>' % \
                   escape(prettify(v))
        out += "</tbody></table>"
    else:
        out = "<p>No data.</p>"
    return out


def dicttable (d, kls="req"):
    items = d and d.items() or []
    items.sort()
    return dicttable_items(items, kls)


def debugerror():    
    exception_type, exception_value, tback = sys.exc_info()
    frames = []
    while tback is not None:
        filename = tback.tb_frame.f_code.co_filename
        function = tback.tb_frame.f_code.co_name
        lineno = tback.tb_lineno - 1
    
        # hack to get correct line number for templates
        lineno += tback.tb_frame.f_locals.get("__lineoffset__", 0)
        
        pre_context_lineno, pre_context, context_line, post_context = \
            _get_lines_from_file(filename, lineno, 7)
    
        if '__hidetraceback__' not in tback.tb_frame.f_locals:
            frames.append({
                'tback': tback,
                'filename': filename,
                'function': function,
                'lineno': lineno,
                'vars': tback.tb_frame.f_locals,
                'id': id(tback),
                'pre_context': pre_context,
                'context_line': context_line,
                'post_context': post_context,
                'pre_context_lineno': pre_context_lineno,
            })
        tback = tback.tb_next
    frames.reverse()

    out = """<div id="summary">
      <h1>%(exception_type)s at %(context_path)s</h1>
      <h2>%(exception_value)s</h2>
      <table><tr>
        <th>Python</th>
        <td>%(frame_file)s in %(frame_func)s line %(frame_line)s</td>
      </tr><tr>
        <th>Web</th>
        <td>%(context_method)s %(context_home)s%(context_path)s</td>
      </tr></table>
    </div>
    <div id="traceback">
    <h2>Traceback <span>(innermost first)</span></h2>
    <ul class="traceback">
    """ % {
        "exception_type": escape(exception_type.__name__),
        "exception_value": exception_value,
        "context_home": escape(webapi.context["home"]),
        "context_path": escape(webapi.context["path"]),
        "context_method": escape(webapi.context["method"]),
        "frame_file": escape(frames[0]["filename"]),
        "frame_func": escape(frames[0]["function"]),
        "frame_line": frames[0]["lineno"]
    }
    
    for frame in frames:
        out += """<li class="frame"><code>%s</code> in <code>%s</code>""" % \
               (escape(frame["filename"]), escape(frame["function"]))

        if frame["context_line"] is not None:
            out += '<div class="context" id="c%s">' % frame["id"]
            if frame["pre_context"]:
                out += """<ol start="%s" class="pre-context" id="pre%s">""" % \
                       (frame["pre_context_lineno"], frame["id"])
                for line in frame["pre_context"]:
                    out += """<li onclick="toggle('pre%(frameid)s',
                    'post%(frameid)s')">%(line)s</li>
                    """ % {"frameid": frame["id"], "line": escape(line)}

                out += "</ol>"
                out += """<ol start="%s" class="context-line">
                <li onclick="toggle('pre%s', 'post%s')">%s
                </li></ol>
                """ % (frame["lineno"], frame["id"],
                       frame["id"], frame["context_line"])
                  
            if frame["post_context"]:
                out += """<ol start="%s" class="post-context"
                id="post%s">""" % (frame["lineno"] + 1, frame["id"])
                
                for line in frame["post_context"]:
                    out += """<li onclick="toggle('pre%s',
                    'post%s')">%s</li>
                    """ % (frame["id"], frame["id"],
                           escape(frame["context_line"]))
                out += "</ol>"
            out += "</div>"
        
        if frame["vars"]:
            out += """<div class="commands"><a href='#'
            onclick="return varToggle(this, '%s')"><span>&#x25b6;</span>
            Local vars</a></div>""" % frame["id"]
            out += dicttable(frame["vars"], kls='vars')
        out += "</li>"
    
    out += '</ul></div><div id="requestinfo">'
    
    if webapi.context["output"] or webapi.context["headers"]:
        out += """<h2>Response so far</h2> <h3>HEADERS</h3>"""
        out += dicttable(dict(webapi.getheaders()))
        out += '<h3>BODY</h3><p class="req" style="padding-bottom: 2em"><code>'
        out += str(escape(webapi.context["output"])) + "</code></p>"
      
    out += '<h2>Request information</h2>'
    out += '<h3>INPUT</h3>'
    out += dicttable(webapi.getall())
    out += '<h3 id="cookie-info">COOKIES</h3>'
    out += dicttable(webapi.cookies())
        
    out += '<h3 id="meta-info">META</h3>'

    newctx = [(k, v) for (k, v) in webapi.context.iteritems()
              if not k.startswith('_') and not isinstance(v, dict)]
    out += dicttable(dict(newctx))
    
    out += '<h3 id="meta-info">ENV</h3>'
    out += dicttable(webapi.context["environ"]) + '</div>'

    return error_template_start + out + error_template_end


class _Index:
    def GET(self):
        pass  # lint:ok

if __name__ == "__main__":
    from application import Application
    app = Application({
        "/": _Index
    }, debug=True)

    app.run()
