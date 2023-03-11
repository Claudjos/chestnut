import os, pytest
import azure.functions as func
from . import ctrl_sync, ctrl_async
from chestnut import middleware
from json import loads


os.environ["CHESTNUT_MIDDLEWARE"] = "azure"
main_sync = middleware(ctrl_sync)
main_async = middleware(ctrl_async)


req = func.HttpRequest(
	"GET",
	"/somewhere/1?name=johnny",
	headers={"content-type": "application/json"},
	route_params={"id": "1"},
	params={"name": "johnny"},
	body=b''
)


def test_sync():
	global req
	res = main_sync(req)
	assert res.status_code == 200
	assert loads(res.get_body()) == {"id": "1", "name": "johnny"}
	assert res.headers["x-test"] == "test"


@pytest.mark.asyncio
async def test_async():
	global req
	res = await main_async(req)
	assert res.status_code == 200
	assert loads(res.get_body()) == {"id": "1", "name": "johnny"}
	assert res.headers["x-test"] == "test"
