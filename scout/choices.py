from django.utils.translation import ugettext_lazy as _

HTTP_200 = 200
HTTP_201 = 201
HTTP_202 = 202
HTTP_203 = 203
HTTP_204 = 204
HTTP_205 = 205
HTTP_206 = 206
HTTP_301 = 301
HTTP_302 = 302
HTTP_303 = 303
HTTP_304 = 304
HTTP_305 = 305
HTTP_307 = 307
HTTP_400 = 400
HTTP_401 = 401
HTTP_403 = 403
HTTP_404 = 404
HTTP_405 = 405
HTTP_406 = 406
HTTP_407 = 407
HTTP_408 = 408
HTTP_409 = 409
HTTP_410 = 410
HTTP_411 = 411
HTTP_412 = 412
HTTP_413 = 413
HTTP_414 = 414
HTTP_415 = 415
HTTP_416 = 416
HTTP_417 = 417
HTTP_500 = 500
HTTP_501 = 501
HTTP_502 = 502
HTTP_503 = 503
HTTP_504 = 504
HTTP_505 = 505

HTTP_STATUS_CODES = (
    # We support all of them but for the sake of sanity;
    # most used ones are at the top of the list.
    (HTTP_200, _('<200> Success: OK')),
    (HTTP_301, _('<301> Redirection: Moved Permanently')),
    (HTTP_302, _('<302> Redirection: Found')),
    (HTTP_404, _('<404> Client Error: Not Found')),
    (HTTP_500, _('<500> Server Error: Internal Server Error')),
    (None, '-'),
    (HTTP_201, _('<201> Success: Created')),
    (HTTP_202, _('<202> Success: Accepted')),
    (HTTP_203, _('<203> Success: Non-Authoritative Information')),
    (HTTP_204, _('<204> Success: No Content')),
    (HTTP_205, _('<205> Success: Reset Content')),
    (HTTP_206, _('<206> Success: Partial Content')),
    (HTTP_303, _('<303> Redirection: See Other')),
    (HTTP_304, _('<304> Redirection: Not Modified')),
    (HTTP_305, _('<305> Redirection: Use Proxy')),
    (HTTP_307, _('<307> Redirection: Temporary Redirect')),
    (HTTP_400, _('<400> Client Error: Bad Request')),
    (HTTP_401, _('<401> Client Error: Unauthorized')),
    (HTTP_403, _('<403> Client Error: Forbidden')),
    (HTTP_405, _('<405> Client Error: Method Not Allowed')),
    (HTTP_406, _('<406> Client Error: Not Acceptable')),
    (HTTP_407, _('<407> Client Error: Proxy Auth Required')),
    (HTTP_408, _('<408> Client Error: Request Timeout')),
    (HTTP_409, _('<409> Client Error: Conflict')),
    (HTTP_410, _('<410> Client Error: Gone')),
    (HTTP_411, _('<411> Client Error: Length Required')),
    (HTTP_412, _('<412> Client Error: Precondition Failed')),
    (HTTP_413, _('<413> Client Error: Request Entity Too Large')),
    (HTTP_414, _('<414> Client Error: Request-URI Too Long')),
    (HTTP_415, _('<415> Client Error: Unsupported Media Type')),
    (HTTP_416, _('<416> Client Error: Requested Range Not Satisfiable')),
    (HTTP_417, _('<417> Client Error: Expectation Failed')),
    (HTTP_501, _('<501> Server Error: Not Implemented')),
    (HTTP_502, _('<502> Server Error: Bad Gateway')),
    (HTTP_503, _('<503> Server Error: Service Unavailable')),
    (HTTP_504, _('<504> Server Error: Gateway Timeout')),
    (HTTP_505, _('<505> Server Error: HTTP Version Not Supported')),
) 
