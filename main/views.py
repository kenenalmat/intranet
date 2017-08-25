# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from utils import http, go_intranet, codes

import json, time

@csrf_exempt
@http.required_parameters(["student_id"])
@require_http_methods("POST")
def get_schedule(request):
	"""
	"""
	start = time.time()

	student_id = request.POST["student_id"]
	schedule = go_intranet.get_schedule(student_id)

	end = time.time()
	print (end - start)
	print type(schedule)

	res = {
		"result": [x for x in schedule]
	}

	return JsonResponse(res, safe=False)