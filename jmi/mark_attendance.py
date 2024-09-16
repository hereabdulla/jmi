from os import name
from collections import namedtuple
import frappe
import xml.etree.ElementTree as ET
from cgi import print_environ
import requests,json
from datetime import date
from datetime import time,datetime
import xmltodict
from collections import namedtuple
from frappe.utils.data import ceil, get_time, get_year_start
from datetime import datetime,date
from calendar import monthrange
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
from numpy import empty
import pandas as pd
from frappe.permissions import check_admin_or_system_manager
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_url_to_form
import math

@frappe.whitelist()
def mark_attendance_new(from_date,to_date):
		# from_date = "2023-11-02"
		# to_date = "2023-11-04"
		checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=True) 
		if checkins:
			date = checkins[0].time
			from_date = datetime.strftime(date,'%Y-%m-%d')
			for c in checkins:
				print(c.name)
				if frappe.db.exists("Employee",{'name':c.employee,'status':"Active"}):
					print("HI")
					att = mark_attendance_from_checkin(c.name,c.employee,c.time,c.device_id)
					if att:
						frappe.db.set_value("Employee Checkin",c.name, "skip_auto_attendance", "1")
		get_total_working_hours_jmi_plant_1_new(from_date,to_date)
		get_total_working_hours_except_jmi_plant_1_new(from_date , to_date)
		get_total_working_hours_vcp_vcr(from_date ,to_date)
		mark_absent_employee_new(from_date, to_date)
		# return "OK"

def get_total_working_hours_jmi_plant_1_new(from_date , to_date):
	# print("HI")
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
	# print("HI")
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
	# print("HI")
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
	# print("HI")
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
			
def mark_attendance_from_checkin(checkin,employee,time,device):
	att_time = time.time()
	att_date = time.date()
	shift = ''
	# All
	if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('06:00:00','%H:%M:%S').time():
		shift = '1'
		print(shift)

	# All
	elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
		shift = '2'
		print(shift)

	# All
	elif datetime.strptime('22:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
		shift ='3'
		print(shift)

	# All
	elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
		shift ='G'
		print(shift)

	# All except P1
	if device in ['BRM9203461488','BRM9193660282','BRM9211160652','BRM9215260842','BRM9222361257']:
		if datetime.strptime('18:00:00','%H:%M:%S').time() < att_time < datetime.strptime('19:30:00','%H:%M:%S').time():
			shift = '5'
			print(shift)
	# P1
	elif device in ['BRM9222360384']:
		if datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('18:00:00','%H:%M:%S').time():
			shift = '5 - P1'
			print(shift)

	# Seyoon
	elif device in ['BRM9211160652']:
		if datetime.strptime('10:00:00','%H:%M:%S').time() < att_time < datetime.strptime('11:30:00','%H:%M:%S').time():
			shift = '6 - S'
			print(shift)

	# VCR/VCR
	elif device in ['BRM9215260842','BRM9222361257']:
		if datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('18:00:00','%H:%M:%S').time():
			shift = '6 - V'
			print(shift)
	
	attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
	if not attendance:          
		att = frappe.new_doc('Attendance')
		att.employee = employee
		att.attendance_date = att_date
		att.status = "Absent"
		att.shift = shift
		att.in_time = time
		att.total_wh = ''
		att.late_hours = ''
		att.save(ignore_permissions=True)
		frappe.db.commit()
		frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
		return att	
	
	if device in ['BRM9222360383','BRM9222360378','BRM9222360385','BRM9222361258','BRM9222361360','BRM9232260887']:
		max_out = datetime.strptime('10:00:00', '%H:%M:%S').time()
		if att_time < max_out:
			yesterday = add_days(att_date,-1)
			checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee = '%s' and device_id in ('BRM9222360383','BRM9222360378','BRM9222360385','BRM9222361258','BRM9222361360','BRM9232260887') and date(time) = '%s' and time(time) < '%s' order by time "%(employee,att_date,max_out),as_dict=True)            
			att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':yesterday})
			if att:
				att = frappe.get_doc("Attendance",att)
				if att.docstatus == 0:
					if not att.out_time:
						if len(checkins) > 0:
							att.shift = get_actual_shift(get_time(checkins[-1].time))
							att.out_time = checkins[-1].time
							frappe.db.set_value("Employee Checkin",checkins[-1].name, "attendance", att.name)
						else:
							att.shift = get_actual_shift(get_time(checkins[-1].time))
							att.out_time = checkins[0].time
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
				if len(checkins) > 0:
					att.shift = get_actual_shift(get_time(checkins[-1].time))
					att.out_time = checkins[-1].time
					frappe.db.set_value("Employee Checkin",checkins[-1].name, "attendance", att.name)
				else:
					att.shift = get_actual_shift(get_time(checkins[-1].time))
					att.out_time = checkins[0].time
					frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
				att.save(ignore_permissions=True)
				frappe.db.commit()
				return att
		else:
			checkins = frappe.db.sql("select name,time from `tabEmployee Checkin` where employee ='%s' and device_id in ('BRM9222360383','BRM9222360378','BRM9222360385','BRM9222361258','BRM9222361360','BRM9232260887') and date(time) = '%s' order by time "%(employee,att_date),as_dict=True)
			att = frappe.db.exists("Attendance",{'employee':employee,'attendance_date':att_date})
			if att:
				att = frappe.get_doc("Attendance",att)
				if att.docstatus == 0:
					if not att.out_time:
						if len(checkins) > 0:
							att.shift = get_actual_shift(get_time(checkins[-1].time))
							att.out_time = checkins[-1].time
							frappe.db.set_value("Employee Checkin",checkins[-1].name, "attendance", att.name)
						else:
							att.shift = get_actual_shift(get_time(checkins[-1].time))
							att.out_time = checkins[0].time
							frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
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
					att.shift = get_actual_shift(get_time(checkins[-1].time))
					att.out_time = checkins[-1].time
					frappe.db.set_value("Employee Checkin",checkins[-1].name, "attendance", att.name)
				else:
					att.shift = get_actual_shift(get_time(checkins[-1].time))
					att.out_time = checkins[0].time
					frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name)
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkins[0].name, "attendance", att.name) 
				return att

