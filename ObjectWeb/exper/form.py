#!/usr/bin/python
################################################################################
## @author: Abram C. Isola (Head Author)
## @organization: Abram C. Isola Development
## @contact: abram@isola.mn || http://abram.isola.mn/projects/ObjectWeb
## @license: LGPLv3 (See LICENSE)
## @summary: This document creates a standard, easy interface for form
##           processing.
################################################################################

import copy

import ObjectWeb.webapi as webapi

def attrget(obj, attr, value=None):
    try:
        if hasattr(obj, 'has_key') and obj.has_key(attr): 
            return obj[attr]
    except TypeError:
        # Handle the case where has_key takes different number of arguments.
        # This is the case with Model objects on appengine. See #134
        pass
    if hasattr(obj, attr):
        return getattr(obj, attr)
    return value

class Form(object):
    
    def __init__(self, *inputs, **kwargs):
        self.inputs = inputs
        self.valid = True
        self.error = ''
        self.validators = kwargs.pop('validators', [])
        self.form_id = kwargs.pop('form_id', None)

    def __call__(self, x=None):
        o = copy.deepcopy(self)
        if x: o.validates(x)
        return o

    def render(self):
        form_out = ''
        if self.form_id:
            form_out += '<div id="%s" class="ow_form">' % (str(self.form_id),)
        else:
            form_out += '<div class="ow_form">\n'

        form_out += '<form method="POST" enctype="application/x-www-form-urlencoded">'
        
        form_out += '<div class="form_error">%s</div>' % self.error
        
        for i in self.inputs:
            form_out += '<div class="form_elem_wrap">'
            form_out += '<div class="form_label"><label for="%s">%s</label></div>' % (i.id, i.label)
            form_out += '<div class="form_input">%s</div>' % (i.render(),)
            form_out += '</div>'

        form_out += "</form></div>"
        return form_out

    def validates(self, source=None, _validate=True, **kw):
        source = source or kw or webapi.getallvars()
        out = True
        for i in self.inputs:
            v = attrget(source, i.name)
            if _validate:
                out = i.validate(v) and out
            else:
                i.set_value(v)
        if _validate:
            out = out and self._validate(source)
            self.valid = out
        return out

    def _validate(self, value):
        self.value = value
        for v in self.validators:
            if not v.valid(value):
                self.note = v.msg
                return False
        return True

    def fill(self, source=None, **kw):
        return self.validates(source, _validate=False, **kw)

    def __getattr__(self, name):
        # don't interfere with deepcopy
        inputs = self.__dict__.get('inputs') or []
        for x in inputs:
            if x.name == name: return x
        raise AttributeError, name

    def get(self, i, default=None):
        try:
            return self.inputs[i]
        except KeyError:
            return default
