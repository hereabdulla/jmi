# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class ApprovalSummary(Document):
	@frappe.whitelist()
	def submit_doc(self,doctype,name,workflow_state):
		doc = frappe.get_doc(doctype,name)
		doc.workflow_state = workflow_state
		doc.save(ignore_permissions=True)
		doc.submit()
		return "ok"

	@frappe.whitelist()
	def get_leave_app(self):
		data = frappe.get_list("Employee",{"workflow_state":"Pending For HR"},["name","first_name","branch",	"designation","contractor","company"])
		return data

	@frappe.whitelist()
	def get_att_app(self):
		data = frappe.get_list("Attendance Regularize",{"workflow_state":"Pending For HR"},["name","employee","branch","contractor","designation","corrected_total_working_hours","corrected_overtime_hours"])
		return data
	
	
	@frappe.whitelist()
	def submit_all_doc_after_approval(self,doctype,name,workflow_state):
		frappe.db.set_value(doctype,name,"workflow_state",workflow_state)
		return "ok"