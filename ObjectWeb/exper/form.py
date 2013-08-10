#!/usr/bin/python
################################################################################
## @author: Abram C. Isola (Head Author)
## @organization: Abram C. Isola Development
## @contact: abram@isola.mn || http://abram.isola.mn/projects/ObjectWeb
## @license: LGPLv3 (See LICENSE)
## @summary: This document creates a standard, easy interface for form
##           processing.
################################################################################


################################################################################
# Import Standard Libraries
################################################################################
import copy


################################################################################
# Import ObjectWeb
################################################################################
import ObjectWeb.webapi as webapi


################################################################################
# ObjectWeb Form Helper Functions
################################################################################
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


################################################################################
# Form Class
################################################################################
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
                self.error = v.msg
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


################################################################################
# Input Base Class
################################################################################

class Input(object):
    def __init__(self, name, *validators, **attrs):
        self.name = name
        self.validators = validators
        self.attrs = attrs = AttributeList(attrs)
        
        self.label = attrs.pop('label', name)
        self.value = attrs.pop('value', None)
        self.error = None
        
        self.id = attrs.setdefault('id', self.get_default_id())
        
        if 'class_' in attrs:
            attrs['class'] = attrs['class_']
            del attrs['class_']
        
    def get_type(self):
        raise NotImplementedError
        
    def get_default_id(self):
        return self.name

    def validate(self, value):
        self.set_value(value)

        for v in self.validators:
            if not v.valid(value):
                self.error = v.msg
                return False
        return True

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def render(self):
        attrs = self.attrs.copy()
        attrs['type'] = self.get_type()
        if self.value is not None:
            attrs['value'] = self.value
        attrs['name'] = self.name
        return '<input %s/>' % attrs
        
    def addatts(self):
        # add leading space for backward-compatibility
        return " " + str(self.attrs)

# AttributeList Helper Class
class AttributeList(dict):
    def copy(self):
        return AttributeList(self)
        
    def __str__(self):
        return " ".join(['%s="%s"' % (k, v) for k, v in self.items()])
        
    def __repr__(self):
        return '<attrs: %s>' % repr(str(self))


