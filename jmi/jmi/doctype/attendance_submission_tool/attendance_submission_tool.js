// Copyright (c) 2023, TEAMPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Submission Tool', {
	refresh: function(frm) {
	// 	frm.set_value("from_date","")
	// 	frm.set_value("to_date","")
	// 	frm.set_value("branch","")
	// 	frm.set_value("contractor","")
		frm.disable_save()
	},

	submit_attendance(frm) {
		frappe.call({
			"method": "jmi.jmi.doctype.attendance_submission_tool.attendance_submission_tool.submit_att",
			"args":{
				"from_date":frm.doc.from_date,
				"to_date":frm.doc.to_date,
				"contractor":frm.doc.contractor,
				"branch":frm.doc.branch,
			},
			freeze: true,
			freeze_message: 'Submitted Attendance....',
			callback(r){
				if(r.message == "ok"){
					frappe.msgprint("Attendance Submitted Successfully")
				}
			}
		})
	}
});
