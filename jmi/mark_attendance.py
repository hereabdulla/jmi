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




@frappe.whitelist()

def mark_att():
	# from_date = "2022/11/01"
	# to_date = "2022/11/16"
	to_date = today()
	from_date= get_first_day(today())
	# admin_office_checkins = frappe.db.sql(""" select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' and device_id in ('ADMIN OFFICE','Admin Office out') order by time"""%(from_date,to_date),as_dict = 1)
	checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=True) 
	attendance = frappe.db.sql("""select name,employee,shift,in_time,out_time,attendance_date from `tabAttendance` where docstatus != 2  and attendance_date between '%s' and '%s' """ % (from_date,to_date),as_dict=1)

	if checkins:
		date = checkins[0].time
		from_date = datetime.strftime(date,'%Y-%m-%d')
		
		for c in checkins:
			mark_attendance_from_checkin(c.name,c.employee,c.time,c.device_id)
			# print(c)
	  
def mark_attendance_from_checkin(checkin,employee,time,device):
	att_time = time.time()
	att_date = time.date()
	# print(employee)
	# print(att_date)
	# print(att_time)              
	if device in ['BRM9222360384','BRM9203461488','BRM9193660282','BRM9215260842','BRM9211160652','BRM9222361257']:
		if datetime.strptime('06:30:00','%H:%M:%S').time() < att_time < datetime.strptime('07:00:00','%H:%M:%S').time():
			shift ='1st'
			print('1')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			print(attendance)
			if not attendance:          
				att = frappe.new_doc('Attendance')
				print(att)
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '1st'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

				return att

		# elif device in ['ZONE 1 IN','ZONE 2 IN']:
		elif datetime.strptime('14:30:00','%H:%M:%S').time() < att_time < datetime.strptime('15:00:00','%H:%M:%S').time():
			shift ='2nd'
			print('2')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			print(attendance)
			if not attendance:          
				att = frappe.new_doc('Attendance')
				print(att)
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '2nd'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

		elif datetime.strptime('22:30:00','%H:%M:%S').time() < att_time < datetime.strptime('23:00:00','%H:%M:%S').time():
			shift ='3rd'
			print('3')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			print(attendance)
			if not attendance:          
				att = frappe.new_doc('Attendance')
				print(att)
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '3rd'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

				return att

		elif datetime.strptime('17:30:00','%H:%M:%S').time() < att_time < datetime.strptime('18:00:00','%H:%M:%S').time():
			shift ='5th'
			print('5')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			print(attendance)
			if not attendance:          
				att = frappe.new_doc('Attendance')
				print(att)
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '5th'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

				return att

		elif datetime.strptime('18:30:00','%H:%M:%S').time() < att_time < datetime.strptime('19:00:00','%H:%M:%S').time():
			shift ='5th'
			print('5')
			attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
			print(attendance)
			if not attendance:          
				att = frappe.new_doc('Attendance')
				print(att)
				att.employee = employee
				att.attendance_date = att_date
				att.status = 'Present'
				att.shift = '5th'
				att.in_time = time
				att.total_wh = ''
				att.late_hours = ''
				att.save(ignore_permissions=True)
				frappe.db.commit()
				frappe.db.set_value("Employee Checkin",checkin, "attendance", att.name)
				frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

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
			# max_out = datetime.strptime('16:00:00', '%H:%M:%S').time()
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

