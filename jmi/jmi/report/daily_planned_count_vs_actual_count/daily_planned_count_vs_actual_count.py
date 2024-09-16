# Copyright (c) 2023, TEAMPRO and contributors
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
from functools import total_ordering
from itertools import count
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime, time
from numpy import true_divide
import pandas as pd
import datetime as dt

def execute(filters=None):
	columns, data = [], []
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
	employee_plan = frappe.get_single('CL Employee Plan').contractor_employee_plan
	for e in employee_plan:
		attendance = frappe.db.sql("""select count(status) as cnt from `tabAttendance` where attendance_date between '%s' and '%s' and status = 'Present' and branch = '%s' """%(filters.from_date, filters.to_date, e.plant), as_dict=1)[0]
		row = [e.plant, e.planned_count, attendance['cnt']]
		data.append(row)

	return data
