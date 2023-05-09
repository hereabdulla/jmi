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
# import frappe
# from numpy import empty
# import pandas as pd
import json
import datetime
# from frappe.permissions import check_admin_or_system_manager
# from frappe.utils.csvutils import read_csv_content
# from six.moves import range
# from six import string_types
# from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
# 	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime,date
from calendar import monthrange
# from frappe import _, msgprint
# from frappe.utils import flt
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




@frappe.whitelist()

def mark_att():
    # from_date = "2023/03/20"
    # to_date = "2023/04/21"
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



def get_total_working_hours_jmi_plant_1():
    to_date = today()
    from_date= get_first_day(today())
    # from_date = today()
    # to_date = add_days(from_date,-1)
    # from_date = '2023-03-21'
    # to_date = '2023-05-03'
    attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
    for att in attendance:
        if att.branch == 'JMI Plant 1' and att.docstatus == 0:
            if att.in_time and att.out_time:
                str_working_hours = att.out_time - att.in_time
                time_d_float = str_working_hours.total_seconds()
                whrs = time_d_float/3600
                total_working_hours = "{:.2f}".format(whrs)
                print(total_working_hours)			
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
                        print(over_time)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time)
                elif float(total_working_hours) < 4:
                    print('hi')
                    frappe.set_value('Attendance',att.name,'status','Absent')
                elif float (total_working_hours) >=4 and float(total_working_hours) < 7.5:
                    print('hii')
                    frappe.set_value('Attendance',att.name,'status','Half Day')
                    frappe.set_value('Attendance',att.name,'leave_type','Loss of Pay')	
                elif float(total_working_hours) >= 7.5:
                    print('hiii')
                    frappe.set_value('Attendance',att.name,'status','Present')
            if not (att.in_time and att.out_time):
                print('jii')
                frappe.set_value('Attendance',att.name,'status','Absent')

