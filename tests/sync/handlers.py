from chestnut.http import Request, Response


def handle_get(request: Request) -> Response:
	return Response(
		status=200,
		body={
			"id": request.route_params["id"],
			"name": request.query_params["name"]
		},
		headers={"x-test": "test"}
	)


def handle_post(request: Request) -> Response:
	return Response(
		status=200,
		body=request.json
	)


def handle_get_stream(request: Request) -> Response:
	def stream():
		for i in range(0, 5):
			yield "{}\n".format(i)
		return
	return Response(
		status=200,
		body=stream()
	)
