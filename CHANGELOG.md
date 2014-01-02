CHANGELOG
=========

Version 2.0 (Beta)
------------------
- There are so many changes to the existing framework, including loss of 
  backwards compatibility. This caused the change of the major version number.
- **Finally** made the debug funtion work.
- Added special methods for comparison the Form class.
- Removed ObjectWeb.response because it seemed to be unneccesarily tedious and 
  I favored using strings to identify return statuses.
- webapi.header() will now automatically add the ";charset=utf-8" to Content-Type.
- webapi.status() now only uses strings as ObjectWeb.response is deprecated and
  removed.
- Added webapi.redirect() convenience function for permanent redirects.
- Added webapi.seeother() convenience function for temporary redirects.
- Fixed cookie getting bug.
- Removed old webapi.request_var() support.
- Renamed webapi.getvar() to webapi.get().
- Renamed webapi.getvars() to webapi.getall().
- Removed unused webapi.autoassign()
- "exper" has been removed and depricated.
- Examples updated to reflect changes.

Version 1.5.2r3 (Beta)
----------------------
- Forms API has been somewhat tested and moved to Beta. (ObjectWeb.forms)
- Examples updated to reflect changes.

Version 1.5.2r2 (Beta)
----------------------
- Addition of *untested* working Form API.
- Changed Standard heading for files.
- Updated Versioning Information.
- getallvars is **gone**.

Version 1.5.2 (Beta)
--------------------
- Addition of experimental projects folder (ObjectWeb.exper)
- Addition of builtin form processing.


Version 1.5 (Beta)
------------------

- Added Changelog
- Updated Readme
- Changed ObjectWeb.webapi.request_var to ObjectWeb.webapi.getvar, however, kept 
  backwords compatability.
- Added ObjectWeb.webapi.getvars.
- Better commenting/documentation.


Versions 1.1 (Beta) - 1.4 (Beta)
--------------------------------
VERSIONS 1.1 through 1.4 were never officially released and not changes 
documented due to rapid production.
