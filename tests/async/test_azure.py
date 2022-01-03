from .handlers import handle_get
from chestnut.asynclayers.azure import azure_layer
import azure.functions as func
import pytest
from json import loads


async def main(req: func.HttpRequest) -> func.HttpResponse:
	return await azure_layer(handle_get, req)


@pytest.mark.asyncio
async def test_get():
	req = func.HttpRequest(
		"GET",
		"/somewhere/1?name=johnny",
		headers={"content-type": "application/json"},
		route_params={"id": "1"},
		params={"name": "johnny"},
		body=b''
	)
	res = await main(req)
	assert res.status_code == 200
	assert loads(res.get_body()) == {"id": "1", "name": "johnny"}
	assert res.headers["x-test"] == "test"
