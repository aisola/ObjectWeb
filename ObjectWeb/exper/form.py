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
import re


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

        form_out += '<form method="POST" enctype="multipart/form-data">'
        
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

################################################################################
# Simple Input Subclasses
################################################################################
class Textbox(Input):
    def get_type(self):
        return 'text'

class Password(Input):    
    def get_type(self):
        return 'password'

class Hidden(Input):
    def get_type(self):
        return 'hidden'

class File(Input):
    def get_type(self):
        return 'file'

################################################################################
# Slightly-More-Complicated Input Subclasses
################################################################################
class Textarea(Input):
    def render(self):
        attrs = self.attrs.copy()
        attrs['name'] = self.name
        value = self.value or ''
        return '<textarea %s>%s</textarea>' % (attrs, value)

class Dropdown(Input):
    def __init__(self, name, args, *validators, **attrs):
        self.args = args
        super(Dropdown, self).__init__(name, *validators, **attrs)

    def render(self):
        attrs = self.attrs.copy()
        attrs['name'] = self.name
        
        x = '<select %s>\n' % attrs
        
        for arg in self.args:
            x += self._render_option(arg)

        x += '</select>\n'
        return x

    def _render_option(self, arg, indent='  '):
        if isinstance(arg, (tuple, list)):
            value, desc= arg
        else:
            value, desc = arg, arg 

        if self.value == value or (isinstance(self.value, list) and value in self.value):
            select_p = ' selected="selected"'
        else:
            select_p = ''
        return indent + '<option%s value="%s">%s</option>\n' % (select_p, value, desc)
        

class GroupedDropdown(Dropdown):
    def __init__(self, name, args, *validators, **attrs):
        self.args = args
        super(Dropdown, self).__init__(name, *validators, **attrs)

    def render(self):
        attrs = self.attrs.copy()
        attrs['name'] = self.name
        
        x = '<select %s>\n' % attrs
        
        for label, options in self.args:
            x += '  <optgroup label="%s">\n' % label
            for arg in options:
                x += self._render_option(arg, indent = '    ')
            x +=  '  </optgroup>\n'
            
        x += '</select>\n'
        return x

class Radio(Input):
    def __init__(self, name, args, *validators, **attrs):
        self.args = args
        super(Radio, self).__init__(name, *validators, **attrs)

    def render(self):
        x = '<span>'
        for arg in self.args:
            if isinstance(arg, (tuple, list)):
                value, desc= arg
            else:
                value, desc = arg, arg 
            attrs = self.attrs.copy()
            attrs['name'] = self.name
            attrs['type'] = 'radio'
            attrs['value'] = value
            if self.value == value:
                attrs['checked'] = 'checked'
            x += '<input %s/> %s' % (attrs, desc)
        x += '</span>'
        return x

class Checkbox(Input):
    def __init__(self, name, *validators, **attrs):
        self.checked = attrs.pop('checked', False)
        Input.__init__(self, name, *validators, **attrs)
        
    def get_default_id(self):
        value = self.value or ""
        return self.name + '_' + value.replace(' ', '_')

    def render(self):
        attrs = self.attrs.copy()
        attrs['type'] = 'checkbox'
        attrs['name'] = self.name
        attrs['value'] = self.value

        if self.checked:
            attrs['checked'] = 'checked'            
        return '<input %s/>' % attrs

    def set_value(self, value):
        self.checked = bool(value)

    def get_value(self):
        return self.checked

class Button(Input):
    def __init__(self, name, *validators, **attrs):
        super(Button, self).__init__(name, *validators, **attrs)
        self.description = ""

    def render(self):
        attrs = self.attrs.copy()
        attrs['name'] = self.name
        if self.value is not None:
            attrs['value'] = self.value
        html = attrs.pop('html', None) or self.name
        return '<button %s>%s</button>' % (attrs, html)

################################################################################
# Validators
################################################################################

class Validator:
    def __deepcopy__(self, memo): return copy.copy(self)
    def __init__(self, msg, test): webapi.autoassign(self, locals())
    def valid(self, value): 
        try: return self.test(value)
        except: return False

Required = Validator("Required", bool)

class RegExp(Validator):
    def __init__(self, rexp, msg):
        self.rexp = re.compile(rexp)
        self.msg = msg
    
    def valid(self, value):
        return bool(self.rexp.match(value))
