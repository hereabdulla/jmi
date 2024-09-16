# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
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

def execute(filters=None):
	columns, data = [] ,[]
	columns = get_columns()
	data = get_data(filters)
	return columns,data

def get_columns():
	column = [
		_('Employee ID') + ':Data:120',
		_('Employee Name') + ':Data:150',
		_('Branch') + ':Data:150',
		_('Contractor') + ':Data:190',
		_('Attendance Date') + ':Data:120',
		_('IN Time') + ':Data:120',
		_('OUT Time') + ':Data:120'

	]
	return column

def get_data(filters):
	data = []
	if filters.contractor and filters.branch:
		attendance = frappe.db.sql("""select * from `tabAttendance` where attendance_date ='%s' and branch = '%s' and contractor = '%s' """%(filters.date,filters.branch,filters.contractor),as_dict=1)
	elif filters.contractor:
		attendance = frappe.get_all("Attendance",{"attendance_date":filters.date,"contractor":filters.contractor},['*'])
	elif filters.branch :
		attendance = frappe.get_all("Attendance",{"attendance_date":filters.date,"branch":filters.branch},['*'])
	
	else:
		attendance = frappe.get_all("Attendance",{"attendance_date":filters.date},['*'])

	for i in attendance:
		frappe.errprint("Hi")
		if frappe.db.exists("Employee",{'employee':i.employee,}):
			
			row = [i.employee,i.employee_name,i.branch,i.contractor,i.attendance_date]
			in_time=i.in_time
			if in_time:
				row.append(in_time.strftime('%H:%M'))
			else:
				row.append("")
			out_time=i.out_time
			if out_time:
				row.append(out_time.strftime('%H:%M'))
			else:
				row.append("")

			data.append(row)
	return data
