import frappe

@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    if not frappe.db.exists('Employee Checkin',{'employee':str(args['employee']),'time':str(args['time'])}):
        if frappe.db.exists('Employee',{'name':args['employee']}):
            ec = frappe.new_doc('Employee Checkin')
            ec.employee = args['employee'].upper()
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
            uec = frappe.new_doc('Unregistered Employee Checkin')
            uec.employee = args['employee'].upper()
            uec.time = args['time']
            uec.device_id = args['device_id']
            if args['log_type'] == 'in':
                uec.log_type = 'IN'
            elif args['log_type'] == 'out':
                uec.log_type = 'OUT'
            uec.save(ignore_permissions=True)
            frappe.db.commit()
            return "Checkin Marked"
    else:
        return "Checkin Marked"