def is_between(time, time_range):
	if time_range[1] < time_range[0]:
		return time >= time_range[0] or time <= time_range[1]
	return time_range[0] <= time <= time_range[1]

def get_actual_shift(get_shift_time):
	from datetime import datetime
	from datetime import date, timedelta,time
	shift_1_time = [time(hour=11, minute=0, second=0),time(hour=17, minute=0, second=0)]
	shift_2_time = [time(hour=20, minute=0, second=0),time(hour=23, minute=59, second=59)]
	shift_3_time = [time(hour=5, minute=00, second=0),time(hour=10, minute=0, second=0)]
	shift_g_time = [time(hour=17, minute=0, second=1),time(hour=20, minute=0, second=0)]
	shift = ''
	if is_between(get_shift_time,shift_1_time):
		shift = '1'
	if is_between(get_shift_time,shift_2_time):
		shift = '2'
	if is_between(get_shift_time,shift_3_time):
		shift = '3'
	if is_between(get_shift_time,shift_g_time):
		shift = 'G'
	return shift   

@frappe.whitelist()
def mark_employee_checkin():
	serial_number_list=["BRM9222360384","BRM9222360383","BRM9203461488","BRM9222360378","BRM9193660282","BRM9222360385","BRM9211160652","BRM9222361360","BRM9222361258","BRM9215260842","BRM9222361257","BRM9222360379"]
	from_date= "2023-11-17"
	to_date = '2023-11-18'
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
			mylist = attlog.split('\n')
			# frappe.log_error(title=serial,message=mylist)
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

# def get_api_log():
# 	serial_number_list=["BRM9222360384","BRM9222360383","BRM9203461488","BRM9222360378","BRM9193660282","BRM9222360385","BRM9211160652","BRM9222361360","BRM9222361258","BRM9215260842","BRM9222361257","BRM9232260887"]
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
def update_checkin_att():
	checkin = frappe.db.sql("""update `tabEmployee Checkin` set attendance = '' where date(time) between "2023-10-21" and "2023-11-08" """,as_dict = True)
	print(checkin)
	checkin = frappe.db.sql("""update `tabEmployee Checkin` set skip_auto_attendance = 0 where date(time) between "2023-10-21" and "2023-11-08" """,as_dict = True)
	print(checkin)
	checkin = frappe.db.sql("""delete from `tabAttendance` where attendance_date between "2023-10-21" and "2023-11-08" """,as_dict = True)
	print(checkin)
	# checkin = frappe.db.sql("""delete from `tabUnregistered Employee Checkin` """,as_dict = True)
	# print(checkin)

@frappe.whitelist()
def mark_attendance_new_ec():
	from_date = "2024-03-21"
	to_date = "2024-04-20"
	mark_attendance_new(from_date,to_date)