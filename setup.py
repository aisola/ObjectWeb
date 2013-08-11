#!/usr/bin/python
################################################################################
## @author: Abram C. Isola (Head Author)
## @organization: Abram C. Isola Development
## @contact: abram@isola.mn || http://abram.isola.mn/projects/ObjectWeb
## @license: LGPLv3 (See LICENSE)
## @summary: This document serves as a setup/install file for the ObjectWeb 
##           Framework.
################################################################################
from distutils.core import setup

setup(
    name='ObjectWeb',
    version="1.5.2 (Beta)",
    author='Abram C. Isola',
    author_email='abram@isola.mn',
    packages=['ObjectWeb',"ObjectWeb.exper"],
    url='http://abram.isola.mn/projects/ObjectWeb',
    description='A pure-Python standalone Web Framework for WSGI and CGI.',
)