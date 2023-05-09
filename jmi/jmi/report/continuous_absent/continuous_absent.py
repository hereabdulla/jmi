# Copyright (c) 2022, TeamPRO and contributors
# For license information, please see license.txt
from email.utils import formatdate 
import frappe
from frappe.utils.data import cstr
from frappe.utils import date_diff, add_months,today,add_days,nowdate,flt,format_date
import calendar
from frappe.utils.file_manager import get_file
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from datetime import date, datetime, timedelta
from frappe import _, get_file_items
from datetime import datetime
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form
from frappe.utils import add_months, add_days, format_time, today, nowdate, getdate, format_date
import calendar
import pandas as pd
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form
from frappe.utils.background_jobs import enqueue
from frappe.desk.query_report import background_enqueue_run

def execute(filters=None):
    columns, data = [] ,[]
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    column = [
        _('Employee ID') + ':Data:120',
        _('Employee Name') + ':Data:150',
        _('Designation') + ':Data:150',
        _('From Date') + ':Data:120',
        _('Absent Days') + ':Data:100',
       
    ]
    return column

def get_data(filters):
    data = []
    if filters.employee:
        employee = frappe.db.get_all('Employee',{'status':'Active',"name":filters.employee},['*'])
    else:
        employee = frappe.db.get_all('Employee',{'status':'Active'},['*'])
    for emp in employee:
        row = [emp.name,emp.employee_name,emp.designation]
        date_string = '2022-01-01'
        frm = datetime.strptime(date_string, '%Y-%m-%d').date()
        to = datetime.strptime(today(),'%Y-%m-%d').date()
        delta = to - frm
        dates = []
        for d in range(delta.days + 1):
            day = frm + timedelta(days=d) 
            dates.append(str(day))
        l = []
        for i in dates:
            l.insert(0,i)
        count = 0
        continuous_absent_count = 0 
        f_date = ''
        for day in l:
            status = frappe.get_value('Attendance',{'attendance_date':day,'employee':emp.name},['status'])
            if status:
                if status == "Absent":
                    count = count + 1
                    if count >= 3:
                        continuous_absent_count =  count 
                else:
                    count = 0
                    f_date = add_days(day,1)
                    break
            else:
                if day == today():
                    f_date = date_string
                else:
                    f_date = day
        frappe.errprint(continuous_absent_count)
        row.append(f_date)
        row.append(continuous_absent_count)
        if not continuous_absent_count == 0:
            data.append(row)
        count = 0
        continuous_absent_count = 0
        f_date = ''

    return data