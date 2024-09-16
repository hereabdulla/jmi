# Copyright (c) 2023, TEAMPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt


def execute(filters=None):
	if not filters:
		filters = {}
	columns = get_columns()
	data = []
	row = []
	salary_slips = get_conditions(filters)
	for ss in salary_slips:
		z = ss.employee
		a = ss.employee_name
		c = ss.bank_account_no
		d = ss.ifsc_code
		e = ss.gross_pay
		f = ss.designation
		g = ss.branch
		h = frappe.get_value('Salary Detail',{'salary_component':"Provident Fund",'parent':ss.name},["amount"] or 0)
		row = [z or "-",a or "-",f or "-",g or '-',c or "-",d or "-",e or 0,h or 0]
		data.append(row)

	return columns, data


def get_columns():
	columns = [
		_("Employee") + ":Data:100",
		_("Employee Name") + ":Data:150",
		_("Designation") + ":Data:150",
		_("Branch") + ":Data:150",
		_("Bank Account Number") + ":Data:150",
		_("IFSC Code") + ":Data:150",
		_("Gross Pay") + ":Data:120",
		_("PF") + ":Data:120",
	]
	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("start_date"):
		conditions += "start_date >= %(start_date)s"
	if filters.get("end_date"):
		conditions += " and end_date >= %(end_date)s"
	salary_slips = frappe.db.sql("""select * from `tabSalary Slip` where start_date = '%s' and end_date = '%s'"""%(filters.start_date, filters.end_date), as_dict=True)
	return salary_slips
