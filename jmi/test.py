from os import name
from os import name
from collections import namedtuple
import frappe
import requests
import xml.etree.ElementTree as ET
from cgi import print_environ
import requests,json
from datetime import date
from datetime import time,datetime
import xmltodict
from os import name
from os import name
from collections import namedtuple
import json
import datetime
from datetime import datetime,date
from calendar import monthrange
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from os import name
from os import name
from collections import namedtuple
import frappe
from numpy import empty
import pandas as pd
import json
import datetime
from frappe.permissions import check_admin_or_system_manager
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_url_to_form
import math
from datetime import date, timedelta,time
import math
from numpy import empty
import pandas as pd
import json
import datetime
from frappe.permissions import check_admin_or_system_manager
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_url_to_form
import math

@frappe.whitelist()
def employee_background(from_date, to_date):
	frappe.enqueue(
		mark_attendance_new, # python function or a module path as string
		queue="long", # one of short, default, long
		timeout=80000, # pass timeout manually
		is_async=True, # if this is True, method is run in worker
		now=False, # if this is True, method is run directly (not in a worker) 
		job_name='Attendance',
		from_date=from_date,
		to_date=to_date
	) 
	return 'ok'


@frappe.whitelist()
def bulk_att():
	from_date = "2023-09-21"
	to_date = "2023-09-21"
	frappe.enqueue(
		mark_attendance_new, # python function or a module path as string
		queue="long", # one of short, default, long
		timeout=80000, # pass timeout manually
		is_async=True, # if this is True, method is run in worker
		now=False, # if this is True, method is run directly (not in a worker) 
		job_name='Attendance _ Monthly',
		from_date=from_date,
		to_date=to_date
	) 
	return 'ok'

@frappe.whitelist()
def mark_attendance_new():
		from_date = "2023-09-21"
		to_date = "2023-09-21"
		checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where  date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=True) 
		if checkins:
			date = checkins[0].time
			from_date = datetime.strftime(date,'%Y-%m-%d')
			for c in checkins:
				print(c.name)
				if frappe.db.exists("Employee",{'name':c.employee,'status':"Active"}):
					att = mark_attendance_from_checkin(c.name,c.employee,c.time,c.device_id)
					if att:
						frappe.db.set_value("Employee Checkin",c.name, "skip_auto_attendance", "1")
		get_total_working_hours_jmi_plant_1_new(from_date,to_date)
		get_total_working_hours_except_jmi_plant_1_new(from_date , to_date)
		get_total_working_hours_vcp_vcr(from_date ,to_date)
		mark_absent_employee_new(from_date, to_date)
		return "OK"

def get_total_working_hours_jmi_plant_1_new(from_date , to_date):
	print("HI")
	attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
	for att in attendance:
		if att.branch == 'JMI Plant 1' and att.docstatus == 0:
			if att.in_time and att.out_time:
				str_working_hours = att.out_time - att.in_time
				time_d_float = str_working_hours.total_seconds()
				whrs = time_d_float/3600
				total_working_hours = "{:.2f}".format(whrs)			
				frappe.db.set_value('Attendance',att.name,'total_working_hours',total_working_hours) 
				if float(total_working_hours) > 8:
					frappe.set_value('Attendance',att.name,'status','Present')
					over_time_hours = float(total_working_hours) - 8
					if float(over_time_hours) >= 7:
						over_time_hours_1 = 8
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours_1)
					elif float(over_time_hours)  >= 4:
						ot = 4.50
						frappe.db.set_value('Attendance',att.name,'over_time_hours',ot)
					elif float(over_time_hours) >= 2:
						over_time_hours = 2.50
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours)
					elif  float(over_time_hours) < 2:
						over_time = 0
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time)
				elif float(total_working_hours) < 4:
					frappe.set_value('Attendance',att.name,'status','Absent')
				elif float (total_working_hours) >=4 and float(total_working_hours) < 7.5:
					frappe.set_value('Attendance',att.name,'status','Half Day')
					frappe.set_value('Attendance',att.name,'leave_type','Loss of Pay')	
				elif float(total_working_hours) >= 7.5:
					frappe.set_value('Attendance',att.name,'status','Present')
			if not (att.in_time and att.out_time):
				frappe.set_value('Attendance',att.name,'status','Absent')

