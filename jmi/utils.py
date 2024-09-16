import frappe
from frappe.model.naming import parse_naming_series
import re
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,format_date,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)

@frappe.whitelist()
def set_naming(branch,contractor,contractor_short_code,branch_short_code):
    if frappe.db.exists("Employee",{'branch':branch,'contractor':contractor}):
        query = frappe.db.sql("""select name  from `tabEmployee` WHERE branch = '%s' and contractor = '%s' order by name DESC """%(branch,contractor),as_dict = 1)[0]
        input_string = query['name']
        match = re.search(r'(\d+)$', input_string)
        if match:
            number = match.group(1)
            leng = int(number) + 1
            str_len = str(leng)
            lengt = len(str_len)
            ty = str(lengt)
            if ty == "3":
                code = str(branch_short_code) + str(contractor_short_code) + "0" + str(leng)
            elif ty == "2":
                code = str(branch_short_code) + str(contractor_short_code) + "00" + str(leng)
            elif ty == "1":
                code = str(branch_short_code) + str(contractor_short_code) + "000" + str(leng)
            else:
                code = str(branch_short_code) + str(contractor_short_code) + str(leng) 
    else:
        code = str(branch_short_code) + str(contractor_short_code) + "0001"
    return code

@frappe.whitelist()
def validate_att_relieving_date(doc,method):
    if doc.relieving_date:
        if frappe.db.exists("Attendance",{'employee':doc.name,'attendance_date':add_days(doc.relieving_date,1),'docstatus':1}):
            frappe.throw('Attendance has been already marked for the next day. Kindly check the Relieving Date')

@frappe.whitelist()
def validate_relieving_day_att(doc,method):
    if frappe.db.exists("Employee",{'name':doc.employee,'relieving_date':add_days(doc.attendance_date,-1)}):
        frappe.throw('Employee has been already marked left on Yesterday.')
