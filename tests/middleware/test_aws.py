import os, pytest
from . import ctrl_sync, ctrl_async
from chestnut import middleware
from json import loads


os.environ["CHESTNUT_MIDDLEWARE"] = "aws"
main_sync = middleware(ctrl_sync)
main_async = middleware(ctrl_async)


req = {
	'httpMethod': 'GET',
	'resource': '/somewhere/abc',
	'body': None,
	'multiValueHeaders': {},
	'multiValueQueryStringParameters': {'name': ['johnny']},
	'pathParameters': {'id': 'abc'},
}


def test_sync():
	global req
	res = main_sync(req, None)
	assert res["statusCode"] == 200
	assert res["headers"]["x-test"] == "test"
	json = loads(res["body"])
	assert json["id"] == "abc"
	assert json["name"] == "johnny"


@pytest.mark.asyncio
async def test_async():
	global req
	res = await main_async(req, None)
	assert res["statusCode"] == 200
	assert res["headers"]["x-test"] == "test"
	json = loads(res["body"])
	assert json["id"] == "abc"
	assert json["name"] == "johnny"
