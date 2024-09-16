// Copyright (c) 2023, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Approval Summary', {
	refresh: function(frm) {
		frm.disable_save()
		frm.trigger("data_fetch")

	$('*[data-fieldname="employee_approval_pending"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="employee_approval_pending"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="employee_approval_pending"]').find('.grid-add-row').remove()


	$('*[data-fieldname="attendance_regularize"]').find('.grid-remove-rows').hide();
	$('*[data-fieldname="attendance_regularize"]').find('.grid-remove-all-rows').hide();
	$('*[data-fieldname="attendance_regularize"]').find('.grid-add-row').remove()


	
	if (frappe.user.has_role(['HR Manager'])){
		frm.fields_dict["employee_approval_pending"].grid.add_custom_button(__('Reject'),
		function () {
			if(frm.doc.employee_approval_pending){
				$.each(frm.doc.employee_approval_pending, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Employee",
							name: d.employee_id,
							workflow_state: 'Draft'
						}).then(r => {
							frm.get_field("employee_approval_pending").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}			
		}).addClass('btn-danger')


		frm.fields_dict["employee_approval_pending"].grid.add_custom_button(__('Approve'),
		function () {
			if(frm.doc.employee_approval_pending){
				$.each(frm.doc.employee_approval_pending, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Employee",
							name: d.employee_id,
							workflow_state : "Active",
						}).then(r => {
							frm.get_field("employee_approval_pending").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}
		}).css({'color':'white','background-color':"#009E60","margin-left": "10px", "margin-right": "10px"});
		
		frm.fields_dict["attendance_regularize"].grid.add_custom_button(__('Reject'),
		function () {
			if(frm.doc.attendance_regularize){
				$.each(frm.doc.attendance_regularize, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Attendance Regularize",
							name: d.employee,
							workflow_state: 'Draft'
						}).then(r => {
							frm.get_field("attendance_regularize").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}			
		}).addClass('btn-danger')


		frm.fields_dict["attendance_regularize"].grid.add_custom_button(__('Approve'),
		function () {
			if(frm.doc.attendance_regularize){
				$.each(frm.doc.attendance_regularize, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_all_doc_after_approval', {
							doctype: "Employee",
							name: d.employee,
							workflow_state : "Approved",
						}).then(r => {
							frm.get_field("attendance_regularize").grid.grid_rows[d.idx - 1].remove();
						})
					}
				})
			}
		}).css({'color':'white','background-color':"#009E60","margin-left": "10px", "margin-right": "10px"});
		

	}
	},
		
	
	onload(frm){
		frappe.run_serially([
			() => frm.call('get_leave_app').then(r=>{
				if (frappe.session.user){
			
				if (r.message) {
					$.each(r.message, function (i, d) {
						frm.add_child('employee_approval_pending', {
							'employee_id':d.name,
							'employee_name':d.first_name,
							'branch':d.branch,
							'designation' :d.designation,
							'contracor':d.contracor,
							'company':d.company,
							

						})
						frm.refresh_field('employee_approval_pending')	
					})
				}
			}
		}
			)	,
			() => frm.call('get_att_app').then(r=>{
				if (frappe.session.user){
					if (frappe.user.has_role(['HR Manager'])){
				if (r.message) {
					$.each(r.message, function (i, d) {
						frm.add_child('attendance_regularize', {
							'application_id':d.name,
							'employee':d.employee,
							'attendance_date':d.attendance_date,
							'branch':d.branch,
							
							'contracor':d.contracor,
							'designation' :d.designation,
							'corrected_total_working_hours':d.corrected_total_working_hours,
							'corrected_overtime_hours':d.corrected_overtime_hours,
							

						})
						frm.refresh_field('attendance_regularize')	
					})
				}
			}
		}
			})	,
			
			
		])
	}	

});
