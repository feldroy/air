# Exceptions

## BaseAirException

Bases: `Exception`

Base AIR Exception

## HTTPException

Bases: `HTTPException`

Convenience import from FastAPI

## ObjectDoesNotExist

Bases: `HTTPException`

Thrown when a record in a persistence store can't be found.

## RenderException

Bases: `BaseAirException`

Error thrown when render function fails.
