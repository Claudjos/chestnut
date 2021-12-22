from tests.handlers import handle_get, handle_post, handle_get_stream
from chestnut.layers.azure import azure_layer
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
	return azure_layer(handle_get, req)


def main2(req: func.HttpRequest) -> func.HttpResponse:
	return azure_layer(handle_get_stream, req)


def main3(req: func.HttpRequest) -> func.HttpResponse:
	return azure_layer(handle_post, req)


"""
TESTS
"""


def test_get():
	req = func.HttpRequest(
		"GET",
		"/somewhere/1?name=johnny",
		headers={"content-type": "application/json"},
		route_params={"id": "1"},
		params={"name": "johnny"},
		body=b''
	)
	res = main(req)
	assert res.status_code == 200
	assert res.get_body() == b'{"id":"1","name":"johnny"}'
	assert res.headers["x-test"] == "test"


def test_stream():
	req = func.HttpRequest(
		"GET",
		"/stream",
		body=b''
	)
	res = main2(req)
	assert res.status_code == 200
	assert res.get_body() == b'0\n1\n2\n3\n4\n'


def test_post():
	req = func.HttpRequest(
		"POST",
		"/somewhere",
		headers={"content-type":"application/json"},
		body=b'{"foo":"bar"}'
	)
	res = main3(req)
	assert res.status_code == 200
	assert res.get_body() == b'{"foo":"bar"}'