def get_total_working_hours_except_jmi_plant_1():
    to_date = today()
    from_date= get_first_day(today())
    # # from_date = today()
    # to_date = add_days(from_date,-1)
    # from_date = '2023-03-20'
    # to_date = '2023-05-03'
    attendance = frappe.db.sql("""select docstatus,name,employee,status,shift,in_time,out_time,attendance_date,branch,designation from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
    for att in attendance:
        if att.branch != 'JMI Plant 1' and att.docstatus == 0:
            if att.in_time and att.out_time:
                str_working_hours = att.out_time - att.in_time
                time_d_float = str_working_hours.total_seconds()
                whrs = time_d_float/3600
                total_working_hours = "{:.2f}".format(whrs)
                print(total_working_hours)			
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
                    elif  float(over_time_hours) < 2:
                        over_time = 0
                        print(over_time)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time)
                elif float(total_working_hours) < 4:
                    print('hi')
                    frappe.set_value('Attendance',att.name,'status','Absent')
                elif float (total_working_hours) >=4 and float(total_working_hours) < 7.5:
                    print('hii')
                    frappe.set_value('Attendance',att.name,'status','Half Day')
                    frappe.set_value('Attendance',att.name,'leave_type','Loss of Pay')	
                elif float(total_working_hours) >= 7.5:
                    print('hiii')
                    frappe.set_value('Attendance',att.name,'status','Present')
            if not (att.in_time and att.out_time):
                print('jii')
                frappe.set_value('Attendance',att.name,'status','Absent')
                

                


def mark_absent_employee():
    # to_date = '2023-04-21'
    # from_date= '2023-03-20'
    # to_date = today()
    # from_date= get_first_day(today())
    att_date = today()
    yesterday = add_days(att_date,-1)
    employee = frappe.db.sql("""select * from `tabEmployee` where status = 'Active'""",as_dict =1)
    for emp in employee:
        # dates = get_dates(from_date,to_date)
        dates = get_dates(yesterday,att_date)
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


def mark_employee_checkin():

    serial_number_list=["BRM9222360384","BRM9222360383","BRM9203461488","BRM9222360378","BRM9193660282","BRM9222360385","BRM9211160652","BRM9222361360","BRM9222361258","BRM9215260842","BRM9222361257","BRM9222360379"]

    to_date = date.today()
    # from_date= "2023-03-21"
    from_date =add_days(to_date,-1)
    # to_date = '2023-03-27'

    for serial in serial_number_list:
        url = "http://192.168.1.189:8080/iclock/webapiservice.asmx?op=GetTransactionsLog"
        payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetTransactionsLog xmlns=\"http://tempuri.org/\">\n      <FromDate>%s</FromDate>\n      <ToDate>%s</ToDate>\n      <SerialNumber>%s</SerialNumber>\n      <UserName>tss</UserName>\n      <UserPassword>Tss@12345</UserPassword>\n      <strDataList></strDataList>\n    </GetTransactionsLog>\n  </soap:Body>\n</soap:Envelope>" % (from_date,to_date,serial)

        ET.headers = {
        'Content-Type': 'text/xml'
        }

        response = requests.request("POST", url, headers=ET.headers, data=payload)

        root=ET.fromstring(response.text)

        my_dict = xmltodict.parse(response.text)
        # print(my_dict)
        attlog = my_dict['soap:Envelope']['soap:Body']['GetTransactionsLogResponse']['strDataList']
        if attlog:
            mylist = attlog.split('\n')
            frappe.log_error(title='at',message=mylist)
            for mydict in mylist:
                mytlist = mydict.split('\t')
                emp_id = mytlist[0]
                date_time = mytlist[1]
                log_type = mytlist[2]
                urls = "http://192.168.1.188/api/method/jmi.biometric_checkin.mark_checkin?employee=%s&time=%s&device_id=%s&log_type=%s" % (emp_id,date_time,serial,log_type)
                headers = { 'Content-Type': 'application/json','Authorization': 'token 2d42d97bd67d671: 8bb6689649df56c'}
                responses = requests.request('GET',urls,headers=headers,verify=False)
                print(responses.text)
                # res = json.loads(responses.text)
                # print(urls)






def create_hooks_mark_ot():
    job = frappe.db.exists('Scheduled Job Type', 'mark_employee_checkin')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'jmi.mark_attendance.mark_employee_checkin',
            "frequency": 'Cron',
            "cron_format": '*/10 * * * *'
        })
        sjt.save(ignore_permissions=True)



       
       
     


# @frappe.whitelist()
# def del_att():
# # # # # # # # # # # #     # att = frappe.db.sql("""delete from `tabAttendace` where attendance_date = '2022-08-0
# # # # # # # # #     att = frappe.db.sql(""" update `tabEmployee Checkin` set skip_auto_attendance = 0 where date(time) between  '2023-01-15' and '2023-02-23' """)
#     att = frappe.db.sql(""" update `tabAttendance` set docstatus = 0 where branch = 'JMI Plant 3'  and attendance_date between '2023-03-20' and '2023-04-21' """)

# # # # # # # # # # #     # print(att)
    # att = frappe.db.sql(""" delete from `tabAttendance` where attendance_date between '2023-03-21' and '2023-05-03' and docstatus = '0' """)
#     att = frappe.db.sql("""update `tabWorkspace` set public = '0' where name ='Home'  """)
# # #     # print(att)
# # #     # att = frappe.db.sql(""" select sum(over_time_hours) from `tabAttendance` where contractor ='UPDATER SERVICES (P) LTD' and attendance_date between '2022-12-26' and '2023-01-20'  """)
# #     emp = frappe.db.sql("""select name from `tabEmployee` where status = 'Left' and branch ='JMI Plant 1' """,as_dict=1)
# #     for e in emp:
    # emp = frappe.db.sql("""select name from `tabEmployee` where status = 'Active'  """,as_dict=1)
   
    # for e in emp:
    #     print(e.name)
    # att = frappe.db.sql(""" update `tabEmployee` set date_of_joining = '2023-03-20' where status = 'Active' """)
# att = frappe.db.sql(""" delete from `tabEmployee` where name ='V2OG090'  """)
#     # att = frappe.db.sql(""" select count(status) from `tabAttendance` where status = 'Present' and branch ='JMI Plant 1' and contractor ='UPDATER SERVICES (P) LTD' and attendance_date between '2022-12-26' and '2023-01-20'  """)
    
        # print(e.name)
    # att = frappe.db.sql(""" update `tabSalary Slip` set docstatus =1  """)