def get_total_working_hours_except_jmi_plant_1_new(from_date , to_date):
	print("HI")
	attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
	for att in attendance:
		if att.branch != 'JMI Plant 1' and att.docstatus == 0:
			if att.in_time and att.out_time:
				str_working_hours = att.out_time - att.in_time
				time_d_float = str_working_hours.total_seconds()
				whrs = time_d_float/3600
				total_working_hours = "{:.2f}".format(whrs)			
				frappe.db.set_value('Attendance',att.name,'total_working_hours',total_working_hours) 
				if float(total_working_hours) > 8:
					frappe.set_value('Attendance',att.name,'status','Present')
					over_time_hours = float(total_working_hours) - 8
					if float(over_time_hours) >= 7:
						over_time_hours_1 = 7.5
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours_1)
					elif float(over_time_hours) >= 3:
						over_time_hours = 3.50
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours)
					elif float(over_time_hours) < 2:
						over_time = 0
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time)
				elif float(total_working_hours) < 4:
					frappe.set_value('Attendance',att.name,'status','Absent')
				elif float (total_working_hours) >=4 and float(total_working_hours) < 7.5:
					frappe.set_value('Attendance',att.name,'status','Half Day')
					frappe.set_value('Attendance',att.name,'leave_type','Loss of Pay')	
				elif float(total_working_hours) >= 7.5:
					frappe.set_value('Attendance',att.name,'status','Present')
			if not (att.in_time and att.out_time):
				frappe.set_value('Attendance',att.name,'status','Absent')

def get_total_working_hours_vcp_vcr(from_date ,to_date):
	print("HI")
	attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
	for att in attendance:
		if (att.branch == 'VCP' or att.branch == 'VCR') and att.docstatus == 0:
			if att.in_time and att.out_time:
				str_working_hours = att.out_time - att.in_time
				time_d_float = str_working_hours.total_seconds()
				whrs = time_d_float/3600
				total_working_hours = "{:.2f}".format(whrs)			
				frappe.db.set_value('Attendance',att.name,'total_working_hours',total_working_hours) 
				if float(total_working_hours) > 8:
					frappe.set_value('Attendance',att.name,'status','Present')
					over_time_hours = float(total_working_hours) - 8
					if float(over_time_hours) >= 7:
						over_time_hours_1 = 8
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours_1)
					elif float(over_time_hours) >= 3:
						over_time_hours = 4
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours)
					elif float(over_time_hours) < 2:
						over_time = 0
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time)
				elif float(total_working_hours) < 4:
					frappe.set_value('Attendance',att.name,'status','Absent')
				elif float (total_working_hours) >=4 and float(total_working_hours) < 8:
					frappe.set_value('Attendance',att.name,'status','Half Day')
					frappe.set_value('Attendance',att.name,'leave_type','Loss of Pay')	
				elif float(total_working_hours) >= 8:
					frappe.set_value('Attendance',att.name,'status','Present')
			if not (att.in_time and att.out_time):
				frappe.set_value('Attendance',att.name,'status','Absent')

def mark_absent_employee_new(from_date, to_date):
	print("HI")
	to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date()
	from_date = datetime.strptime(str(from_date),'%Y-%m-%d').date()
	dates = get_dates(from_date,to_date)
	for date in dates:
		employee = frappe.db.get_all('Employee',{'status':'Active','date_of_joining':['<=',date]})
		for emp in employee:
			hh = check_holiday(date,emp.name)
			if not hh:
				if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')}):
					att = frappe.new_doc("Attendance")
					att.employee = emp.name
					att.status = 'Absent'
					att.attendance_date = date
					att.save(ignore_permissions=True)
					frappe.db.commit()
			
def get_dates(from_date,to_date):
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	# frappe.errprint(no_of_days)
	dates = [add_days(from_date, i) for i in range(0, no_of_days)]
	# frappe.errprint(dates)
	return dates

def check_holiday(date,emp):
	holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
	holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
	left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
	if holiday:
		if holiday[0].weekly_off == 1:
			return "WW"
		else:
			return "HH"
			
def mark_attendance_from_checkin(checkin,employee,time,device):
	att_time = time.time()
	att_date = time.date()
	
# JMI PLANT 1       
	if device in ['BRM9222360384']:
		if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
			shift ='1'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '1'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
			shift ='G'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = 'G'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
			shift ='2'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '2'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)

		elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
			shift ='3'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '3'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
			shift ='4'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '4'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

# JMI PLANT 2 IN
	elif device in ['BRM9203461488']:
		if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
			shift ='1'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '1'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
			shift ='G'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = 'G'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
			shift ='2'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '2'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)

		elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
			shift ='3'
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '3'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
			shift ='4'
			print('4')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '4'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att
