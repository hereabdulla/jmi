import requests
import xml.etree.ElementTree as ET
from cgi import print_environ
import requests,json
from datetime import date
from datetime import time,datetime
import xmltodict
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
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,format_date,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime,date
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_url_to_form,money_in_words
import math
from frappe.utils.data import ceil, get_time, get_year_start
from datetime import datetime,date
from datetime import time

@frappe.whitelist()
def get_mandays_amount(contractor,branch):
	man_days_amount = frappe.db.sql("""select sum(rounded_total) from `tabSalary Slip` where docstatus != 2  and contractor='%s' and branch = '%s' """%(contractor,branch),as_dict = 1)[0]
	return[man_days_amount['sum(rounded_total)']]

@frappe.whitelist()
def cron_job_checkin():
	job = frappe.db.exists('Scheduled Job Type', 'mark_employee_checkin')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'jmi.custom.mark_employee_checkin',
			"frequency" : 'Cron',
			"cron_format" : '*/30 * * * *'
		})
		sjt.save(ignore_permissions=True)

@frappe.whitelist()
def mark_employee_checkin():
	from_date = add_days(today(),-1)  
	to_date = today()
	# from_date='2024-08-06'
	# to_date='2024-08-06' 
	device = frappe.db.get_all("Device Details",['*'])
	if device:
		for s in device:
			serial = s.device_serial_number 
			url = "http://192.168.1.189:8080/iclock/webapiservice.asmx?op=GetTransactionsLog"
			payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetTransactionsLog xmlns=\"http://tempuri.org/\">\n      <FromDate>%s</FromDate>\n      <ToDate>%s</ToDate>\n      <SerialNumber>%s</SerialNumber>\n      <UserName>tss</UserName>\n      <UserPassword>Tss@12345</UserPassword>\n      <strDataList></strDataList>\n    </GetTransactionsLog>\n  </soap:Body>\n</soap:Envelope>" % (from_date,to_date,serial)
			ET.headers = {
			'Content-Type': 'text/xml'
			}
			response = requests.request("POST", url, headers=ET.headers, data=payload)
			root=ET.fromstring(response.text)
			my_dict = xmltodict.parse(response.text)
			try:
				attlog = my_dict['soap:Envelope']['soap:Body']['GetTransactionsLogResponse']['strDataList']
			except KeyError as e:
				print(f"KeyError: {e}. Handling missing key.")
				attlog = []
			if attlog:
				mylist = attlog.split('\n')
				for mydict in mylist:
					mytlist = mydict.split('\t')
					emp_id = mytlist[0]
					date_time = mytlist[1]
					log_type = mytlist[2]
					urls = "http://192.168.1.188/api/method/jmi.biometric_checkin.mark_checkin?employee=%s&time=%s&device_id=%s&log_type=%s" % (emp_id,date_time,serial,log_type)
					headers = { 'Content-Type': 'application/json','Authorization': 'token 2d42d97bd67d671: 8bb6689649df56c'}
					responses = requests.request('GET',urls,headers=headers,verify=False)
					res = json.loads(responses.text)
				
@frappe.whitelist()
def att_background_frontend(from_date, to_date, plant):
	# to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date()
	# from_date = datetime.strptime(str(from_date),'%Y-%m-%d').date()
	dates = get_dates(from_date,to_date)
	for date in dates:
		checkin = frappe.db.sql("""select count(*) as count from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) = '%s' order by time ASC """%(date),as_dict=True) 
		if plant == '':
			checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) = '%s' order by time ASC"""%(date),as_dict=True) 
		else:
			checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) = '%s' and branch = '%s' order by time ASC"""%(date,plant),as_dict=True) 
		if checkins:
			for c in checkins:
				if frappe.db.exists("Employee",{'name':c.employee,'status':"Active"}):
					att = mark_attendance_from_checkin(c.name,c.employee,c.time,c.device_id,c.log_type,plant)
					if att:
						frappe.db.set_value("Employee Checkin",c.name, "skip_auto_attendance", "1")
	get_total_working_hours_jmi_plant_1_new(from_date,to_date,plant)
	get_total_working_hours_except_jmi_plant_1_new(from_date,to_date,plant)
	get_total_working_hours_vcp_vcr(from_date,to_date,plant)
	mark_absent_employee_new(from_date,to_date,plant)
	return "OK"


