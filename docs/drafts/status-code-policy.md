GET success                         200
POST create resource               201
PATCH update/archive/restore       200
DELETE with response body          200
Invalid request/business rule      400
Authentication failure             401
Valid login, insufficient access   403
Owned resource not found           404
Pydantic/request validation        422
Duplicate unique resource          409