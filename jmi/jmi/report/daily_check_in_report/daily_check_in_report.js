// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Check IN Report"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default":frappe.datetime.nowdate(),
		},
		{
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
			
		},
		{
			"fieldname": "contractor",
			"label": __("Contractor"),
			"fieldtype": "Link",
			"options": "Contractor",
		},
	]
};

