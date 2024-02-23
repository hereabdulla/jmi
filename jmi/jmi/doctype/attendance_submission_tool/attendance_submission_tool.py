# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AttendanceSubmissionTool(Document):
	pass
	
@frappe.whitelist()	
def submit_att(from_date,to_date,contractor,branch):
	frappe.db.sql("""update `tabAttendance` set docstatus = 1 where attendance_date between '%s' and '%s' and branch = '%s' and contractor = '%s' """%(from_date,to_date,branch,contractor))

