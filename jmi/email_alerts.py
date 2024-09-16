import frappe
from frappe.utils.data import add_days, today
from frappe.utils import  formatdate
from frappe.utils import format_datetime


@frappe.whitelist()    
def daily_att_report():
    branch=frappe.db.get_all("Branch",['*'])
    for b in branch:
        daily_att= frappe.db.sql("""
        select * from `tabAttendance` where attendance_date = DATE_SUB(CURDATE(), INTERVAL 1 DAY) and branch=%s""",(b.name), as_dict=1)
        attendance = ''
        attendance += '<table class = table table - bordered style=border-width:2px><tr><td colspan = 7><b>Daily Attendance Report - %s</b></td></tr>'%(b.branch)
        attendance += '<tr><td>Employee</td><td>Employee Name</td><td>Contractor</td><td>Shift</td><td>Status</td><td>IN Time</td><td>OUT Time'
        for att in daily_att:
            attendance += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(att.employee,att.employee_name,att.contractor or '',att.shift or '',att.status or '',format_datetime(att.in_time) or '',format_datetime(att.out_time) or '') 
        attendance += '</table>' 
        frappe.sendmail(
            recipients=[b.plant_hr,b.hr_manager],
            # recipients=['giftyannie6@gmail.com'],
                cc = [''],
                subject=('Daily Attendance Report - '+frappe.utils.today()+" - "+b.branch),
                message="""
                        Dear Sir/Mam,<br>
                        <p>Kindly find the attached Daily Attendance Report</p>
                        %s
                        """ % (attendance)
            ) 
    return True
    
from datetime import datetime
@frappe.whitelist()    
def att_reg():
    branch=frappe.db.get_all("Branch",['*'])
    for b in branch:  
        current_date = datetime.now()
        if current_date.day >= 21:
            if current_date.month == 1:
                start_date = datetime(current_date.year - 1, 12, 21)
            else:
                start_date = datetime(current_date.year, current_date.month - 1, 21)
        else:
            if current_date.month == 1:
                start_date = datetime(current_date.year - 1, 11, 21)
            else:
                start_date = datetime(current_date.year, current_date.month - 2, 21)
        end_date = datetime(current_date.year, current_date.month,current_date.day)
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        print(start_date_str)
        print(end_date_str)
        daily_att = frappe.db.sql("""
            SELECT * FROM `tabAttendance Regularize`
            WHERE attendance_date BETWEEN %s AND %s AND branch=%s AND workflow_state!="Draft" AND workflow_state!="Approved" AND workflow_state!="Rejected"
        """, (start_date_str, end_date_str, b.name), as_dict=True)        
        attendance = ''
        attendance += '<table class = table table - bordered style=border-width:2px><tr><td colspan = 7><b>Attendance Regularize Report-Waiting for Approval - %s</b></td></tr>'%(b.branch)
        attendance += '<tr><td>Employee</td><td>Branch</td><td>Contractor</td><td>Designation</td><td>Attendance Date</td></tr>'
        for att in daily_att:
            attendance += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(att.employee,att.branch,att.contractor or '',att.designation or '',att.attendance_date or '') 
        attendance += '</table>'  
        frappe.sendmail(
            
            recipients=[b.plant_hr,'admin@jmil.in'],
            # recipients=['giftyannie6@gmail.com'],
                cc = [''],
                subject=('Attendance Regularize'+" - "+b.branch),
                message="""
                        Dear Sir/Mam,<br>
                        <p>Kindly find the attached Attendance Regularize Report - Waiting for your approval</p>
                        %s
                        """ % (attendance)
            )
        
    return True