# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
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

def execute(filters=None):
	columns, data = [] ,[]
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	column = [
		_('Employee ID') + ':Data:120',
		_('Employee Name') + ':Data:120',
		_('Department') + ':Data:120',
        _('Designation') + ':Data:120',
        _('Shift') + ':Data:120',
        _('Out Time') + ':Data:200',
		_('Early By') + ':Data:150',
	]
	return column
    
def get_data(filters):
    data = []
    mydates = pd.date_range(filters.from_date, filters.to_date).tolist()
    employee = frappe.db.get_all("Employee",["*"])
    for emp in employee:
        for date in mydates:
            if frappe.db.exists("Attendance",{'employee':emp.employee,'status':'Present','attendance_date':date.date()}):
                out_time = frappe.get_value('Attendance',{'attendance_date':date.date()},["out_time","shift","attendance_date"])
                shift_end_time = frappe.get_value("Shift Type",{"name":out_time[1]},["end_time"])
                if out_time[0] and out_time[1]:
                    shift_time = dt.datetime.strptime(str(shift_end_time),"%H:%M:%S")
                    shift_end_time = dt.datetime.combine(out_time[2],shift_time.time())
                    if out_time[0] < shift_end_time:
                        early_by = shift_end_time - out_time[0]
                        frappe.errprint(early_by)
                        row = [emp.name,emp.employee_name,emp.department,emp.designation,out_time[1],out_time[0],early_by]
                        data.append(row)

    return data


