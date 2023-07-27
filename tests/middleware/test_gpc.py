import os, pytest, flask
from . import ctrl_sync, ctrl_async
from chestnut import middleware
from json import loads
from io import BytesIO


os.environ["CHESTNUT_MIDDLEWARE"] = "gcp"
main_sync = middleware(ctrl_sync)
main_async = middleware(ctrl_async)


req = flask.Request({
	"wsgi.input": BytesIO(b''),
	"wsgi.url_scheme": "http",
	"REQUEST_METHOD": "GET",
	"PATH_INFO": "/somewhere/1",
	"RAW_URI": "/somewhere/1?name=jhonny",
	"QUERY_STRING": "name=jhonny",
	"SERVER_NAME": "Test",
	"CONTENT_TYPE": "application/json",
	"CONTENT_LENGTH": "0"
})
req.url_rule = "/somewhere/<id>" # pointless
req.view_args = {"id": "1"}


def test_sync():
	global req
	res = main_sync(req)
	assert res.status_code == 200
	assert res.json == {"id": "1", "name": "jhonny"}
	assert res.headers["x-test"] == "test"


@pytest.mark.asyncio
async def test_async():
	global req
	res = await main_async(req)
	assert res.status_code == 200
	assert res.json == {"id": "1", "name": "jhonny"}
	assert res.headers["x-test"] == "test"
