from .handlers import handle_get, handle_post, handle_get_stream
from chestnut.layers.aws import aws_layer
from json import loads


def get_handler(event, context):
	return aws_layer(handle_get, event)


def stream_handler(event, context):
	return aws_layer(handle_get_stream, event)


def post_handler(event, context):
	return aws_layer(handle_post, event)


"""
TESTS
"""


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
