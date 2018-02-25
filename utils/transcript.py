from unidecode import unidecode
from w3lib.html import replace_entities
import lxml.html as lh
import mechanize, codecs, chardet, urllib

import go_intranet

import sys, json
reload(sys)
sys.setdefaultencoding('utf8')

IUP_URL = "http://intranet2.kbtu.kz/OR3/KBTU.OR.Registration/Students/PrintIUP.aspx"
GET_SUBJ_URL = "http://intranet2.kbtu.kz/or2/or.attestation/admin/ChoiceSection.aspx?InstructorID={}"
SEARCH_TEACHER_URL = "http://intranet2.kbtu.kz/or2/or.attestation/admin/SearchTeacher.aspx"
INSTRUCTORS_FILE = "instructors.json"

SUBJECT_URL = "http://intranet2.kbtu.kz/or2/or.attestation/admin/"

OUT_FILE = "out.csv"

INSTRUCTORS_SELECTOR = "//tr[@bgcolor='White']"
IUP_TABLE_SELECTOR = "//table[@id='data_tbl']"
IUP_ROW_SELECTOR = ""



TRANSCIPT_URL = "http://intranet2.kbtu.kz/OR3/KBTU.OR.Transcript/Students/Transcript.aspx?studentid={}"
SEARCH_STUDENT_URL = "http://intranet2.kbtu.kz/or2/or.attestation/admin/SearchStudent.aspx"

DISCIPLINE_SELECTOR = "//tr[@valign='top']"
STUDENT_INFO_SELECTOR = "//table[@id='ctl00_MainBody_Transcript1_dtlStudent']//td[@valign='top']"
STUDENTS_SELECTOR = "//tr[@bgcolor='White']"
STUDENTS_HTML_FILE = "students"


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

def check(id):
	if id >= "A" and id <= "Z":
		return False

	if id > "10":
		return True
	return False


def get_transcipt(student_id):
	br = mechanize.Browser()
	br = authorize(br)
	br.open(TRANSCIPT_URL.format(student_id))

	with open("out", "wb") as f:
		f.write(br.response().read())

	tree = lh.fromstring(br.response().read())

	student_info = tree.xpath(STUDENT_INFO_SELECTOR)
	title = ""
	a = []
	for line in student_info:
		data = line.text_content().splitlines()
		a.append(" ".join(x.strip() for x in data))

	title = ";".join(x for x in a)

	subjects = tree.xpath(DISCIPLINE_SELECTOR)
	for s in subjects:
		data = s.findall("td")
		cur = []

		cur.append(title)
		for d in data:
			cur.append(d.text_content().strip(' '))
		res = ";".join(str(x) for x in cur)
		
		with open(OUT_FILE, "a") as f:
			f.write(res + "\n")


def update_students():
	br = mechanize.Browser()
	br = authorize(br)
	br.open(SEARCH_STUDENT_URL)
	br.select_form("__aspnetForm")
	br.submit()
	with open(STUDENTS_HTML_FILE, "wb") as f:
		f.write(br.response().read())


def get_students():
	s = ""
	with open(STUDENTS_HTML_FILE, "r") as f:
		s = f.read()

	tree = lh.fromstring(s)
	table = tree.xpath(STUDENTS_SELECTOR)
	
	students = []
	for student in table:
		params = student.findall("td")		
		student_id = (params[1].text_content())
		students.append(student_id)

	students.sort()

	with open("ids", "wb") as f:
		for s in students:
			if check(s):
				f.write(s + "\n")


def get_shit_that_Alikhan_wants():
	ids = []
	with open("ids", "r") as f:
		for line in f:
			ids.append(line.strip())
	
	with open(OUT_FILE, 'w'): 
		pass
	
	for id in ids:
		get_transcipt(id)
	

get_students()
get_shit_that_Alikhan_wants()
