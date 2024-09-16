// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mark Employee Checkin', {
	refresh: function(frm) {
			frm.set_value("from_date","")
			frm.set_value("to_date","")
			frm.disable_save()
		},
});
