#!/usr/bin/python
################################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## summary: This document serves as a setup/install file for the ObjectWeb 
##           Framework.
## maintainer: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
################################################################################
from distutils.core import setup

setup(
    name='ObjectWeb',
    version="2.1 (Beta)",
    author='Abram C. Isola',
    author_email='abram@isola.mn',
    packages=['ObjectWeb'],
    url='https://github.com/aisola/ObjectWeb',
    description='A pure-Python standalone Web Framework for WSGI and CGI.',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved',
        'Programming Language :: Python',
        'Topic :: Software Development :: Web Development',
    ]
)