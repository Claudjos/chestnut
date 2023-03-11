from .handlers import handle_get, handle_post
from chestnut import layer
from io import BytesIO
import flask


get_handler = layer(handle_get, "gcp")
post_handler = layer(handle_post, "gcp")


def test_get():
	req = flask.Request({
		"wsgi.input": BytesIO(b''),
		"wsgi.url_scheme": "http",
		"REQUEST_METHOD": "GET",
		"PATH_INFO": "/somewhere/1",
		"RAW_URI": "/somewhere/1?name=jhonny",
		"QUERY_STRING": "name=jhonny",
		"SERVER_NAME": "Test",
		"CONTENT_TYPE": "application/json",
		"CONTENT_LENGTH": 0
	})
	req.url_rule = "/somewhere/<id>" # pointless
	req.view_args = {"id": "1"}
	res = get_handler(req)
	assert res.status_code == 200
	assert res.json == {"id": "1", "name": "jhonny"}
	assert res.headers["x-test"] == "test"


def test_post():
	body = b'{"foo":"bar"}'
	req = flask.Request({
		"wsgi.input": BytesIO(body),
		"wsgi.url_scheme": "http",
		"REQUEST_METHOD": "POST",
		"PATH_INFO": "/somewhere",
		"RAW_URI": "/somewhere",
		"QUERY_STRING": "n",
		"SERVER_NAME": "Test",
		"CONTENT_TYPE": "application/json",
		"CONTENT_LENGTH": len(body)
	})
	req.url_rule = "/somewhere" # pointless
	req.view_args = {}
	res = post_handler(req)
	assert res.status_code == 200
	assert res.json == {"foo": "bar"}
