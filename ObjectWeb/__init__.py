#!/usr/bin/python
################################################################################
## @author: Abram C. Isola (Head Author)
## @organization: Abram C. Isola Development
## @contact: abram@isola.mn || http://abram.isola.mn/projects/ObjectWeb
## @license: LGPLv3 (See LICENSE)
## @summary: This document initializes the ObjectWeb Framework for use.
## 
## @precondition: Apache2 MUST be configured correctly with mod_wsgi if 
##                Apache will be used as the server.
################################################################################

################################################################################
# Import
################################################################################
from application import *
from webapi import *
from response import *

################################################################################
# Meta Information
################################################################################
__author__ = ["See CONTRIB"]
__version__ = "1.5 (Beta)"
__url__ = "http://gihub.com/aisola/ObjectWeb"
