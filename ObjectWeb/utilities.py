#!/usr/bin/python
################################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## @summary: This document creates several helper functions and framework
##           utilities.
## maintainer: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
################################################################################

import threading

class cached_property(object):
    """A decorator that converts a function into a lazy property.

    The function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::

        class Foo(object):

            @cached_property
            def foo(self):
                # calculate something important here
                return 42

    The class has to have a `__dict__` in order for this property to
    work.

    .. note:: Implementation detail: this property is implemented as non-data
       descriptor.  non-data descriptors are only invoked if there is
       no entry with the same name in the instance's __dict__.
       this allows us to completely get rid of the access function call
       overhead.  If one choses to invoke __get__ by hand the property
       will still work as expected because the lookup logic is replicated
       in __get__ for manual invocation.

    This class was ported from `Werkzeug`_ and `Flask`_.
    """

    _default_value = object()

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func
        self.lock = threading.RLock()

    def __get__(self, obj, type=None):
        if obj is None:
            return self

        with self.lock:
            value = obj.__dict__.get(self.__name__, self._default_value)
            if value is self._default_value:
                value = self.func(obj)
                obj.__dict__[self.__name__] = value

            return value