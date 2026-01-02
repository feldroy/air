# Exceptions

## BaseAirException

Bases: `Exception`

Base AIR Exception

## BrowserOpenError

Bases: `RuntimeError`

Opening the browser failed.

## HTTPException

Bases: `HTTPException`

Convenience import from FastAPI

## ObjectDoesNotExist

Bases: `HTTPException`

Thrown when a record in a persistence store can't be found.

## RenderException

Bases: `BaseAirException`

Error thrown when a render function fails.
