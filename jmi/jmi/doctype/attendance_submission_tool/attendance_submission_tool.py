# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AttendanceSubmissionTool(Document):
	def validate(self):
		frappe.db.sql("""update `tabAttendance` set docstatus = 1 where attendance_date between '%s' and '%s' and branch = '%s' and contractor = '%s' """%(self.from_date,self.to_date,self.branch,self.contractor))

