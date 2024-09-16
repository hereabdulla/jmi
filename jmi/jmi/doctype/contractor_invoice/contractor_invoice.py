# Copyright (c) 2022, TEAMPRO and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_url_to_form,money_in_words

class ContractorInvoice(Document):
	pass

@frappe.whitelist()
def get_md(contractor,branch,start_date,end_date,designation):
	mdr = frappe.get_value('Contractor Wages',{'designation':designation,'parent':contractor},['total'])
	tar = frappe.get_value('Contractor Wages',{'designation':designation,'parent':contractor},['travel_allowance_rate'])
	man_days = frappe.db.sql("""select sum(payment_days) from `tabSalary Slip` where docstatus != '2' and contractor ='%s' and branch = '%s' and start_date = '%s' and end_date = '%s' and designation = '%s' """%(contractor,branch,start_date,end_date,designation),as_dict = 1)[0]
	ot = frappe.db.sql("""select (sum(overtime_hours))  as ot_hrs from `tabSalary Slip` where docstatus != 2  and contractor ='%s' and branch ='%s' and start_date = '%s' and end_date = '%s' and designation = '%s' """%(contractor,branch,start_date,end_date,designation),as_dict = 1)[0]
	return man_days['sum(payment_days)'] or 0 ,  ot['ot_hrs'] or 0 , mdr or 0 ,tar or 0

@frappe.whitelist()
def get_total_amount_in_words(total_amount):
	tot = money_in_words(total_amount)
	return tot
