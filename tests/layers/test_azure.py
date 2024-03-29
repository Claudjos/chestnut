from .handlers import handle_get, handle_post, handle_get_stream
from chestnut import layer
import azure.functions as func


main = layer(handle_get, "azure")
main2 = layer(handle_get_stream, "azure")
main3 = layer(handle_post, "azure")


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
