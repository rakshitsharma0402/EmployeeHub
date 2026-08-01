# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	return columns, data, None, chart


def get_columns() -> list[dict]:
	return [
		{"label": _("Department"), "fieldname": "department", "fieldtype": "Link", "options": "Department", "width": 160},
		{"label": _("Total Employees"), "fieldname": "total_employees", "fieldtype": "Int", "width": 130},
		{"label": _("Active Employees"), "fieldname": "active_employees", "fieldtype": "Int", "width": 130},
		{"label": _("Inactive/Terminated"), "fieldname": "inactive_terminated", "fieldtype": "Int", "width": 150},
		{"label": _("Avg Leave Balance"), "fieldname": "avg_leave_balance", "fieldtype": "Float", "width": 150},
		{"label": _("Top Skill"), "fieldname": "top_skill", "fieldtype": "Data", "width": 150},
	]


def get_data(filters: dict) -> list[dict]:
	conditions, values = build_conditions(filters)

	department_rows = frappe.db.sql(
		f"""
		SELECT
			e.department AS department,
			COUNT(e.name) AS total_employees,
			SUM(CASE WHEN e.employee_status = 'Active' THEN 1 ELSE 0 END) AS active_employees,
			SUM(CASE WHEN e.employee_status IN ('Inactive', 'Terminated') THEN 1 ELSE 0 END) AS inactive_terminated,
			AVG(e.annual_leave_balance) AS avg_leave_balance
		FROM `tabEmployee` e
		WHERE 1=1 {conditions}
		GROUP BY e.department
		ORDER BY e.department
		""",
		values,
		as_dict=True,
	)

	for row in department_rows:
		row["top_skill"] = get_top_skill_for_department(row["department"])
		row["avg_leave_balance"] = round(row["avg_leave_balance"] or 0, 1)

	return department_rows


def build_conditions(filters: dict) -> tuple[str, dict]:
	conditions = ""
	values = {}

	if filters.get("department"):
		conditions += " AND e.department = %(department)s"
		values["department"] = filters["department"]

	if filters.get("employee_status"):
		conditions += " AND e.employee_status = %(employee_status)s"
		values["employee_status"] = filters["employee_status"]

	return conditions, values


def get_top_skill_for_department(department: str) -> str:
	result = frappe.db.sql(
		"""
		SELECT es.skill AS skill, COUNT(es.skill) AS skill_count
		FROM `tabEmployee` e
		JOIN `tabEmployee Skill` es ON es.parent = e.name
		WHERE e.department = %(department)s
		GROUP BY es.skill
		ORDER BY skill_count DESC
		LIMIT 1
		""",
		{"department": department},
		as_dict=True,
	)
	return result[0]["skill"] if result else "-"


def get_chart(data: list[dict]) -> dict:
	return {
		"data": {
			"labels": [row["department"] for row in data],
			"datasets": [{"name": "Employees", "values": [row["total_employees"] for row in data]}],
		},
		"type": "bar",
	}
