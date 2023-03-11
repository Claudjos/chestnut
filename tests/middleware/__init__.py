from chestnut.http import Request, Response


def ctrl_sync(request: Request) -> Response:
	return Response(
		status=200,
		body={
			"id": request.route_params["id"],
			"name": request.query_params["name"]
		},
		headers={"x-test": "test"}
	)


async def ctrl_async(request: Request) -> Response:
	return ctrl_sync(request)
