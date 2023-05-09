# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
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
		_('Employee ID') + ':Data:100',
		_('Employee Name') + ':Data:120',
		_('Department') + ':Data:120',
		_('Shift') + ':Data:80',
        _('In Time') + ':Data:170',
		_('Late By') + ':Data:120'
	]
	return column

def get_data(filters):
	data = []
	mydates = pd.date_range(filters.from_date,filters.to_date).tolist()
	for date in mydates:
		attendance = frappe.get_all("Attendance",{"attendance_date":date.date()},['*'])
		for i in attendance:
			shift_time = frappe.get_value("Shift Type",{'name':i.shift},["start_time"])
			if frappe.db.exists("Employee",{'employee':i.employee,}):
					if i.shift and i.in_time:
						shift_start_time = dt.datetime.strptime(str(shift_time),"%H:%M:%S")
						start_time = dt.datetime.combine(i.attendance_date,shift_start_time.time())
						if i.in_time > start_time:
							late_by = i.in_time - start_time
							frappe.errprint(late_by)
							row = [i.name,i.employee_name,i.department,i.shift,i.in_time,late_by]
							data.append(row)
						




	
	return data

