import frappe

@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    emp_name = frappe.db.get_value('Employee',{'device_code': str(args['employee'])},['employee'])
    if frappe.db.exists('Employee',{'device_code':args['employee']}):
        if not frappe.db.exists('Employee Checkin',{'employee':str(args['employee']),'time':str(args['time'])}):
        
            ec = frappe.new_doc('Employee Checkin')
            ec.employee = emp_name
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
    # else:
    #     return "Checkin Marked"