# JMI PLANT 3 IN
	elif device in ['BRM9193660282']:
		if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
			shift ='1'
			print('1')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '1'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
			shift ='G'
			print('G')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = 'G'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
			shift ='2'
			print('2')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '2'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)

		elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
			shift ='3'
			print('3')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '3'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
			shift ='4'
			print('4')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '4'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

# SEYON PLANT 1N
	elif device in ['BRM9211160652']:
		if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('08:00:00','%H:%M:%S').time():
			shift ='1'
			print('1')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '1'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
			shift ='G'
			print('G')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = 'G'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('10:30:00','%H:%M:%S').time() < att_time < datetime.strptime('11:30:00','%H:%M:%S').time():
			shift ='5'
			print('5')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '5'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
			shift ='2'
			print('2')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '2'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)

		elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
			shift ='3'
			print('3')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '3'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
			shift ='4'
			print('4')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '4'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att
# VCR PLANT IN
	elif device in ['BRM9215260842']:
		if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
			shift ='1-V'
			print('1-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '1-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
			shift ='G-V'
			print('G-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = 'G-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
			shift ='2-V'
			print('2-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '2-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)

		elif datetime.strptime('22:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:59:59','%H:%M:%S').time():
			shift ='3-V'
			print('3-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '3-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('08:00:00','%H:%M:%S').time():
			shift ='4-V'
			print('4-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '4-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('10:00:00','%H:%M:%S').time() < att_time < datetime.strptime('11:30:00','%H:%M:%S').time():
			shift ='5-V'
			print('5-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '5-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('18:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
			shift ='6-V'
			print('6-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '6-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

	  
# VCP PLANT IN
	elif device in ['BRM9222361257']:
		if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
			shift ='1-V'
			print('1-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '1-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
			shift ='G-V'
			print('G-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = 'G-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 
				return att

		elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
			shift ='2-V'
			print('2-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '2-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)

		elif datetime.strptime('22:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:59:59','%H:%M:%S').time():
			shift ='3-V'
			print('3-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '3-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('08:00:00','%H:%M:%S').time():
			shift ='4-V'
			print('4-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '4-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('10:00:00','%H:%M:%S').time() < att_time < datetime.strptime('11:30:00','%H:%M:%S').time():
			shift ='5-V'
			print('5-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '5-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

		elif datetime.strptime('18:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
			shift ='6-V'
			print('6-V')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			if not attendance:          
				att = frappe.new_doc('Attendance')
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '6-V'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				return att

	
	if device in ['BRM9222360383','BRM9222360378','BRM9222360385','BRM9222361258','BRM9222361360','BRM9222360379']:
		max_out = datetime.strptime('10:00:00', '%H:%M:%S').time()
		if att_time < max_out:
			yesterday = add_days(att_date,-1)
			checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and device_id in ('BRM9222360383','BRM9222360378','BRM9222360385','BRM9222361258','BRM9222361360','BRM9222360379') and date(time) = '%s' and time(time) < '%s' order by time "%(employee,att_date,max_out),as_dict=True)            
			att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
			if att:
				att = frappe.get_doc("Attendance",att)
				if att.docstatus == 0:
					if not att.out_time:
						if len(checkins) > 0:
							att.out_time = checkins[-1].time
						else:
							att.out_time = checkins[-1].time
						att.save(ignore_permissions=True)
						frappe.db.commit()
						frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
						return att
					else:
						return att
			else:
				att = frappe.new_doc("Attendance")
				att.employee = employee
				att.attendance_date = yesterday
				att.status = 'Absent'
				if len(checkins) > 0:
					att.out_time = checkins[-1].time
				else:
					att.out_time = checkins[-1].time
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
				return att
		else:
			checkins = frappe.db.sql("select name,time,docstatus from `tabEmployee Checkin` where employee ='%s' and device_id in ('BRM9222360383','BRM9222360378','BRM9222360385','BRM9222361258','BRM9222361360','BRM9222360379') and date(time) = '%s' order by time "%(employee,att_date),as_dict=True)
			att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
			if att:
				att = frappe.get_doc("Attendance",att)
				if att.docstatus == 0:
					if not att.out_time:
						if len(checkins) > 0:
							att.out_time = checkins[-1].time
						else:
							att.out_time = checkins[-1].time
						att.save(ignore_permissions=True)
						frappe.db.commit()
						frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
						return att
					else:
						return att
			else:
				att = frappe.new_doc("Attendance")
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Absent'
				if len(checkins) > 0:
					att.out_time = checkins[-1].time
				else:
					att.out_time = checkins[-1].time
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name) 
				return att


@frappe.whitelist()
def mark_employee_checkin():
	serial_number_list=["BRM9222360384","BRM9222360383","BRM9203461488","BRM9222360378","BRM9193660282","BRM9222360385","BRM9211160652","BRM9222361360","BRM9222361258","BRM9215260842","BRM9232260887"]
	from_date= "2023-10-17"
	to_date = '2023-10-19'
	# from_date = today()
	# to_date = add_days(today(),-1)
	print(from_date)
	print(to_date)
	for serial in serial_number_list:
		url = "http://192.168.1.189:8080/iclock/webapiservice.asmx?op=GetTransactionsLog"
		payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetTransactionsLog xmlns=\"http://tempuri.org/\">\n      <FromDate>%s</FromDate>\n      <ToDate>%s</ToDate>\n      <SerialNumber>%s</SerialNumber>\n      <UserName>tss</UserName>\n      <UserPassword>Tss@12345</UserPassword>\n      <strDataList></strDataList>\n    </GetTransactionsLog>\n  </soap:Body>\n</soap:Envelope>" % (from_date,to_date,serial)
		ET.headers = {
		'Content-Type': 'text/xml'
		}
		response = requests.request("POST", url, headers=ET.headers, data=payload)
		root=ET.fromstring(response.text)
		my_dict = xmltodict.parse(response.text)
		attlog = my_dict['soap:Envelope']['soap:Body']['GetTransactionsLogResponse']['strDataList']
		if attlog:
			print(attlog)
			mylist = attlog.split('\n')
			frappe.log_error(title=serial,message=mylist)
			for mydict in mylist:
				mytlist = mydict.split('\t')
				emp_id = mytlist[0]
				date_time = mytlist[1]
				log_type = mytlist[2]
				urls = "http://192.168.1.188/api/method/jmi.biometric_checkin.mark_checkin?employee=%s&time=%s&device_id=%s&log_type=%s" % (emp_id,date_time,serial,log_type)
				headers = { 'Content-Type': 'application/json','Authorization': 'token 2d42d97bd67d671: 8bb6689649df56c'}
				responses = requests.request('GET',urls,headers=headers,verify=False)
				res = json.loads(responses.text)
				print(emp_id)
	return "OK"


@frappe.whitelist()
def push_punch_hooks():
	job = frappe.db.exists('Scheduled Job Type', 'jmi.mark_attendance.mark_employee_checkin')
	if not job:
		emc = frappe.new_doc("Scheduled Job Type")
		emc.update({
			"method": 'jmi.mark_attendance.mark_employee_checkin',
			"frequency": 'Cron',
			"cron_format": '*/5 * * * *'
		})
		emc.save(ignore_permissions=True)

# def get_api_log():
# 	serial_number_list=["BRM9222360384","BRM9222360383","BRM9203461488","BRM9222360378","BRM9193660282","BRM9222360385","BRM9211160652","BRM9222361360","BRM9222361258","BRM9215260842","BRM9222361257","BRM9222360379"]
# 	from_date= "2023-08-21"
# 	to_date = '2023-08-30'
# 	for serial in serial_number_list:
# 		url = "http://192.168.1.189:8080/iclock/webapiservice.asmx?op=GetTransactionsLog"
# 		payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetTransactionsLog xmlns=\"http://tempuri.org/\">\n      <FromDate>%s</FromDate>\n      <ToDate>%s</ToDate>\n      <SerialNumber>%s</SerialNumber>\n      <UserName>tss</UserName>\n      <UserPassword>Tss@12345</UserPassword>\n      <strDataList></strDataList>\n    </GetTransactionsLog>\n  </soap:Body>\n</soap:Envelope>" % (from_date,to_date,serial)
# 		ET.headers = {
# 		'Content-Type': 'text/xml'
# 		}
# 		response = requests.request("POST", url, headers=ET.headers, data=payload)
# 		root=ET.fromstring(response.text)
# 		my_dict = xmltodict.parse(response.text)
# 		attlog = my_dict['soap:Envelope']['soap:Body']['GetTransactionsLogResponse']['strDataList']
# 		if attlog:
# 			mylist = attlog.split('\n')
# 			frappe.log_error(title=serial,message=mylist)