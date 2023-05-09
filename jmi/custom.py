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
from datetime import datetime,date
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
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
from frappe.utils import get_url_to_form,money_in_words
import math

from datetime import date, timedelta,time
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_url_to_form
import math

@frappe.whitelist()
def ot_hrs(doc,method):
    if doc.contractor != 'UPDATER SERVICES (P) LTD':
        othrs = frappe.db.sql("""select (sum(over_time_hours)) as hrs from `tabAttendance` where employee='%s' and attendance_date between '%s' and '%s' and docstatus !='2' """%(doc.employee,doc.start_date,doc.end_date),as_dict=1)[0]
        ot_time = othrs['hrs']
        frappe.errprint(ot_time)
        frappe.db.set_value('Salary Slip',doc.name,'overtime_hours',ot_time)
    

@frappe.whitelist()
def convert_ot_into_mandays(doc,method):
    if doc.contractor == 'UPDATER SERVICES (P) LTD':
        ot_man_days = frappe.db.sql("""select (sum(over_time_hours) / 8) as ot from `tabAttendance` where employee ='%s' and attendance_date between '%s' and '%s' and docstatus!='2' """%(doc.employee,doc.start_date,doc.end_date),as_dict=1)[0]    
        ot_days = ot_man_days['ot']
        frappe.errprint(ot_days)
        frappe.db.set_value('Salary Slip',doc.name,'overtime_hours',ot_days)
        
    

@frappe.whitelist()
def mark_att(start_date,end_date):
    from_date = start_date
    to_date = end_date
    # to_date = today()
    # from_date= get_first_day(today())
    # admin_office_checkins = frappe.db.sql(""" select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' and device_id in ('ADMIN OFFICE','Admin Office out') order by time"""%(from_date,to_date),as_dict = 1)
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=True) 
    attendance = frappe.db.sql("""select name,employee,shift,in_time,out_time,attendance_date from `tabAttendance` where docstatus != 2  and attendance_date between '%s' and '%s' """ % (from_date,to_date),as_dict=1)

    if checkins:
        date = checkins[0].time
        from_date = datetime.strftime(date,'%Y-%m-%d')
        
        for c in checkins:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.device_id)
            # print(c)
    get_total_working_hours(from_date,to_date)
    mark_absent_employee(from_date,to_date)
    return 'ok'
      
def mark_attendance_from_checkin(checkin,employee,time,device):
    att_time = time.time()
    att_date = time.date()
    # print(employee)
    # print(att_date)
    # print(att_time)              
    if device in ['BRM9222360384','BRM9203461488','BRM9193660282','BRM9215260842','BRM9211160652','BRM9222361257']:
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
        if datetime.strptime('08:00:00','%H:%M:%S').time() < att_time < datetime.strptime('10:00:00','%H:%M:%S').time():
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
        # elif device in ['ZONE 1 IN','ZONE 2 IN']:
        if datetime.strptime('14:00:00','%H:%M:%S').time() < att_time < datetime.strptime('15:30:00','%H:%M:%S').time():
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

