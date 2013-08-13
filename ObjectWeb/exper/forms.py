#!/usr/bin/python
################################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## @summary: This document creates a standard, easy interface for form
##           processing.
## maintainer: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
################################################################################


################################################################################
# Import ObjectWeb
################################################################################
import ObjectWeb.webapi as webapi

################################################################################
# Form Class
################################################################################

class Form(object):
    
    def __init__(self, *fields, **kwargs):
        self.fields = fields
        self.validators = kwargs.pop("validators", [])
        self.formid = kwargs.pop("formid", None)
        self.error = None
        self.valid = True

    def __getattr__(self, name):
        for field in self.fields:
            if field.name == name:
                return field
        raise AttributeError, name
    
    def render(self):
        if self.formid:
            formout = '<form id="%s" method="POST" enctype="multipart/formdata">' % (self.formid,)
        else:
            formout = '<form method="POST" enctype="multipart/formdata">'
        
        if self.error:
            formout += '<div class="form-error">%s</div>'

        for field in self.fields:
            formout += '<div class="form-element">'
            
            if field.show_label():
                formout += '<div class="form-element-label">'
                formout += '<label for="%s">%s</label>' % (field.id, field.label)
                formout += '</div>'
            
            formout += '<div class="form-element-field">%s</div>' % (field.render(),)

            formout += '</div><!-- .form-element -->'

        formout += '</form>'
        return formout


    def validates(self, source=None):
        self.valid = True

        for field in self.fields:
            if source:
                fieldval = source.get(field.name)
            else:
                fieldval = webapi.getvar(field.name)
            field.set_value(fieldval)

        self.valid = self.valid and self._validate()
        return self.valid

    def _validate(self):
        for val in self.validators:
            if not val.valid(self):
                self.error = val.message
                return False
        return True

################################################################################
# Field Class
################################################################################

class Field(object):
    
    def __init__(self, name, **attrs):
        self.name = name
        self.attrs = webapi.AttributeList(attrs)
        
        self.label = self.attrs.pop("label", self.name)
        self.value = self.attrs.pop("value", None)
        self.id = self.attrs.pop("id", self.default_id())

        if "class_" in self.attrs:
            self.attrs["class"] = self.attrs["class_"]
            del self.attrs["class_"]
            del attrs["class_"]

    def default_id(self):
        return self.name

    def field_type(self):
        raise NotImplementedError

    def show_label(self):
        return True

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def render(self):
        attrs = self.attrs.copy()
        attrs["type"] = self.get_type()
        
        if self.value is not None:
            attrs["value"] = self.value
            
        attrs["name"] = self.name

        return '<input %s />' % attrs

################################################################################
# Simple Field Subclasses
################################################################################
class Textbox(Field):
    def get_type(self):
        return 'text'

class Password(Field):    
    def get_type(self):
        return 'password'

class File(Field):
    def get_type(self):
        return 'file'

class Hidden(Field):
    def show_label(self):
        return False
        
    def get_type(self):
        return 'hidden'

################################################################################
# Slightly-Less-Simple Field Subclasses
################################################################################
class Textarea(Field):
    
    def render(self):
        attrs = self.attrs.copy()
        attrs['name'] = self.name
        return '<textarea %s>%s</textarea>' % (attrs, self.value or '')

class Dropdown(Field):
    
    def __init__(self, name, options, **attrs):
        self.options = options
        super(Dropdown, self).__init__(name, **attrs)
        
    def render(self):
        attrs = self.attrs.copy()
        attrs["name"] = self.name
        
        out = '<select %s>' % attrs

        for option in self.options:
            out += self.render_option(option)

        out += '</select>'
        return out

    def render_option(self, option):
        if isinstance(option, tuple) or isinstance(option, list):
            desc, value = option
        else:
            desc, value = option, option

        if self.value == value or (isinstance(self.value, list) and value in self.value):
            select_p = ' selected="selected"'
        else:
            select_p = ''
        return '<option%s value="%s">%s</option>\n' % (select_p, value, desc)

class GroupedDropdown(Dropdown):
    
    def __init__(self, name, options, **attrs):
        self.options = options
        super(GroupedDropdown, self).__init__(self, name, **attrs)

    def render(self):
        attrs = self.attrs.copy()
        attrs['name'] = self.name
        
        out = '<select %s>' % attrs
        
        for label, options in self.options:
            out += '<optgroup label="%s">' % label
            for option in options:
                out += self.render_option(option)
            out +=  '</optgroup>'
            
        out += '</select>'
        return out

class Radio(Field):
    
    def __init__(self, name, options, **attrs):
        super(Radio, self).__init__(name, **attrs)

    def get_type(self):
        return 'radio'

    def render(self):
        out = '<span>'
        for option in self.options:
            if isinstance(option, tuple) or isinstance(option, list):
                value, desc = option
            else:
                value, desc = option, option

            attrs = self.attrs.copy()
            attrs['name'] = self.name
            attrs['type'] = self.get_type()
            attrs['value'] = value

            if self.value == value:
                attrs['checked'] = 'checked'

            out += '<input %s/> %s' % (attrs, desc)
            
        out += '</span>'
        return out
        
class Checkbox(Field):
    
    def __init__(self, name, **attrs):
        self.checked = attrs.pop("checked", False)
        super(Checkbox, self).__init__(name, **attrs)

    def default_id(self):
        value = self.value or ''
        return self.name + "_" + value.replace(" ", "_")

    def get_type(self):
        return "checkbox"
    
    def set_value(self, value):
        self.checked = bool(value)

    def get_value(self):
        return self.checked

    def render(self):
        attrs = self.attrs.copy()
        attrs['type'] = self.get_type()
        attrs['name'] = self.name
        attrs['value'] = self.value

        if self.checked:
            attrs['checked'] = 'checked'            
        return '<input %s/>' % attrs

class Button(Field):
    
    def __init__(self, name, **attrs):
        super(Button, self).__init__(name, **attrs)

    def show_label(self):
        return False

    def render(self):
        attrs = self.attrs.copy()
        
        if self.value is not None:
            attrs['value'] = self.value

        return "<input %s />" % attrs

################################################################################
# Validator
################################################################################

class Validator(object):
    
    def __init__(self, message, booltest):
        self.message = message
        self.booltest = booltest

    def valid(self, form):
        try:
            return self.booltest(form)
        except:
            return False