def get_total_working_hours():
	# from_date = today()
	# to_date = add_days(from_date,-1)
	from_date = '2022-10-23'
	to_date = '2022-11-19'
	attendance = frappe.db.sql("""select name,employee,status,shift,in_time,out_time,attendance_date from `tabAttendance` where attendance_date between '2022-10-23' and '2022-11-23' """,as_dict=True)	
	for att in attendance:
		if att.in_time and att.out_time:
			str_working_hours = att.out_time - att.in_time
			time_d_float = str_working_hours.total_seconds()
			whrs = time_d_float/3600
			total_working_hours = "{:.2f}".format(whrs)
			print(total_working_hours)			
			frappe.db.set_value('Attendance',att,'total_working_hours',total_working_hours)
				
			if float(total_working_hours) > 8:
				over_time_hours = float(total_working_hours) - 8
				if  float(over_time_hours) < 2:
					over_time = 0
					print(over_time)
					frappe.db.set_value('Attendance',att,'over_time_hours',over_time)

				elif float(over_time_hours) < 2.5:
					ot = over_time_hours - 0.000000000001
					frappe.db.set_value('Attendance',att,'over_time_hours',ot)

				elif float(over_time_hours) >= 2.50:
					over_time_hours = 2.50
					frappe.db.set_value('Attendance',att,'over_time_hours',over_time_hours)

				else:
					return '0'
			
			
			if float(total_working_hours) < 4:
				frappe.set_value('Attendance',att,'status','Absent')
			elif float (total_working_hours) >=4 and float(total_working_hours) < 7.5:
				frappe.set_value('Attendance',att,'status','Half Day')	
			elif float(total_working_hours) >= 7.5:
				frappe.set_value('Attendance',att,'status','Present')
				frappe.set_value('Attendance',att,'leave_type','Loss of Pay')		
			# else:
				# 	att.status = 'Half Day'
				# 	att.leave_type ='Loss of Pay'
				# 	frappe.set_value('Attendance',att,'status',att.status)
				# 	frappe.set_value('Attendance',att,'leave_type',att.leave_type)




				# frappe.db.sql("""update `tabAttendance` set status = 'Absent'""")


def mark_absent_employee():
	to_date = '2022-11-22'
	from_date= '2022-11-22'
	att_date = today()
	yesterday = add_days(att_date,-1)
	employee = frappe.db.sql("""select * from `tabEmployee` where status = 'Active'""",as_dict =1)
	for emp in employee:
		dates = get_dates(from_date,to_date)
		# dates = get_dates(yesterday,att_date)
		for date in dates:
			date = datetime.strptime(date,'%Y-%m-%d')
			day = date.date()
			emp_doj = frappe.get_value('Employee',emp.name,'date_of_joining')
			if day >= emp_doj:
				emp_holiday_list = frappe.get_value('Employee',emp.name,'holiday_list')
				holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
				left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(emp_holiday_list,day),as_dict=True)
				if not holiday:
					att = frappe.db.exists("Attendance",{'employee':emp.name,'attendance_date':day})
					if not att:
						att_doc = frappe.new_doc('Attendance')
						att_doc.employee = emp.name
						att_doc.attendance_date = day
						att_doc.status = 'Absent'
						att_doc.save(ignore_permissions=True)

def get_dates(from_date,to_date):
	no_of_days = date_diff(add_days(to_date, 1), from_date)
	dates = [add_days(from_date, i) for i in range(0, no_of_days)]
	return dates


def create_hooks_mark_ot():
	job = frappe.db.exists('Scheduled Job Type', 'get_total_working_hours')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'hrpro.mark_attendance.get_total_working_hours',
			"frequency": 'Cron',
			"cron_format": '30 10 * * *'
		})
		sjt.save(ignore_permissions=True)



	   
	   
	 


# @frappe.whitelist()
# def del_att():
# 	# att = frappe.db.sql("""delete from `tabAttendace` where attendance_date = '2022-08-0
# 	att = frappe.db.sql(""" update `tabEmployee Checkin` set skip_auto_attendance = 0 where date(time) between  '2022-10-01' and '2022-11-04' """)

# 	print(att)
# 	att = frappe.db.sql(""" update `tabEmployee Checkin` set attendance = '' where date(time) between  '2022-10-01' and '2022-11-04' """)

# 	# # print(att)
# 	att = frappe.db.sql(""" delete from `tabAttendance` where attendance_date between  '2022-10-01' and '2022-11-04'  """)