@frappe.whitelist()
def cron_job_att():
	job = frappe.db.exists('Scheduled Job Type', 'mark_attendance_new')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'jmi.custom.mark_attendance_new',
			"frequency" : 'Cron',
			"cron_format" : '*/45 * * * *'
		})
		sjt.save(ignore_permissions=True)

@frappe.whitelist()
def mark_attendance_manual():
	from_date='2024-08-30'
	to_date='2024-08-31' 
	dates = get_dates(from_date,to_date)
	plant = ''
	for date in dates:
		checkin = frappe.db.sql("""select count(*) as count from `tabEmployee Checkin` where date(time) = '%s' order by time ASC """%(date),as_dict=True) 
		checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) = '%s' order by time ASC"""%(date),as_dict=True)
		if checkins:
			for c in checkins:
				if frappe.db.exists("Employee",{'name':c.employee,'status':"Active"}):
					att = mark_attendance_from_checkin(c.name,c.employee,c.time,c.device_id,c.log_type,plant)
					if att:
						frappe.db.set_value("Employee Checkin",c.name, "skip_auto_attendance", "1")
	get_total_working_hours_jmi_plant_1_new(from_date,to_date,plant)
	get_total_working_hours_except_jmi_plant_1_new(from_date,to_date,plant)
	get_total_working_hours_vcp_vcr(from_date,to_date,plant)
	mark_absent_employee_new(from_date,to_date,plant)
	return "OK"

@frappe.whitelist()
def mark_employee_checkin_manual():
	from_date='2024-09-09'
	to_date='2024-09-09'
	device = frappe.db.get_all("Device Details",['*'])
	# device = frappe.db.sql("""SELECT * FROM `tabDevice Details` WHERE device_name LIKE '%VCP%'""",as_dict=True)
	if device:
		for s in device:
			serial = s.device_serial_number 
			# serial = 'BRM9222361261'
			url = "http://192.168.1.189:8080/iclock/webapiservice.asmx?op=GetTransactionsLog"
			payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetTransactionsLog xmlns=\"http://tempuri.org/\">\n      <FromDate>%s</FromDate>\n      <ToDate>%s</ToDate>\n      <SerialNumber>%s</SerialNumber>\n      <UserName>tss</UserName>\n      <UserPassword>Tss@12345</UserPassword>\n      <strDataList></strDataList>\n    </GetTransactionsLog>\n  </soap:Body>\n</soap:Envelope>" % (from_date,to_date,serial)
			ET.headers = {
			'Content-Type': 'text/xml'
			}
			response = requests.request("POST", url, headers=ET.headers, data=payload)
			root=ET.fromstring(response.text)
			my_dict = xmltodict.parse(response.text)
			try:
				attlog = my_dict['soap:Envelope']['soap:Body']['GetTransactionsLogResponse']['strDataList']
			except KeyError as e:
				print(f"KeyError: {e}. Handling missing key.")
				attlog = []
			if attlog:
				mylist = attlog.split('\n')
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

@frappe.whitelist()
def mark_attendance_new():
	from_date = today()
	to_date = today()
	# from_date='2024-07-20'
	# to_date='2024-07-20' 
	dates = get_dates(from_date,to_date)
	plant = ''
	for date in dates:
		checkin = frappe.db.sql("""select count(*) as count from `tabEmployee Checkin` where date(time) = '%s' order by time ASC """%(date),as_dict=True) 
		checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) = '%s' order by time ASC"""%(date),as_dict=True) 
		if checkins:
			for c in checkins:
				if frappe.db.exists("Employee",{'name':c.employee,'status':"Active"}):
					att = mark_attendance_from_checkin(c.name,c.employee,c.time,c.device_id,c.log_type,plant)
					if att:
						frappe.db.set_value("Employee Checkin",c.name, "skip_auto_attendance", "1")
	get_total_working_hours_jmi_plant_1_new(from_date,to_date,plant)
	get_total_working_hours_except_jmi_plant_1_new(from_date,to_date,plant)
	get_total_working_hours_vcp_vcr(from_date,to_date,plant)
	mark_absent_employee_new(from_date,to_date,plant)
	return "OK"

