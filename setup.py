#!/usr/bin/python
################################################################################
## contact: abram@isola.mn || https://github.com/aisola/ObjectWeb
## license: LGPLv3
## summary: This document serves as a setup/install file for the ObjectWeb 
##           Framework.
## maintaier: Abram C. Isola <abram@isola.mn>
## contrib: Abram C. Isola <abram@isola.mn> (all)
################################################################################
from distutils.core import setup

setup(
    name='ObjectWeb',
    version="1.5.2r2 (Beta)",
    author='Abram C. Isola',
    author_email='abram@isola.mn',
    packages=['ObjectWeb',"ObjectWeb.exper"],
    url='http://abram.isola.mn/projects/ObjectWeb',
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