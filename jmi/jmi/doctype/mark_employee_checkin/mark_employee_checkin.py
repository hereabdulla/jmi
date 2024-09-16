# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
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
# from frappe.utils.background_jobs import enqueue
# from frappe.utils import get_url_to_form
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
from frappe.model.document import Document
from jmi.custom import get_dates, mark_attendance_from_checkin, get_total_working_hours_jmi_plant_1_new, get_total_working_hours_except_jmi_plant_1_new, get_total_working_hours_vcp_vcr, mark_absent_employee_new

class MarkEmployeeCheckin(Document):

	def mark_att(self,from_date, to_date):
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
		
	# JMI PLANT 1       
		if device in ['BRM9222360384']:
			if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
				shift ='1'
				print('1')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
				shift ='G'
				print('G')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
				shift ='2'
				print('2')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

			elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
				shift ='3'
				print('3')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att

			elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
				shift ='4'
				print('4')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 
					return att

	# JMI PLANT 2 IN
		elif device in ['BRM9203461488']:
			if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
				shift ='1'
				print('1')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
				shift ='G'
				print('G')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
				shift ='2'
				print('2')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

			elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
				shift ='3'
				print('3')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att

			elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
				shift ='4'
				print('4')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 
					return att
	# JMI PLANT 3 IN
		elif device in ['BRM9193660282']:
			if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
				shift ='1'
				print('1')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
				shift ='G'
				print('G')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
				shift ='2'
				print('2')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

			elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
				shift ='3'
				print('3')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att

			elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
				shift ='4'
				print('4')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 
					return att
	# SEYON PLANT 1N
		elif device in ['BRM9211160652']:
			if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('08:00:00','%H:%M:%S').time():
				shift ='1'
				print('1')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
				shift ='G'
				print('G')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('10:30:00','%H:%M:%S').time() < att_time < datetime.strptime('11:30:00','%H:%M:%S').time():
				shift ='5'
				print('5')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
				shift ='2'
				print('2')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

			elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
				shift ='3'
				print('3')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att

			elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
				shift ='4'
				print('4')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 
					return att
	# VCR PLANT IN
		elif device in ['BRM9215260842']:
			if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
				shift ='1'
				print('1')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
				shift ='G'
				print('G')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 
					return att
			elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
				shift ='2'
				print('2')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

			elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
				shift ='3'
				print('3')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 
					return att

			elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
				shift ='4'
				print('4')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 
					return att
	# VCP PLANT IN
		elif device in ['BRM9222361257']:
			if datetime.strptime('06:00:00','%H:%M:%S').time() < att_time < datetime.strptime('07:30:00','%H:%M:%S').time():
				shift ='1'
				print('1')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
				shift ='G'
				print('G')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att
			elif datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
				shift ='2'
				print('2')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

			elif datetime.strptime('21:00:00','%H:%M:%S').time() < att_time < datetime.strptime('23:30:00','%H:%M:%S').time():
				shift ='3'
				print('3')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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
					frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1') 

					return att

			elif datetime.strptime('17:00:00','%H:%M:%S').time() < att_time < datetime.strptime('20:00:00','%H:%M:%S').time():
				shift ='4'
				print('4')
				attendance = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=','2')})        
				print(attendance)
				if not attendance:          
					att = frappe.new_doc('Attendance')
					print(att)
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


@frappe.whitelist()
def mark_employee_checkin_frontend(from_date, to_date, with_biometric,plant, device_type):
	frappe.enqueue(
		mark_employee_checkin_frontend_queue, # python function or a module path as string
		queue="long", # one of short, default, long
		timeout=36000, # pass timeout manually
		is_async=True, # if this is True, method is run in worker
		now=True, # if this is True, method is run directly (not in a worker) 
		job_name='Checkin Upload', # specify a job name
		# enqueue_after_commit=False, # enqueue the job after the database commit is done at the end of the request
		from_date = from_date , # kwargs are passed to the method as arguments
		to_date = to_date,
		with_biometric = with_biometric,
		plant=plant,
		device_type=device_type

	)

@frappe.whitelist()
def mark_employee_checkin_frontend_queue(from_date, to_date, with_biometric, plant, device_type):
	device = frappe.db.get_all("Device Details",['*'])
	if device:
		for s in device:
			if s.branch ==plant and s.log_type == device_type:
				
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
def mark_employee_checkin_frontend_without_device_id(from_date, to_date, plant):
	frappe.enqueue(
		mark_employee_checkin_frontend_queue_without_device_id, # python function or a module path as string
		queue="long", # one of short, default, long
		timeout=36000, # pass timeout manually
		is_async=True, # if this is True, method is run in worker
		now=False, # if this is True, method is run directly (not in a worker) 
		job_name='Checkin Upload', # specify a job name
		enqueue_after_commit=False, # enqueue the job after the database commit is done at the end of the request
		from_date = from_date , # kwargs are passed to the method as arguments
		to_date = to_date,
		plant =plant
	)  

@frappe.whitelist()
def mark_employee_checkin_frontend_queue_without_device_id(from_date, to_date, plant):
	device = frappe.db.get_all("Device Details",['*'])
	if device:
		for s in device:
			if s.branch ==plant:
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
						print(emp_id)
			else:
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
						print(emp_id)

frappe.whitelist()
def att_background_frontend_queue(from_date, to_date, plant):
	frappe.enqueue(
		att_background_frontend, # python function or a module path as string
		queue="long", # one of short, default, long
		timeout=36000, # pass timeout manually
		is_async=True, # if this is True, method is run in worker
		now=True, # if this is True, method is run directly (not in a worker) 
		job_name='Attendance Upload', # specify a job name
		# enqueue_after_commit=False, # enqueue the job after the database commit is done at the end of the request
		from_date = from_date , # kwargs are passed to the method as arguments
		to_date = to_date,
		plant=plant
	)  

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
