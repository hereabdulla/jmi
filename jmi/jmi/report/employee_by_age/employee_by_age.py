# Copyright (c) 2024, TEAMPRO and contributors
# For license information, please see license.txt

# import frappe

# myapp/myapp/report/employee_age_report/employee_age_report.py

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"label": _("Age Range"), "fieldname": "age_range", "fieldtype": "Data"},
        {"label": _("Number of Employees"), "fieldname": "employee_count", "fieldtype": "Int"},
    ]
    data = []

    age_ranges = get_age_ranges()

    employees = frappe.get_all(
        "Employee",
        filters={"status": "Active"},
        fields=["name", "age"]
    )

    age_list = []
    for emp in employees:
        if emp.age is not None:
            age_list.append(int(emp.age))  # Ensure age is treated as an integer

    count_by_range = count_employees_by_range(age_list, age_ranges)

    for age_range, count in count_by_range.items():
        data.append({"age_range": age_range, "employee_count": count})

    return columns, data

def get_age_ranges():
    ranges = []
    for i in range(15, 80, 5):
        ranges.append(f"{i}-{i+4}")
    ranges.append("80+")
    return ranges

def count_employees_by_range(age_list, age_ranges):
    count_by_range = {range_: 0 for range_ in age_ranges}
    for age in age_list:
        for range_ in age_ranges:
            if range_ == "80+":
                if age >= 80:
                    count_by_range[range_] += 1
            else:
                start, end = map(int, range_.split("-"))
                if start <= age <= end:
                    count_by_range[range_] += 1
    return count_by_range