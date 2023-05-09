// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Dashboard', {
	refresh: function(frm) {
		frm.disable_save()
	},
	download: function (frm) {
		if (frm.doc.report == 'Wage Register') {
			var path = "jmi.jmi.doctype.report_dashboard.wage_register.download"
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s&contractor=%(contractor)s&branch=%(branch)s'
		}
		if (path) {
			window.location.href = repl(frappe.request.url +
				'?cmd=%(cmd)s&%(args)s', {
				cmd: path,
				args: args,
				// date: frm.doc.date,
				from_date : frm.doc.from_date,
				to_date : frm.doc.to_date,
				// employee : frm.doc.employee,
				contractor : frm.doc.contractor,
			    branch : frm.doc.branch,
				// job_order_number : frm.doc.job_order_number
			
			});
		}
	}
});
