from typing import Callable, Awaitable
from chestnut.http import Request


def framework_layer_sync(
	request_converter: Callable,
	response_converter: Callable,
	handler: Callable,
	req: Request
):
	return response_converter(handler(request_converter(req)))


async def framework_layer_async(
	request_converter: Callable,
	response_converter: Callable,
	handler: Awaitable,
	req: Request
):
	return response_converter(await handler(request_converter(req)))
