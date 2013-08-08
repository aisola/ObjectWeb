#!/usr/bin/python
################################################################################
## @author: Abram C. Isola (Head Author)
## @organization: Abram C. Isola Development
## @contact: abram@isola.mn || http://abram.isola.mn/projects/ObjectWeb
## @license: LGPLv3 (See LICENSE)
## @summary: This document creates the Response Objects that are used to 
##           identify the status.
################################################################################
import webapi

## 1XX Informational ##############################################################
class Continue(object):
    def __str__(self): return "100 Continue"
    def __int__(self): return 100

class SwitchingProtocols(object):
    def __str__(self): return "101 Switching Protocols"
    def __int__(self): return 101

class Processing(object):
    def __str__(self): return "102 Processing"
    def __int__(self): return 102

## 2XX Success ####################################################################
class OK(object):
    def __str__(self): return "200 OK"
    def __int__(self): return 200

class Created(object):
    def __str__(self): return "201 Created"
    def __int__(self): return 201

class Accepted(object):
    def __str__(self): return "202 Accepted"
    def __int__(self): return 202

class NonAuthoritativeInformation(object):
    def __str__(self): return "203 Non-Authoritative Information"
    def __int__(self): return 203
    
class NoContent(object):
    def __str__(self): return "204 No Content"
    def __int__(self): return 204

class ResetContent(object):
    def __str__(self): return "205 Reset Content"
    def __int__(self): return 205

class PartialContent(object):
    def __str__(self): return "206 Partial Content"
    def __int__(self): return 205

class AlreadyReported(object):
    def __str__(self): return "208 Already Reported"
    def __int__(self): return 208

class IMUsed(object):
    def __str__(self): return "226 IM Used"
    def __int__(self): return 226

## 3XX Redirection ################################################################
class MovedPermanently(object):
    def __init__(self,location):
        webapi.header("Location",str(location))
    def __str__(self): return "301 Moved Permanently"
    def __int__(self): return 301

class Found(object):
    def __str__(self): return "302 Found"
    def __int__(self): return 302

class SeeOther(object):
    def __init__(self,location):
        webapi.header("Location",str(location))
    def __str__(self): return "303 See Other"
    def __int__(self): return 303

class NotModified(object):
    def __str__(self): return "304 Not Modified"
    def __int__(self): return 304

class TemporarRedirect(object):
    def __init__(self,location):
        webapi.header("Location",str(location))
    def __str__(self): return "307 Temporary Redirect"
    def __int__(self): return 307

class PermanentRedirect(object):
    def __init__(self,location):
        webapi.header("Location",str(location))
    def __str__(self): return "308 Permanent Redirect"
    def __int__(self): return 308

## 4XX Client Error ###############################################################
class BadRequest(object):
    def __str__(self): return "400 Bad Request"
    def __int__(self): return 400

class Unauthorized(object):
    def __str__(self): return "401 Unauthorized"
    def __int__(self): return 401

class PaymentRequired(object):
    def __str__(self): return "402 Payment Required"
    def __int__(self): return 402
    
class Forbidden(object):
    def __str__(self): return "403 Forbidden"
    def __int__(self): return 403

class NotFound(object):
    def __str__(self): return "404 Not Found"
    def __int__(self): return 404

class MethodNotAllowed(object):
    def __str__(self): return "405 Method Not Allowed"
    def __int__(self): return 405

class NotAcceptable(object):
    def __str__(self): return "406 Not Acceptable"
    def __int__(self): return 406

class RequestTimeout(object):
    def __str__(self): return "408 Request Timeout"
    def __int__(self): return 408

class Conflict(object):
    def __str__(self): return "409 Conflict"
    def __int__(self): return 409

class Gone(object):
    def __str__(self): return "410 Gone"
    def __int__(self): return 410

class LengthRequired(object):
    def __str__(self): return "411 Length Required"
    def __int__(self): return 411

class PreconditionFailed(object):
    def __str__(self): return "412 Precondition Failed"
    def __int__(self): return 412

class RequestEntityTooLarge(object):
    def __str__(self): return "413 Request Entity Too Large"
    def __int__(self): return 413

class RequestURITooLong(object):
    def __str__(self): return "414 Request URI Too Long"
    def __int__(self): return 414

class UnsupportedMediaType(object):
    def __str__(self): return "415 Unsupported Media Type"
    def __int__(self): return 415

class RequestedRangeNotSatisfiable(object):
    def __str__(self): return "416 Requested Range Not Satisfiable"
    def __int__(self): return 416

class ExpectationFailed(object):
    def __str__(self): return "417 ExpectationFailed"
    def __int__(self): return 417

class UnprocessableEntity(object):
    def __str__(self): return "422 Unprocessable Entity"
    def __int__(self): return 422

class Locked(object):
    def __str__(self): return "423 Locked"
    def __int__(self): return 423

class FailedDependency(object):
    def __str__(self): return "424 Failed Dependency"
    def __int__(self): return 424

class MethodFailure(object):
    def __str__(self): return "424 Method Failure"
    def __int__(self): return 424

class UnorderedCollection(object):
    def __str__(self): return "425 Unordered Connection"
    def __int__(self): return 425

class Upgradeequired(object):
    def __str__(self): return "426 Upgrade Required"
    def __int__(self): return 426
    
class PreconditionRequired(object):
    def __str__(self): return "428 Precondition Required"
    def __int__(self): return 428

class TooManyRequests(object):
    def __str__(self): return "429 Too Many Requests"
    def __int__(self): return 429

class RequestHeaderFieldsTooLarge(object):
    def __str__(self): return "431 Request Header Fields Too Large"
    def __int__(self): return 431

## 5XX Server Error ###############################################################
class InternalServerError(object):
    def __str__(self): return "500 Internal Server Error"
    def __int__(self): return 500

class NotImplemented501(object):
    def __str__(self): return "501 Not Implemented"
    def __int__(self): return 501