def get_total_working_hours():
    # to_date = today()
    # from_date= get_first_day(today())
    # from_date = today()
    # to_date = add_days(from_date,-1)
    # from_date = '2023-01-15'
    # to_date = '2023-02-23'
    attendance = frappe.db.sql("""select name,employee,status,shift,in_time,out_time,attendance_date,branch from `tabAttendance` where attendance_date between '%s' and '%s' """%(from_date,to_date),as_dict=True)	
    for att in attendance:
        if att.in_time and att.out_time:
            str_working_hours = att.out_time - att.in_time
            time_d_float = str_working_hours.total_seconds()
            whrs = time_d_float/3600
            total_working_hours = "{:.2f}".format(whrs)
            print(total_working_hours)			
            frappe.db.set_value('Attendance',att.name,'total_working_hours',total_working_hours)
                
            if float(total_working_hours) > 8:
                if att.branch == 'JMI Plant 1':
                    over_time_hours = float(total_working_hours) - 8
                    if  float(over_time_hours) < 2:
                        over_time = 0
                        print(over_time)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time)

                    elif float(over_time_hours) < 2.5:
                        ot = over_time_hours - 0.00000000000001
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',ot)

                    elif float(over_time_hours) >= 2.50:
                        over_time_hours = 2.50
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours)

                elif att.branch == 'JMI Plant 2' or 'JMI Plant 3' or 'Seyoon' or 'VEL 1' or 'VEL 2':
                    over_time_hours = float(total_working_hours) - 8
                    if  float(over_time_hours) < 3:
                        over_time = 0
                        print(over_time)
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time)

                    elif float(over_time_hours) < 3.5:
                        ot = over_time_hours - 0.00000000000001
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',ot)

                    elif float(over_time_hours) >= 3.50:
                        over_time_hours = 3.50
                        frappe.db.set_value('Attendance',att.name,'over_time_hours',over_time_hours)
            
            if float(total_working_hours) < 4:
                print('hi')
                frappe.set_value('Attendance',att.name,'status','Absent')
            elif float (total_working_hours) >=4 and float(total_working_hours) < 7.5:
                print('hii')
                frappe.set_value('Attendance',att.name,'status','Half Day')
                frappe.set_value('Attendance',att.name,'leave_type','Loss of Pay')	
            elif float(total_working_hours) >= 7.5:
                print('hiii')
                frappe.set_value('Attendance',att.name,'status','Present')
                       
            # else:
                # 	att.status = 'Half Day'
                # 	att.leave_type ='Loss of Pay'
                # 	frappe.set_value('Attendance',att,'status',att.status)
                # 	frappe.set_value('Attendance',att,'leave_type',att.leave_type)




                # frappe.db.sql("""update `tabAttendance` set status = 'Absent'""")


def mark_absent_employee():
    # to_date = '2023-02-23'
    # from_date= '2023-01-15'
    # to_date = today()
    # from_date= get_first_day(today())
    # att_date = today()
    # yesterday = add_days(att_date,-1)
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

@frappe.whitelist()
def mark_employee_checkin(start_date,end_date):

    serial_number_list=["BRM9222360384","BRM9222360383","BRM9203461488","BRM9222360378","BRM9193660282","BRM9222360385","BRM9211160652","BRM9222361360","BRM9222361258","BRM9215260842","BRM9222361257","BRM9222360379"]
    s_date = start_date
    e_date = end_date
    to_date = e_date
    # from_date= date.today()
    from_date = s_date
    # to_date = '2022-12-23'

    for serial in serial_number_list:
        url = "http://192.168.1.189:8080/iclock/webapiservice.asmx?op=GetTransactionsLog"
        payload = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n  <soap:Body>\n    <GetTransactionsLog xmlns=\"http://tempuri.org/\">\n      <FromDate>%s </FromDate>\n      <ToDate>%s </ToDate>\n      <SerialNumber>%s</SerialNumber>\n      <UserName>tss</UserName>\n      <UserPassword>Tss@12345</UserPassword>\n    </GetTransactionsLog>\n  </soap:Body>\n</soap:Envelope>" % (from_date,to_date,serial)

        ET.headers = {
        'Content-Type': 'text/xml'
        }

        response = requests.request("POST", url, headers=ET.headers, data=payload)

        root=ET.fromstring(response.text)

        my_dict = xmltodict.parse(response.text)
        # print(my_dict)
        attlog = my_dict['soap:Envelope']['soap:Body']['GetTransactionsLogResponse']['strDataList']
        mylist = attlog.split('\n')
        frappe.log_error(title='at',message=mylist)
        for mydict in mylist:
            mytlist = mydict.split('\t')
            emp_id = mytlist[0]
            date_time = mytlist[1]
            log_type = mytlist[2]
            urls = "http://localhost:8001/api/method/jmi.biometric_checkin.mark_checkin?employee=%s&time=%s&device_id=%s&log_type=%s" % (emp_id,date_time,serial,log_type)
            headers = { 'Content-Type': 'application/json','Authorization': 'token 2d42d97bd67d671: 8bb6689649df56c'}
            responses = requests.request('GET',urls,headers=headers,verify=False)
            print(responses.text)
            # res = json.loads(responses.text)
            # print(urls)
            return 'ok'

