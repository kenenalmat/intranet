from functools import wraps
from django.http import HttpResponse
import codes, messages, json


def http_response_with_json_body(body):
    return HttpResponse(body, content_type="application/json")


def http_response_with_json(json_object):
    return http_response_with_json_body(json.dumps(json_object))

def json_response():
	"""
	"""
	def decorator(func):
		@wraps(func)
		def inner(*args, **kwargs):
			response = func(*args, **kwargs)
			if not ('code' in response):
			 	response['code'] = codes.OK
			return http_response_with_json(response)
		return inner
	return decorator

def required_parameters(params):
	"""
	"""
	def decorator(func):
		@wraps(func)
		def inner(request, *args, **kwargs):
			if request.method == "POST":
				for p in params:
					value = request.POST.get(p)
					if value is None:
						print "shit"
						return code_response(codes.MISSING_PARAMETER, message=messages.MISSING_PARAMETER.format(p))
			else:
				for p in params:
					value = request.GET.get(p)
					if value is None:
						return code_response(codes.MISSING_PARAMETER, message=messages.MISSING_PARAMETER.format(p))
			return func(request, *args, **kwargs)
		return inner
	return decorator


def code_response(code, message=None, error=None):
	"""
	"""
	result = {'code': code}
	if message:
		result['message'] = message
	if error:
		result['error'] = error
	return result
