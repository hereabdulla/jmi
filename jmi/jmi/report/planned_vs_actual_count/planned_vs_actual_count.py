# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

# import frappe
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


def execute(filters=None):
	columns, data = [] ,[]
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	column = [
		_('Branch') + ':Data:200',
		_('Planned Count') + ':Data:200',
		_('Actual Count') + ':Data:200'
	]
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
				frappe.errprint(e.plant)
				attendance = frappe.db.sql("""select count(status) as cnt from `tabAttendance` where attendance_date = '%s' and status = 'Present' and branch = '%s' """%(filters.date,e.plant),as_dict=1)[0]
				row = [e.plant,e.planned_count,attendance['cnt']]
				data.append(row)
	
	return data

