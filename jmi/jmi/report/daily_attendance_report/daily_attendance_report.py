# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe

# import frappe
from frappe.model.document import Document
import frappe
from frappe.model.document import Document
import math
import frappe
import json
import requests
import pandas as pd
import openpyxl
from six import BytesIO
from frappe.utils import (
    flt,
    cint,
    cstr,
    get_html_format,
    get_url_to_form,
    gzip_decompress,
    format_duration,
    today
)
from datetime import timedelta, datetime
# from __future__ import unicode_literals
from six.moves import range
from six import string_types
import frappe
import json
from frappe.utils import getdate,get_time, cint, add_months, date_diff, add_days, nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from datetime import datetime
from calendar import monthrange

from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
import pandas as pd 
# from __future__ import unicode_literals
from functools import total_ordering
from itertools import count,groupby
# import more_itertools
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date,now
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide 
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
		_('Employee Name') + ':Data:150',
		_('Branch') + ':Data:150',

		_('Contractor') + ':Data:190',
		_('Attendance Date') + ':Data:120',
        _('Status') + ':Data:120',
		_('In Time') + ':Data:220',
		_('Out Time') + ':Data:220'
	]
	return column

def get_data(filters):
	data = []
	mydates = pd.date_range(filters.from_date,filters.to_date).tolist()
	for date in mydates:
		if filters.employee:
			attendance = frappe.get_all("Attendance",{"attendance_date":date.date(),"employee":filters.employee},['*'])
		elif filters.contractor and filters.branch:
			attendance = frappe.db.sql("""select * from `tabAttendance` where attendance_date ='%s' and branch = '%s' and contractor = '%s' """%(date.date(),filters.branch,filters.contractor),as_dict=1)
		elif filters.contractor and filters.branch and filters.employee:
			attendance = frappe.get_all("Attendance",{"attendance_date":date.date(),"branch":filters.branch,"employee":filters.employee},['*'])
		elif filters.contractor:
			attendance = frappe.get_all("Attendance",{"attendance_date":date.date(),"contractor":filters.contractor},['*'])
		elif filters.branch :
			attendance = frappe.get_all("Attendance",{"attendance_date":date.date(),"branch":filters.branch},['*'])
		
		else:
			attendance = frappe.get_all("Attendance",{"attendance_date":date.date()},['*'])

		for i in attendance:
			if frappe.db.exists("Employee",{'employee':i.employee,}):
				
				row = [i.employee,i.employee_name,i.branch,i.contractor,i.attendance_date,i.status,i.in_time,i.out_time]
				data.append(row)
						




	
	return data

