from .handlers import handle_get, handle_post, handle_get_stream
from chestnut import layer
from json import loads


get_handler = layer(handle_get, "aws")
stream_handler = layer(handle_get_stream, "aws")
post_handler = layer(handle_post, "aws")


def test_get():
	event = {
		'httpMethod': 'GET',
		'resource': '/somewhere/abc',
		'body': None,
		'multiValueHeaders': {},
		'multiValueQueryStringParameters': {'name': ['johnny']},
		'pathParameters': {'id': 'abc'},
	}
	res = get_handler(event, None)
	assert res["statusCode"] == 200
	assert res["headers"]["x-test"] == "test"
	json = loads(res["body"])
	assert json["id"] == "abc"
	assert json["name"] == "johnny"


def test_stream():
	event = {
		'httpMethod': 'GET',
		'resource': '/stream',
		'body': None,
		'multiValueHeaders': {},
		'multiValueQueryStringParameters': {},
		'pathParameters': {},
	}
	res = stream_handler(event, None)
	assert res["statusCode"] == 200
	assert res["body"] == '0\n1\n2\n3\n4\n'


def test_post():
	event = {
		'httpMethod': 'POST',
		'resource': '/somewhere',
		'body': '{"foo": "bar"}',
		'multiValueHeaders': {},
		'multiValueQueryStringParameters': {},
		'pathParameters': {},
	}
	res = post_handler(event, None)
	assert res["statusCode"] == 200
	assert res["body"] == '{"foo":"bar"}'
