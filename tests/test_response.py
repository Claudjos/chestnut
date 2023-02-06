from chestnut import http


def test_content_type_json():
	r = http.Response(body=[])
	assert r.headers.get("content-type", "") == "application/json"


def test_content_type():
	r = http.Response(body="ciao")
	assert r.headers.get("content-type", "") == ""
