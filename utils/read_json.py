# -*- coding: utf-8 -*-

import json

FILENAME = "instructors.json"
f = open(FILENAME)
instructors = json.loads(f.read())

for i in instructors:
	print i["instructor_first_name"]