def get_total_working_hours_jmi_plant_1_new(from_date , to_date,plant):
	if plant == '':
		attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
	else:
		attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' and branch = '%s' """%(from_date,to_date,plant),as_dict=True)	
	for att in attendance:
		# print(frappe.db.exists('Employee',{'status':'Active','name':att.employee}))
		if frappe.db.exists('Employee',{'status':'Active','name':att.employee}):
			if att.branch == 'JMI Plant 1':
				if att.in_time and att.out_time and att.docstatus==0:
					str_working_hours = att.out_time - att.in_time
					time_d_float = str_working_hours.total_seconds()
					whrs = time_d_float/3600
					total_working_hours = "{:.2f}".format(whrs)			
					frappe.db.set_value('Attendance',att.name,'total_working_hours',total_working_hours) 
					if float(total_working_hours) >= 8:
						frappe.set_value('Attendance',att.name,'status','Present')
						over_time_hours = float(total_working_hours) - 8
						if float(over_time_hours) >= 7:
							over_time_hours_1 = 7.50
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
		print(att.name)

def get_total_working_hours_except_jmi_plant_1_new(from_date , to_date ,plant):
	if plant == '':
		attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
	else:
		attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' and branch = '%s' """%(from_date,to_date,plant),as_dict=True)	
	for att in attendance:
		if frappe.db.exists('Employee',{'status':'Active','name':att.employee}):
			if att.branch in ('JMI Plant 2', 'JMI Plant 3', 'VCT', 'Seyoon'):
				if att.in_time and att.out_time and att.docstatus != 2:
					str_working_hours = att.out_time - att.in_time
					time_d_float = str_working_hours.total_seconds()
					whrs = time_d_float/3600
					total_working_hours = "{:.2f}".format(whrs)			
					frappe.db.set_value('Attendance',att.name,'total_working_hours',total_working_hours) 
					if float(total_working_hours) >= 8:
						frappe.set_value('Attendance',att.name,'status','Present')
						over_time_hours = float(total_working_hours) - 8
						if float(over_time_hours) >= 7:
							over_time_hours_1 = 7.5
							frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours_1)
						elif float(over_time_hours) >= 4:
							over_time_hours = 3.50
							frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours)
						elif float(over_time_hours) >= 2:
							over_time_hours_2 = 2.50
							frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours_2)
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
				if not (att.in_time and att.out_time) and att.docstatus!=2:
					frappe.set_value('Attendance',att.name,'status','Absent')
		print(att.name)

def get_total_working_hours_vcp_vcr(from_date ,to_date,plant):
	if plant == '':
		attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
	else:
		attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' and branch = '%s' """%(from_date,to_date,plant),as_dict=True)
	for att in attendance:
		if (att.branch in ('VCP', 'VCR')):
			if att.in_time and att.out_time and att.docstatus != 2:
				str_working_hours = att.out_time - att.in_time
				time_d_float = str_working_hours.total_seconds()
				whrs = time_d_float/3600
				total_working_hours = "{:.2f}".format(whrs)			
				frappe.db.set_value('Attendance',att.name,'total_working_hours',total_working_hours) 
				if float(total_working_hours) >= 8:
					frappe.set_value('Attendance',att.name,'status','Present')
					over_time_hours = float(total_working_hours) - 8
					if float(over_time_hours) >= 7:
						over_time_hours_1 = 8
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours_1)
					elif float(over_time_hours) >= 4:
						over_time_hours = 4
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours)
					elif att.branch == 'VCP' and float(over_time_hours) >= 2:
						over_time = 2.50
						frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time)
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
		print(att.name)

def mark_absent_employee_new(from_date, to_date ,plant):
	to_date = datetime.strptime(str(to_date),'%Y-%m-%d').date()
	from_date = datetime.strptime(str(from_date),'%Y-%m-%d').date()
	dates = get_dates(from_date,to_date)
	for date in dates:
		if plant == '':
			employee = frappe.db.get_all('Employee',{'status':'Active','date_of_joining':['<=',date]})
		else:
			employee = frappe.db.get_all('Employee',{'status':'Active','date_of_joining':['<=',date],'branch':plant})
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
	dates = [add_days(from_date, i) for i in range(0, no_of_days)]
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
			