@frappe.whitelist()
def get_total_over_time(contractor,branch,start_date,end_date):
    if contractor == 'UPDATER SERVICES (P) LTD':
        ot = frappe.db.sql("""select ((sum(over_time_hours))/8)  as ot_hrs from `tabAttendance` where contractor ='%s' and branch ='%s' and attendance_date between '%s' and '%s' """%(contractor,branch,start_date,end_date),as_dict=1)[0]
        return ot['ot_hrs']
    else:
        ot = frappe.db.sql("""select (sum(overtime_hours))  as ot_hrs from `tabSalary Slip` where contractor ='%s' and branch ='%s' and start_date = '%s' and end_date = '%s' """%(contractor,branch,start_date,end_date),as_dict=1)[0]
        frappe.errprint(ot['ot_hrs'])
        return ot['ot_hrs']
    

    
        
@frappe.whitelist()
def get_mandays(contractor,branch,start_date,end_date):
    
    man_days = frappe.db.sql("""select sum(payment_days) from `tabSalary Slip` where docstatus != '2' and contractor ='%s' and branch = '%s' and start_date = '%s' and end_date = '%s' """%(contractor,branch,start_date,end_date),as_dict = 1)[0]
    frappe.errprint(man_days['sum(payment_days)'])
    return man_days['sum(payment_days)'] or '0'

@frappe.whitelist()
def get_mandays_amount(contractor,branch):
    man_days_amount = frappe.db.sql("""select sum(rounded_total) from `tabSalary Slip` where docstatus ='0' and contractor='%s' and branch = '%s' """%(contractor,branch),as_dict = 1)[0]
    return[man_days_amount['sum(rounded_total)']]

@frappe.whitelist()
def get_total_amount_in_words(total_amount):
    tot = money_in_words(total_amount)
    return tot

# @frappe.whitelist()
# def get_rate(contractor):
#     rate = frappe.db.sql("""select `tabContractor Wages`.designation as designation,`tabContractor Wages`.basic as basic,
#     `tabContractor Wages`.dearness_allowance as dearness_allowance,
#     `tabContractor Wages`.hra as hra from `tabContractor` left join `tabContractor Wages` on `tabContractor`.name = `tabContractor Wages`.parent """)

# @frappe.whitelist()
# def custom():
#     shift = frappe.db.sql("""update `tabShift Type` set name = '4' where name = '5' """)
#     print(shift)

# @frappe.whitelist()
# def get_total_time(): 
#     ot = frappe.db.sql("""select sum(over_time_hours) from `tabAttendance` where contractor ='Adhavan Enterprises' and branch ='JMI Plant 1' and attendance_date between '26-11-2022' and '25-12-2022' """)
#     print(ot)


def mark_employee_checkin_manual():

    serial_number_list=["BRM9222360384","BRM9222360383","BRM9203461488","BRM9222360378","BRM9193660282","BRM9222360385","BRM9211160652","BRM9222361360","BRM9222361258","BRM9215260842","BRM9222361257","BRM9222360379"]

    # to_date = date.today()
    from_date= "2023-04-22"
    # from_date =add_days(to_date,-1)
    to_date = '2023-05-01'

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


# @frappe.whitelist()
# def delete_bulk_attendance():
#     emp_list = [ "UD391",
#         "UD403",
#         "UP002",
#         "UP013",
#         "UP014",
#         "UP087",
#         "UP088",
#         "UP103",
#         "UP107",
#         "UP143",
#         "UP149",
#         "UP353",
#         "UP402",
#         "AD232",
#         "AD377",
#         "AD380",
#         "P1AD395",
#         "P1AD396",
#         "P1AD397",
#         "P1AD400",
#         "AD133",
#         "AD159",
#         "AD196",
#         "AD212",
#         "AD233",
#         "AD236",
#         "AD238",
#         "AD268",
#         "AD348",
#         "AD351",
#         "AD362",
#         "AD363",
#         "AD364",
#         "AD365",
#         "AD366",
#         "AD367",
#         "AD371",
#         "AD372",
#         "AD373",
#         "AD375",
#         "AD376",
#         "AD378",
#         "AD379",
#         "AD381",
#         "AD382",
#         "P1AD398",
#         "P1AD399"
#         ]
#     for e in emp_list:
#         print(e)
#         test = frappe.db.sql("""delete from `tabAttendance` where employee = '%s' and attendance_date between '2023-03-21' and '2023-04-28' """%(e))
