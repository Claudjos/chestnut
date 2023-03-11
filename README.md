# About

This package provides a framework to develop portable APIs. Supported platforms: Azure Functions, AWS Lambda, GPC, Flask.

## Install
```
pip install chestnut
```

## How to use
Write functions to handle your API operations using the package _chestnut.http_ request/response classes. The decorator _@middleware_ will convert requests/responses from/to the current platform, which is defined in the environment variable _CHESTNUT_MIDDLEWARE_. It supports both functions and coroutines.
```
from chestnut.http import Request, Response
from chestnut import middleware


@middleware
def handler(req: Request) -> Response:
	message = "Hello {} !".format(
		req.query_params.get("name", "anonymous")
	)
	return Response(status=200, body=message)

```

## Unit test
```
pip install -r requirements.txt -r test-requirements.txt
python -m pytest tests/ --cov=chestnut
```