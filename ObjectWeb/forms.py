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
import copy

################################################################################
# Import ObjectWeb
################################################################################
import ObjectWeb.webapi as webapi

################################################################################
# Form Class
################################################################################

class Form(object):
    """
        This should serve as the main interface between the server and client 
        when dealing with HTML Forms and Form Processing.
    """
    
    def __init__(self, *fields, **kwargs):
        """
            *THIS METHOD SHOULD NOT BE CALLED MANUALLY.*
            
            Initializes the Application Object.
            
            @param *fields: Turns to be a list of Field Objects that define the
            fields.

            @param **kwargs: The validators + (key, value) pairs of attributes.

            @return: Form Object.
        """
        self.fields = fields
        self.validators = kwargs.pop("validators", [])
        self.formid = kwargs.pop("formid", None)
        self.error = None
        self.valid = True

    def __call__(self):
        """
            *THIS METHOD SHOULD NOT BE CALLED MANUALLY.*

            Creates an exact copy of the curren Form object. This makes form
            processessing easier.

            @return: Form Object.
        """
        return copy.deepcopy(self)

    def __getattr__(self, name):
        """
            *THIS METHOD SHOULD NOT BE CALLED MANUALLY.*

            Lets fields to be called as attributes.

            @return: Form Object.
        """
        # don't interfere with deepcopy
        fields = self.__dict__.get('fields') or []
        for field in fields:
            if field.name == name:
                return field
        raise AttributeError, name
    
    def render(self):
        """
            Creates the actual HTML markup for the form.

            @return: Form HTML.
        """
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
        """
            Ensures that the form has been given valid input.

            @return: BOOL(True|False)
        """
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
    """
        *THIS CLASS SHOULD NOT BE INSTANTIATED MANUALLY.*

        This is a base class for the Field Objects. This normally should not
        be called manually as it can error out without information from 
        subclasses.
    """
    
    def __init__(self, name, **attrs):
        """
            *THIS METHOD SHOULD NOT BE CALLED MANUALLY.*
            
            This instantiates the object.
            
            @return: Field Object.
        """
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
        """
            Defines the default id.

            @return: None.
        """
        return self.name

    def field_type(self):
        """
            Defines the type of field. This must be defined in subclasses.
        """
        raise NotImplementedError

    def show_label(self):
        """
            Defines if the HTML label should be displayed.

            @return: BOOL(True|False)
        """
        return True

    def set_value(self, value):
        """
            Sets the value of the Field.

            @return: None.
        """
        self.value = value

    def get_value(self):
        """
            Gets the value of the Field.

            @return: The value of the field.
        """
        return self.value

    def render(self):
        """
            Creates the actual HTML markup for the Field.

            @return: Field HTML.
        """
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
    """The Field subclass that defines a standard HTML Textbox input."""
    def get_type(self):
        """Defines the type of field."""
        return 'text'

class Password(Field):
    """The Field subclass that defines a standard HTML Password input."""
    def get_type(self):
        """Defines the type of field."""
        return 'password'

class File(Field):
    """The Field subclass that defines a standard HTML File input."""
    def get_type(self):
        """Defines the type of field."""
        return 'file'

class Hidden(Field):
    """The Field subclass that defines a standard HTML Hidden input."""
    def show_label(self):
        """Hides the HTML Field Label."""
        return False
        
    def get_type(self):
        """Defines the type of field."""
        return 'hidden'

################################################################################
# Slightly-Less-Simple Field Subclasses
################################################################################
class Textarea(Field):
    """The Field subclass that defines a standard HTML Textarea."""
    
    def render(self):
        """Creates the actual HTML markup for the Field."""
        attrs = self.attrs.copy()
        attrs['name'] = self.name
        return '<textarea %s>%s</textarea>' % (attrs, self.value or '')

class Dropdown(Field):
    """The Field subclass that defines a standard HTML Dropdown."""
    
    def __init__(self, name, options, **attrs):
        self.options = options
        super(Dropdown, self).__init__(name, **attrs)
        
    def render(self):
        """Creates the actual HTML markup for the Field."""
        attrs = self.attrs.copy()
        attrs["name"] = self.name
        
        out = '<select %s>' % attrs

        for option in self.options:
            out += self.render_option(option)

        out += '</select>'
        return out

    def render_option(self, option):
        """Creates the actual HTML markup for the Field Options."""
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
    """The Field subclass that defines a standard HTML Dropdown with Groups."""
    
    def __init__(self, name, options, **attrs):
        self.options = options
        super(GroupedDropdown, self).__init__(self, name, **attrs)

    def render(self):
        """Creates the actual HTML markup for the Field."""
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
    """The Field subclass that defines a standard HTML Radio Switch."""
    
    def __init__(self, name, options, **attrs):
        super(Radio, self).__init__(name, **attrs)

    def get_type(self):
        """Defines the type of field."""
        return 'radio'

    def render(self):
        """Creates the actual HTML markup for the Field."""
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
    """The Field subclass that defines a standard HTML Checkbox."""
    
    def __init__(self, name, **attrs):
        self.checked = attrs.pop("checked", False)
        super(Checkbox, self).__init__(name, **attrs)

    def default_id(self):
        """Defines the default id."""
        value = self.value or ''
        return self.name + "_" + value.replace(" ", "_")

    def get_type(self):
        """Defines the type of field."""
        return "checkbox"
    
    def set_value(self, value):
        """Sets the Field value."""
        self.checked = bool(value)

    def get_value(self):
        """Returns the Field value."""
        return self.checked

    def render(self):
        """Creates the actual HTML markup for the Field."""
        attrs = self.attrs.copy()
        attrs['type'] = self.get_type()
        attrs['name'] = self.name
        attrs['value'] = self.value

        if self.checked:
            attrs['checked'] = 'checked'            
        return '<input %s/>' % attrs

class Button(Field):
    """The Field subclass that defines a standard HTML Button."""
    
    def __init__(self, name, **attrs):
        super(Button, self).__init__(name, **attrs)

    def show_label(self):
        """Hides the HTML Label"""
        return False

    def get_type(self):
        """Defnes field type."""
        return "button"

    def render(self):
        """Creates the actual HTML markup for the Field."""
        attrs = self.attrs.copy()
        attrs["type"] = self.get_type()
        
        if self.value is not None:
            attrs['value'] = self.label or self.name

        return "<input %s />" % attrs

class Submit(Button):
    """The Field subclass that defines a standard HTML Submit Button."""
    
    def __init__(self, name, **attrs):
        super(Submit, self).__init__(name, **attrs)

    def get_type(self):
        """Defines the Field type."""
        return "submit"

################################################################################
# Validator
################################################################################

class Validator(object):
    """
        This class defines the validation rules for the form.
    """
    
    def __deepcopy__(self, memo):
        """
            Deepcopy needs this.
        """
        return copy.copy(self)
    
    def __init__(self, message, booltest):
        """
            Instantiates the object. This sets the messages of failure and the 
            test.
        """
        self.message = message
        self.booltest = booltest

    def valid(self, form):
        """
            This runs the test and determines if the rule is true or false.

            @param form: *Form* This is a form object that is automatically 
            passed into the function by Form.validates.
        """
        try:
            # Runs the Test
            return self.booltest(form)
        except:
            # Failed
            return False
