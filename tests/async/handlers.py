from chestnut.http import Request, Response


async def handle_get(request: Request) -> Response:
	return Response(
		status=200,
		body={**request.query_params, **request.route_params},
		headers={"x-test": "test"}
	)