def mark_attendance_from_checkin(checkin,employee,time,device,log_type,plant):
	att_time = time.time()
	att_date = time.date()
	device_name = frappe.db.get_value('Device Details', {'device_serial_number': device}, ['device_name'])
	if log_type == "IN":
		shift = ''
		shift1 = frappe.db.get_value('Shift Type',{'name':'1'},['checkin_start_time','checkin_to_time'])
		shift2 = frappe.db.get_value('Shift Type',{'name':'2'},['checkin_start_time','checkin_to_time'])
		shift3 = frappe.db.get_value('Shift Type',{'name':'3'},['checkin_start_time','checkin_to_time'])
		shift4 = frappe.db.get_value('Shift Type',{'name':'4'},['checkin_start_time','checkin_to_time'])
		shift5 = frappe.db.get_value('Shift Type',{'name':'5'},['checkin_start_time','checkin_to_time'])
		shift5p1 = frappe.db.get_value('Shift Type',{'name':'5 - P1'},['checkin_start_time','checkin_to_time'])
		shift6s = frappe.db.get_value('Shift Type',{'name':'6 - S'},['checkin_start_time','checkin_to_time'])
		shift6v = frappe.db.get_value('Shift Type',{'name':'6 - V'},['checkin_start_time','checkin_to_time'])
		shiftg = frappe.db.get_value('Shift Type',{'name':'G'},['checkin_start_time','checkin_to_time'])
		shift7vcp = frappe.db.get_value('Shift Type',{'name':'7 - VCP'},['checkin_start_time','checkin_to_time'])
		shift8vcp = frappe.db.get_value('Shift Type',{'name':'8 - VCP'},['checkin_start_time','checkin_to_time'])
		# All
		att_time_seconds = att_time.hour * 3600 + att_time.minute * 60 + att_time.second
		if shift1[0].total_seconds() < att_time_seconds < shift1[1].total_seconds():
			shift = '1'
		# # All
		if shift2[0].total_seconds() < att_time_seconds < shift2[1].total_seconds():
			shift = '2'
		# # All
		if shift3[0].total_seconds() < att_time_seconds < shift3[1].total_seconds():
			shift = '3'
		# # All
		if shiftg[0].total_seconds() < att_time_seconds < shiftg[1].total_seconds():
			shift = 'G'
		# # All except P1
		if device_name in ['JMI P2 IN','JMI P3 IN','Seyoon IN','VCR IN','VCP IN']:
			if shift5[0].total_seconds() < att_time_seconds < shift5[1].total_seconds():
				shift = '5'
		# # P1
		elif device_name == 'JMI P1 IN':
			if shift5p1[0].total_seconds() < att_time_seconds < shift5p1[1].total_seconds():
				shift = '5 - P1'
		# # Seyoon
		elif device_name == 'Seyoon IN':
			if shift6s[0].total_seconds() < att_time_seconds < shift6s[1].total_seconds():
				shift = '6 - S'
		# # VCR/VCR
		elif device_name in ['VCR IN','VCP IN'] :
			if device_name in ['VCR IN','VCP IN']:
				if shift6v[0].total_seconds() < att_time_seconds < shift6v[1].total_seconds():
					shift = "6 - V"
			elif device_name == 'VCP IN':
				if shift7vcp[0].total_seconds() < att_time_seconds < shift7vcp[1].total_seconds():
					shift = "7 - VCP"
				if shift8vcp[0].total_seconds() < att_time_seconds < shift8vcp[1].total_seconds():
					shift = "8 - VCP"
		checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where employee = '%s' and log_type = "IN" and date(time) = '%s' order by time ASC"""%(employee,att_date),as_dict=True)     
		attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})    
		if not attendance:  
			att = frappe.new_doc('Attendance')
			att.employee = employee
			att.attendance_date = att_date
			att.status = "Absent"
			att.shift = shift
			att.in_time = checkins[0].time
			att.total_wh = ''
			att.late_hours = ''
			att.save(ignore_permissions=True)
			frappe.db.commit()
			for c in checkins:
				frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
				frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
			return att
		else:
			att = frappe.get_doc('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})
			if not att.attendance_regularize:
				att.employee = employee
				att.attendance_date = att_date
				att.status = "Absent"
				att.shift = shift
				att.in_time = checkins[0].time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				for c in checkins:
					frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
					frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
				return att
		
	elif log_type == "OUT":
		if device_name in ['JMI P1 OUT','JMI P2 OUT','JMI P3 OUT','VCR OUT','Seyoon OUT','VCP OUT','VCR OUT NEW']:
			max_out = datetime.strptime('10:00:00', '%H:%M:%S').time()
			device_id =  frappe.db.sql("""SELECT device_serial_number FROM `tabDevice Details` WHERE device_name LIKE '%OUT'""", as_dict=True) 
			device_id_list = []
			for d in device_id:
				data = d.device_serial_number
				device_id_list.append(data)
			if att_time < max_out:
				yesterday = add_days(att_date,-1)
				checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and device_id in ('CUB7242000518','BRM9222360378','BRM9232760084','BRM9222360379','BRM9222361360','BRM9232260887','BRM9222361259') and date(time) = '%s' and time(time) < '%s' order by time  ASC"%(employee,att_date,max_out),as_dict=True)            
				att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
				if att:
					att = frappe.get_doc("Attendance",att)
					if att.docstatus == 0:
						if not att.attendance_regularize:
							if not att.out_time :
								if att.shift == '':
									if checkins:
										if len(checkins) > 0:
											att.shift = get_actual_shift(get_time(checkins[-1].time))
											att.out_time = checkins[-1].time
											for c in checkins:
												frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
												frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
										else:
											att.shift = get_actual_shift(get_time(checkins[0].time))
											att.out_time = checkins[0].time
											frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
											frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
								elif att.shift in['1','4']:
									if checkins:
										if len(checkins) > 0:
											att.shift = get_actual_shift(get_time(checkins[-1].time))
											att.out_time = checkins[-1].time
											for c in checkins:
												frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
												frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
										else:
											att.shift = get_actual_shift(get_time(checkins[0].time))
											att.out_time = checkins[0].time or ''
											frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
											frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
								else:
									if checkins:
										if len(checkins) > 0:
											att.out_time = checkins[-1].time
											for c in checkins:
												frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
												frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
										else:
											att.out_time = checkins[0].time
											frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
											frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
								att.save(ignore_permissions=True)
								frappe.db.commit()
								return att
						else:
							return att
				else:
					att = frappe.new_doc("Attendance")
					att.employee = employee
					att.attendance_date = yesterday
					att.status = 'Absent'
					if checkins:
						if len(checkins) > 0:
							att.shift = get_actual_shift(get_time(checkins[-1].time))
							att.out_time = checkins[-1].time
							for c in checkins:
								frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
								frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
						else:
							att.shift = get_actual_shift(get_time(checkins[0].time))
							att.out_time = checkins[0].time
							frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
							frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
					att.save(ignore_permissions=True)
					frappe.db.commit()
					return att
			else:
				checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee ='%s' and device_id in ('CUB7242000518','BRM9222360378','BRM9232760084','BRM9222360379','BRM9222361360','BRM9232260887','BRM9222361259') and date(time) = '%s' order by time ASC"%(employee,att_date),as_dict=True)
				att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
				if att:
					att = frappe.get_doc("Attendance",att)
					if att.docstatus == 0:
						if not att.attendance_regularize:
							if not att.out_time:
								if att.shift == '':
									if len(checkins) > 0:
										att.shift = get_actual_shift(get_time(checkins[-1].time))
										att.out_time = checkins[-1].time
										for c in checkins:
											frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
											frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
									else:
										att.shift = get_actual_shift(get_time(checkins[0].time))
										att.out_time = checkins[0].time
										frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
										frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
								elif att.shift == ['1','4']:
									if len(checkins) > 0:
										att.shift = get_actual_shift(get_time(checkins[-1].time))
										att.out_time = checkins[-1].time
										for c in checkins:
											frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
											frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
									else:
										att.shift = get_actual_shift(get_time(checkins[0].time))
										att.out_time = checkins[0].time
										frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
										frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
								else:
									if len(checkins) > 0:
										att.out_time = checkins[-1].time
										for c in checkins:
											frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
											frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
									else:
										att.out_time = checkins[0].time
										frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
										frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
								att.save(ignore_permissions=True)
								frappe.db.commit()
								return att
						else:
							return att
				else:
					att = frappe.new_doc("Attendance")
					att.employee = employee
					att.attendance_date = att_date
					att.status = 'Absent'
					if len(checkins) > 0:
						att.shift = get_actual_shift(get_time(checkins[0].time))
						att.out_time = checkins[-1].time
						for c in checkins:
							frappe.db.set_value('Employee Checkin',c.name,'skip_auto_attendance','1')
							frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
					else:
						att.shift = get_actual_shift(get_time(checkins[0].time))
						att.out_time = checkins[0].time
						frappe.db.set_value('Employee Checkin',checkins[0].name,'skip_auto_attendance','1')
						frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
					att.save(ignore_permissions=True)
					frappe.db.commit()
					return att

def is_between(time, time_range):
	if time_range[1] < time_range[0]:
		return time >= time_range[0] or time <= time_range[1]
	return time_range[0] <= time <= time_range[1]

def get_actual_shift(get_shift_time):
	from datetime import datetime
	from datetime import date, timedelta,time
	shift1 = frappe.db.get_value('Shift Type',{'name':'1'},['checkout_start_time','checkout_to_time'])
	shift2 = frappe.db.get_value('Shift Type',{'name':'2'},['checkout_start_time','checkout_to_time'])
	shift3 = frappe.db.get_value('Shift Type',{'name':'3'},['checkout_start_time','checkout_to_time'])
	shift4 = frappe.db.get_value('Shift Type',{'name':'4'},['checkout_start_time','checkout_to_time'])
	shift5 = frappe.db.get_value('Shift Type',{'name':'5'},['checkout_start_time','checkout_to_time'])
	shift5p1 = frappe.db.get_value('Shift Type',{'name':'5 - P1'},['checkout_start_time','checkout_to_time'])
	shift6s = frappe.db.get_value('Shift Type',{'name':'6 - S'},['checkout_start_time','checkout_to_time'])
	shift6v = frappe.db.get_value('Shift Type',{'name':'6 - V'},['checkout_start_time','checkout_to_time'])
	shiftg = frappe.db.get_value('Shift Type',{'name':'G'},['checkout_start_time','checkout_to_time'])
	shift7vcp = frappe.db.get_value('Shift Type',{'name':'7 - VCP'},['checkout_start_time','checkout_to_time'])
	shift8vcp = frappe.db.get_value('Shift Type',{'name':'8 - VCP'},['checkout_start_time','checkout_to_time'])
	att_time_seconds = get_shift_time.hour * 3600 + get_shift_time.minute * 60 + get_shift_time.second
	shift = ''
	if shift3[0].total_seconds() < att_time_seconds < shift3[1].total_seconds():
			shift = '3'
	if shift1[0].total_seconds() < att_time_seconds < shift1[1].total_seconds():
			shift = '1'
	if shiftg[0].total_seconds() < att_time_seconds < shiftg[1].total_seconds():
			shift = 'G'
	if shift2[0].total_seconds() < att_time_seconds < shift2[1].total_seconds():
			shift = '2'
	if shift4[0].total_seconds() < att_time_seconds < shift4[1].total_seconds():
			shift = '4'
	return shift   

# def get_api_log():
#   serial_number_list = []
#	serial_number = frappe.db.get_all("Device Details",['*'])
# 	serial_number_list.append(serial_number)
# 	from_date= "2023-09-21"
# 	to_date = '2023-10-19'
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
# 	return "OK"


@frappe.whitelist() 
def checkin_bulk_upload_csv():
	from frappe.utils.file_manager import get_file
	_file = frappe.get_doc("File", {"file_name": "test393b01.csv"})
	filepath = get_file("test393b01.csv")
	pps = read_csv_content(filepath[1])
	for pp in pps:
		if frappe.db.exists('Employee',{'device_code':pp[0]}):
			if not frappe.db.exists('Employee Checkin',{'employee':pp[0],'time':pp[1]}):
				ec = frappe.new_doc('Employee Checkin')
				ec.employee = frappe.get_value('Employee',{'device_code':pp[0]},['name'])
				ec.device_code = pp[0].upper()
				ec.time = pp[1]
				ec.device_id = pp[3]
				ec.log_type = 'OUT'
				ec.save(ignore_permissions=True)
				frappe.db.commit()
		else:
			if not frappe.db.exists('Unregistered Employee Checkin',{'employee':pp[0],'time':pp[1]}):
				uec = frappe.new_doc('Unregistered Employee Checkin')
				uec.employee = pp[0].upper()
				uec.time = pp[1]
				uec.device_id = pp[3]
				uec.log_type = 'OUT'
				if pp[3] == "BRM9232760454":
					uec.plant_with_type == "P1 IN"
				elif pp[3] == "CUB7242000518":
					uec.plant_with_type == "P1 OUT" 
				elif pp[3] == "BRM9203461488":
					uec.plant_with_type == "P2 IN" 
				elif pp[3] == "BRM9222360378":
					uec.plant_with_type == "P2 OUT" 
				elif pp[3] == "BRM9193660282":
					uec.plant_with_type == "P3 IN" 
				elif pp[3] == "BRM9232760084":
					uec.plant_with_type == "P4 OUT" 
				elif pp[3] == "BRM9211160652":
					uec.plant_with_type == "Seyoon IN" 
				elif pp[3] == "BRM9222361360":
					uec.plant_with_type == "Seyoon OUT" 
				elif pp[3] == "BRM9222361258":
					uec.plant_with_type == "VCR IN" 
				elif pp[3] == "BRM9215260842":
					uec.plant_with_type == "VCR OUT" 
				elif pp[3] == "BRM9222361257":
					uec.plant_with_type == "VCP IN" 
				elif pp[3] == "BRM9232260887":
					uec.plant_with_type == "VCP OUT"
				uec.save(ignore_permissions=True)
				frappe.db.commit()

@frappe.whitelist()
def cron_att_report():
	job = frappe.db.exists('Scheduled Job Type', 'daily_att_report')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'jmi.email_alerts.daily_att_report',
			"frequency" : 'Cron',
			"cron_format" : '00 12 * * *'
		})
		sjt.save(ignore_permissions=True)

@frappe.whitelist()
def cron_attreg_report():
	job = frappe.db.exists('Scheduled Job Type', 'att_reg')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")  
		sjt.update({
			"method" : 'jmi.email_alerts.att_reg',
			"frequency" : 'Cron',
			"cron_format" : '00 12 * * *'
		})
		sjt.save(ignore_permissions=True)	

@frappe.whitelist()
def set_status(doc,method):
	if doc.workflow_state == "Active":
		frappe.db.set_value("Employee",doc.name,'status',"Active")
		frappe.db.set_value("Employee",doc.name,'relieving_date','')
	if doc.workflow_state == "Left":
		frappe.db.set_value("Employee",doc.name,'status',"Left")
		if doc.relieving_date == '':
			frappe.throw(_('Enter the Reliving Date'))

@frappe.whitelist()
def validate_salary_structure_assignment(doc, method):
	employees = frappe.get_all("Employee", {'status': "Active", 'branch': doc.branch, 'contractor': doc.contractor, 'date_of_joining': ['<=', doc.end_date]})
	for employee in employees:
		if not frappe.db.exists("Salary Structure Assignment", {"employee": employee.name, 'docstatus': 1}):
			frappe.throw(f"Salary structure is not assigned for employee: {employee.name}")

@frappe.whitelist()
def get_contractor(name):
	doc = frappe.get_doc("Branch", name)
	states = [state.contractor for state in doc.contractor_list]
	return states

@frappe.whitelist()
def get_designation(name):
	doc = frappe.get_doc("Contractor", name)
	states = [state.designation for state in doc.designation]
	return states

@frappe.whitelist()
def update_att_reg():
	att_reg = frappe.db.sql("""SELECT * FROM `tabAttendance Regularize` WHERE attendance_date BETWEEN '2024-06-01' AND '2024-07-16'""", as_dict=True)
	for i in att_reg:
		attendance_regularize = i.name
		employee = i.employee
		att_date = i.attendance_date
		frappe.db.sql("""UPDATE `tabAttendance` SET attendance_regularize = '%s' WHERE employee = '%s' AND attendance_date = '%s' """ %(attendance_regularize, employee, att_date))
		