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
		_('Shift') + ':Data:120',
		_('Employee Count') + ':Data:150',

	]
	return column

def get_data(filters):
	data = []
	row=[]
	shift_type=frappe.db.get_all("Shift Type",['*'],order_by='name ASC')
	for s in shift_type:
		frappe.errprint(s.name)
		h = frappe.get_value('Branch Shift',{'branch':filters.branch,'parent':s.name},['branch'])
		if h == filters.branch:
			frappe.errprint(h)
			attendance = frappe.db.sql("""select count(*) as count from `tabAttendance` where attendance_date ='%s' and branch = '%s' and shift='%s'"""%(filters.date,filters.branch,s.name),as_dict=1)
			row = [s.name,attendance[0]['count']]
			data.append(row)
	return data
