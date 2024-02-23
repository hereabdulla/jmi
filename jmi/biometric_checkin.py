import frappe

@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
	if frappe.db.exists('Employee',{'device_code':args['employee']}):
		if not frappe.db.exists('Employee Checkin',{'employee':str(args['employee']),'time':str(args['time'])}):
			ec = frappe.new_doc('Employee Checkin')
			ec.employee = frappe.get_value('Employee',{'device_code':args['employee']},['name'])
			ec.device_code = args['employee'].upper()
			ec.time = args['time']
			ec.device_id = args['device_id']
			if args['log_type'] == 'in':
				ec.log_type = 'IN'
			elif args['log_type'] == 'out':
				ec.log_type = 'OUT'
			ec.save(ignore_permissions=True)
			frappe.db.commit()
			return "Checkin Marked"
		else:
			return "Checkin Marked"
	else:
		if not frappe.db.exists('Unregistered Employee Checkin',{'employee':str(args['employee']),'time':str(args['time'])}):
			uec = frappe.new_doc('Unregistered Employee Checkin')
			uec.employee = args['employee'].upper()
			uec.time = args['time']
			uec.device_id = args['device_id']
			if args['log_type'] == 'in':
				uec.log_type = 'IN'
			elif args['log_type'] == 'out':
				uec.log_type = 'OUT'
			if args['device_id'] == "BRM9222360384":
				uec.plant_with_type == "P1 IN"
			elif args['device_id'] == "BRM9222360383":
				uec.plant_with_type == "P1 OUT" 
			elif args['device_id'] == "BRM9203461488":
				uec.plant_with_type == "P2 IN" 
			elif args['device_id'] == "BRM9222360378":
				uec.plant_with_type == "P2 OUT" 
			elif args['device_id'] == "BRM9193660282":
				uec.plant_with_type == "P3 IN" 
			elif args['device_id'] == "BRM9222360385":
				uec.plant_with_type == "P4 OUT" 
			elif args['device_id'] == "BRM9211160652":
				uec.plant_with_type == "Seyoon IN" 
			elif args['device_id'] == "BRM9222361360":
				uec.plant_with_type == "Seyoon OUT" 
			elif args['device_id'] == "BRM9222361258":
				uec.plant_with_type == "VCR IN" 
			elif args['device_id'] == "BRM9215260842":
				uec.plant_with_type == "VCR OUT" 
			elif args['device_id'] == "BRM9222361255":
				uec.plant_with_type == "VCP IN" 
			elif args['device_id'] == "BRM9232260887":
				uec.plant_with_type == "VCP OUT"
			uec.save(ignore_permissions=True)
			frappe.db.commit()
			return "Checkin Marked"
		else:
			return "Checkin Marked"