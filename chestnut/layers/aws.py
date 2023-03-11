from chestnut.http import Request, Response


def response_to_aws(response: Response) -> dict:
	"""
	Converts chestnut.http.Response to a AWS lambda output.
	"""
	return {
		"statusCode": response.status,
		"headers": response.headers,
		"body": response.body.decode()
	}


def aws_to_request(event: dict) -> Request:
	"""
	Converts AWS lambda event into a chestnut.http.Request.
	"""
	return Request(
		method=event.get("httpMethod"),
		path=event.get("resource"),
		headers=event.get("multiValueHeaders"),
		route=event.get("pathParameters"),
		query=event.get("multiValueQueryStringParameters"),
		body=event.get("body")
	)
