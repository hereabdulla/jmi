# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import getdate, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
import pandas as pd
# from __future__ import unicode_literals
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide
import pandas as pd
import datetime as dt
from typing import Dict, List  
Filters = frappe._dict


def execute(filters=None):
	columns, data = [] ,[]
	columns = get_columns(filters)
	data = get_data(filters)
	chart_columns = get_columns_for_rep(filters)
	chart = get_chart_data(filters)
	return columns, data, chart_columns,chart

def get_columns(filters):
	column = [
		_('Branch') + ':Data:200',
		_('Planned Count') + ':Data:200',
	]
	shift=frappe.get_all("Shift Type",order_by='name ASC')
	for s in shift:
		column.append(_(s.name) + ":Data/:70")
	
	return column

def get_data(filters):
	data = []
	ep = frappe.db.exists("CL Plant Count",{"date":filters.date})
	if ep:
		emp_count=frappe.get_doc("CL Plant Count",ep)
		frappe.errprint(emp_count)
		if emp_count.contractor_employee_plan:
			frappe.errprint("Hi")
			for e in emp_count.contractor_employee_plan:
				row2 =  [e.plant,e.planned_count]
				shift =frappe.db.get_all("Shift Type",order_by='name ASC')
				for s in shift:
	
					frappe.errprint(e.plant)
					attendance = frappe.db.sql("""select count(status) as cnt, shift from `tabAttendance` where attendance_date = '%s' and status = 'Present' and branch = '%s' and shift = '%s'"""%(filters.date,e.plant,s.name),as_dict=1)[0]
					if attendance['cnt']:
						row2.append(attendance['cnt'])
					else:
						row2.append(0)
				data.append(row2)

	
	return data

def get_columns_for_rep(filters) -> List[Dict]:
	shiftt = []
	shift = frappe.get_all('Shift Type', ['name'])

	for s in shift:
		label = frappe.scrub(s.name)  
		shiftt.append({"label": label, "fieldtype": "Data", "fieldname": label, "width": 65})

	return shiftt
	
def get_chart_data(filters) -> Dict:
	labels = []
	first_shift1=[]
	sec_shift1=[]
	third_shift1=[]
	fourth_shift1=[]
	fifth_shift1=[]
	fifth_p1_shift1=[]
	sixth_s_shift1=[]
	sixth_v_shift1=[]
	gen1=[]

	ep = frappe.db.exists("CL Plant Count",{"date":filters.date})
	if ep:
		emp_count=frappe.get_doc("CL Plant Count",ep)
		frappe.errprint(emp_count)
		if emp_count.contractor_employee_plan:
			frappe.errprint("Hi")
			first_shift=0
			sec_shift=0
			third_shift=0
			fourth_shift=0
			fifth_shift=0
			fifth_p1_shift=0
			sixth_s_shift=0
			sixth_v_shift=0
			gen=0
			for e in emp_count.contractor_employee_plan:
				labels.append(e.plant)
				shift =frappe.db.get_all("Shift Type",order_by='name ASC')
				for s in shift:
					attendance = frappe.db.sql("""select count(status) as cnt, shift from `tabAttendance` where attendance_date = '%s' and status = 'Present' and branch = '%s' and shift = '%s'"""%(filters.date,e.plant,s.name),as_dict=1)[0]
					if s.name=="1":
						first_shift1.append(attendance['cnt'])
					if s.name=="2":
						sec_shift1.append(attendance['cnt'])
					if s.name=="3":
						third_shift1.append(attendance['cnt'])
					if s.name=="4":
						fourth_shift1.append(attendance['cnt'])
					if s.name=="G":
						gen1.append(attendance['cnt'])
					if s.name=="5":
						fifth_shift1.append(attendance['cnt'])
					if s.name=="5 - P1":
						fifth_p1_shift1
					if s.name=="6 - S":
						sixth_s_shift1
					if s.name=="6 - V":
						sixth_v_shift1
					
	
			# first_shift1.append(first_shift)
			# sec_shift1.append(sec_shift)
			# third_shift1.append(third_shift)
			# fourth_shift1.append(fourth_shift)
			# fifth_shift1.append(fifth_shift)
			# fifth_p1_shift1.append(fifth_p1_shift)
			# sixth_s_shift1.append(sixth_s_shift)
			# sixth_v_shift1.append(sixth_v_shift)
			# gen1.append(gen)

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "1", "values": first_shift1},
				{"name": "2", "values": sec_shift1},
				{"name": "3", "values": third_shift1},
				{"name": "4", "values": fourth_shift1},
				{"name": "5", "values": fifth_shift1},
				{"name": "5 - P1", "values": fifth_p1_shift1},
				{"name": "6 - S", "values": sixth_s_shift1},
				{"name": "6 - V", "values": sixth_v_shift1},
				{"name": "G", "values": gen1},

			],
		},
		"type": "bar",
		"colors":  ["red", "green", "blue", "orange", "purple", "pink", "yellow", "violet"],
	}