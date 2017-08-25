# -*- coding: utf-8 -*-

from unidecode import unidecode
from w3lib.html import replace_entities
import lxml.html as lh
import mechanize, codecs, chardet, urllib

import sys, html, json
reload(sys)
sys.setdefaultencoding('utf8')


IUP_URL = "http://intranet2.kbtu.kz/OR3/KBTU.OR.Registration/Students/PrintIUP.aspx"
GET_SUBJ_URL = "http://intranet2.kbtu.kz/or2/or.attestation/admin/ChoiceSection.aspx?InstructorID={}"
SEARCH_TEACHER_URL = "http://intranet2.kbtu.kz/or2/or.attestation/admin/SearchTeacher.aspx"
INSTRUCTORS_FILE = "instructors.json"

SUBJECT_URL = "http://intranet2.kbtu.kz/or2/or.attestation/admin/"

INSTRUCTORS_SELECTOR = "//tr[@bgcolor='White']"
IUP_TABLE_SELECTOR = "//table[@id='data_tbl']"
IUP_ROW_SELECTOR = ""
WEEK_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]



def get_day_num(day):
	for i in range(6):
		if WEEK_DAYS[i] == day:
			return i

def select_form(form):
	"""
	"""
	return form.attrs.get('action', None) == "login.aspx?path=http://intranet2.kbtu.kz/OR3/KBTU.OR.Registration/Students/PrintIUP.aspx"


def authorize(br):
	"""
	"""
	br.set_handle_equiv(False)
	br.set_handle_robots(False)
	br.open(IUP_URL)
	br.select_form(predicate=select_form)
	br.form["uname"] = "a_kenen"
	br.form["pwd"] = "Kbtu1111"
	br.submit()

	br.select_form("__aspnetForm")
	br.form["_ctl0:_ctl0:txtUserName"] = "15BD02046"
	br.form["_ctl0:_ctl0:txtPassword"] = "Kbtu1111"
	br.submit()
	return br


def update_instructors():
	"""
	"""
	br = mechanize.Browser()
	br = authorize(br)
	br.open(SEARCH_TEACHER_URL)
	br.select_form("__aspnetForm")
	br.submit()

	with open("instructors.html", "wb") as f:
		f.write(br.response().read())

	tree = lh.fromstring(br.response().read())

	table = tree.xpath(INSTRUCTORS_SELECTOR)
	
	# array = []
	# array.append(table[1304])
	# array.append(table[1285])
	# table = array

	instructors = []
	
	for instructor in table:
		params = instructor.findall("td")
		
		instructor_id = (params[1].text_content())
		instructor_second_name = (params[2].text_content())
		instructor_first_name = params[3].text_content()
		instructor_third_name = params[4].text_content()


		instructor = {
			"instructor_id": instructor_id,
			"instructor_first_name": instructor_first_name,
			"instructor_second_name": instructor_second_name,
			"instructor_third_name": instructor_third_name
		}
		instructors.append(instructor)

	with open(INSTRUCTORS_FILE, "wb") as f:
		f.write(json.dumps(instructors, indent=4).encode('utf8'))

	#print u"\u00d0\u0090\u00d1\u0081\u00d0\u00ba\u00d0\u00b0\u00d1\u0080".encode('unicode_escape').decode('string-escape')


def get_students(br, link):
	"""
	"""

	br.follow_link(link)
	tree = lh.fromstring(br.response().read())

	rows = tree.xpath("//tr")[1:]
	
	if len(rows) <= 1:
		return []
	res = []
	for row in rows:
		params = row.findall('td')
		id = params[1].text_content().strip()
		res.append(id)
	
	return res


def check_subject(br, subject_url, student_id):
	"""
	"""
	for f in br.links():
		
		url = f.url
		url = urllib.unquote(url).decode('utf-8').encode('unicode_escape').decode('string-escape')
		
		students = []
		if subject_url == url:
			new_br = br	
			students = get_students(new_br, f)
			
			for student in students:
				if student == student_id:
					return True
	return False


def get_subjects(instructor_id, instructor_full_name, student_id, schedule):
	"""
	"""

	br = mechanize.Browser()
	br = authorize(br)

	br.open(GET_SUBJ_URL.format(instructor_id))

	tree = lh.fromstring(br.response().read())
	
	rows = tree.xpath("//tr")
	rows = rows[2:]

	for row in rows:
		params = row.findall('td')
		subject_title = params[1].text_content().encode('unicode_escape').decode('string-escape').strip()
		subject_type = params[2].find('a').text_content().encode('unicode_escape').decode('string-escape').strip()
		subject_url = params[2].find('a').attrib["href"].encode('unicode_escape').decode('string-escape').strip()
		subject_time = params[2].text_content().encode('unicode_escape').decode('string-escape').strip()
		
		subject_time = subject_time[-15:]

		subject_day = get_day_num(subject_time[:3])
		subject_hour = int(subject_time[4]) * 10 + int(subject_time[5])

		new_br = mechanize.Browser()
		new_br = authorize(new_br)
		new_br.open(GET_SUBJ_URL.format(instructor_id))

		if check_subject(new_br, subject_url, student_id):
			
			obj = {
				"discipline_name": subject_title,
				"instructor_full_name": instructor_full_name,
				"type": subject_type,
				"subject_time": subject_time,
				"day_num": subject_day,
				"subject_hour": subject_hour
			}

			index = subject_day * 14 + subject_hour - 8

			schedule[index] = obj


def get_schedule(student_id):
	"""
	"""
	schedule = [{
		"discipline_name": "NULL",
		"room": 0,
		"instructor_full_name": "NULL",
		"type": -1
	}] * 6 * 14

	update_instructors()
	br = mechanize.Browser()
	br = authorize(br)

	br.open(IUP_URL + "?StudentID={}".format(student_id))	


	tree = lh.fromstring(br.response().read())
	table = tree.xpath(IUP_TABLE_SELECTOR)

	for t in table:
		my_instructors = t.getchildren()[1].findall("tr")
		my_instructors = my_instructors[:len(my_instructors)-1]

		for mi in my_instructors:
			brs = mi[6].getchildren()
			for tag in brs:
				tag.tail = u"*" + tag.tail if tag.tail else "*"

			names = mi[6].text_content().strip().split("*")
			names = names[:len(names) - 1]

			for name in names:

				name = name.strip()

				name = name.replace(" ", "")

				f = open(INSTRUCTORS_FILE, "r")			
				instructors = json.loads(f.read())
				for ins in instructors:
					instructor_id = ins["instructor_id"].encode('unicode_escape').decode('string-escape')
					instructor_first_name = ins["instructor_first_name"].encode('unicode_escape').decode('string-escape')
					instructor_second_name = ins["instructor_second_name"].encode('unicode_escape').decode('string-escape')
					instructor_third_name = ins["instructor_third_name"].encode('unicode_escape').decode('string-escape')
					instructor_full_name = instructor_second_name + " " + instructor_first_name + " " + instructor_third_name
					
					first_instructor_full_name = instructor_full_name
					instructor_full_name = instructor_full_name.replace(" ", "")
					
					
					if instructor_full_name == name:
						print instructor_full_name + " and " + name
						get_subjects(instructor_id, first_instructor_full_name, student_id, schedule)
	return schedule

update_instructors()