from chestnut.http import Request, Response


def test_request_json_rewrite():
	r = Request(method="POST", body=b'{"a":1}', uri="/")
	assert r.json == {"a": 1}
	r.json["b"] = 2
	assert r.json == {"a": 1, "b": 2}


def test_request_json():
	r = Request(method="POST", uri="/")
	assert r.json == {}


def test_response():
	r = Response(status=200, status_code=400, body=[1])
	assert r.status == 200
	assert r.body == b'[1]'
	assert r.text == '[1]'
	assert r.json() == [1]
	assert r.mimetype == "application/json"


def test_response_body_bytes():
	r = Response(status_code=200, body=b'{"a":1}')
	assert r.status == 200
	assert r.json() == {"a": 1}


def test_response_body_string():
	r = Response(body='')
	# body of type string is converted to bytes by super __init__
	r.body = '{"a":1}'
	assert r.json() == {"a": 1}


def test_response_override_content():
	r = Response(status_code=200, body={"a":1}, mimetype="custom")
	assert r.mimetype == "custom"
