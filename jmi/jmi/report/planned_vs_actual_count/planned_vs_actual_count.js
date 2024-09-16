// Copyright (c) 2024, TEAMPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Planned Vs Actual Count"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			// "default": frappe.datetime.add_days(frappe.datetime.get_today(), -1),
			"reqd": 1,
		},
	]
};
