# 
# from frappe import _
# import frappe
# from datetime import datetime

# def execute(filters=None):
#     columns = get_columns()
#     data = get_data(filters)
#     return columns, data

# def get_columns():
#     return [
#         _('Branch') + ':Data:200',
#         _('Branch Attendance Count') + ':Int:150',
#         _('Contractor') + ':Data:200',
#         _('Contractor Attendance Count') + ':Int:150'
#     ]

# def get_data(filters):
#     data = []

#     # Fetch the list of branches and contractors from Employee Plan
#     employee_plan = frappe.get_single('CL Employee Plan').contractor_employee_plan

#     for e in employee_plan:
#         # Calculate branch attendance count
#         branch_attendance_count = get_attendance_count(e.plant, filters)

#         # Calculate contractor attendance count
#         contractor_attendance_count = get_attendance_count(e.contractor, filters)

#         row = [e.plant, branch_attendance_count, e.contractor, contractor_attendance_count]
#         data.append(row)

#     return data

# def get_attendance_count(entity, filters):
#     # Query database to count attendance based on filters
#     query = """
#         SELECT COUNT(status) as cnt
#         FROM `tabAttendance`
#         WHERE attendance_date BETWEEN %(from_date)s AND %(to_date)s
#         AND status = 'Present' AND branch = %(entity)s
#     """
#     result = frappe.db.sql(query, {
#         'from_date': filters.from_date,
#         'to_date': filters.to_date,
#         'entity': entity
#     }, as_dict=True)

#     return result[0].cnt if result else 0


import frappe
from frappe import _
from datetime import datetime, date

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _('Branch') + ':Link/Branch:200',
        _('Today\'s Attendance Count') + ':Int:150',
        _('Contractor') + ':Link/Contractor:200',
        _('Today\'s Contractor Attendance Count') + ':Int:150',

    ]

def get_data(filters):
    data = []

    # Get the list of branches
    branches = frappe.get_all('Branch')
    contractor = frappe.get_all('Contractor')

    for branch in branches:
        # Get today's attendance count for the branch
        attendance_count = get_attendance_count(branch.name, filters.to_date)

        row = [branch.name, attendance_count]
        data.append(row)

    for contract in contractor :
        # Get today's attendance count for the branch
        attendance_count = get_attendance_count(contract.name, filters.to_date)

        row = [contract.name, attendance_count]
        data.append(row)

    return data

def get_attendance_count(branch, attendance_date):
    # Query database to count attendance for the specified branch and date
    query = """
        SELECT COUNT(*) as cnt
        FROM `tabAttendance`
        WHERE attendance_date = %(attendance_date)s
        AND branch = %(branch)s
    """
    result = frappe.db.sql(query, {
        'attendance_date': attendance_date,
        'branch': branch
    }, as_dict=True)

    return result[0].cnt if result else 0
