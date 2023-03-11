import os, inspect


_SUPPORTED = ["AZURE", "AWS", "GCP"]


def middleware(f):
	# Establish environment
	global _SUPPORTED
	env = os.environ.get("CHESTNUT_MIDDLEWARE", None)
	if env is None:
		raise Exception("CHESTNUT_MIDDLEWARE is not set.")
	env = env.upper()
	if env.upper() not in _SUPPORTED:
		raise Exception("Allowed values for CHESTNUT_MIDDLEWARE are: {}.".format(",".join(_SUPPORTED)))
	# Choose middleware
	if inspect.iscoroutinefunction(f):
		# async
		from chestnut.asynclayers.framework import framework_layer
		if env == "AZURE":
			import azure.functions as func
			from chestnut.layers.azure import azure_to_request, response_to_azure
			async def wrapper(req: func.HttpRequest) -> func.HttpResponse:
				return await framework_layer(azure_to_request, response_to_azure, f, req)
	else:
		# functions
		from chestnut.layers.framework import framework_layer
		if env == "AZURE":
			import azure.functions as func
			from chestnut.layers.azure import azure_to_request, response_to_azure
			def wrapper(req: func.HttpRequest) -> func.HttpResponse:
				return framework_layer(azure_to_request, response_to_azure, f, req)
		if env == "AWS":
			from chestnut.layers.aws import aws_to_request, response_to_aws
			def wrapper(req: dict) -> dict:
				return framework_layer(aws_to_request, response_to_aws, f, req)
		if env == "GCP":
			import flask
			from chestnut.layers.gcp import gcp_to_request, response_to_gcp
			def wrapper(req: flask.Request) -> flask.Response:
				return framework_layer(gcp_to_request, response_to_gcp, f, req)
	# Set
	wrapper.__name__ = f.__name__
	wrapper.__doc__ = f.__doc__
	return wrapper
