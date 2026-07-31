# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate, now_datetime, today


class LeaveRequest(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		approval_date: DF.Datetime | None
		approval_status: DF.Literal["Pending", "Approved", "Rejected", "Cancelled"]
		approved_by: DF.Link | None
		department: DF.Link | None
		employee: DF.Link
		employee_name: DF.Data | None
		from_date: DF.Date
		leave_type: DF.Literal["Casual Leave", "Sick Leave", "Earned Leave", "Compensatory Leave"]
		naming_series: DF.Literal["LR-.YYYY.-.#####"]
		reason: DF.Text
		rejection_reason: DF.SmallText | None
		to_date: DF.Date
		total_days: DF.Float
	# end: auto-generated types

	_DOCTYPE_NAME = "Leave Request"

	def validate(self):
		self.calculate_total_days()
		self.validate_dates()
		self.validate_leave_balance()
		self.validate_overlapping_leave()

	def calculate_total_days(self):
		self.total_days = date_diff(self.to_date, self.from_date) + 1

	def validate_dates(self):
		if getdate(self.to_date) < getdate(self.from_date):
			frappe.throw(frappe._("To Date cannot be before From Date."))

		config = frappe.get_single("Leave Configuration")
		if not config.allow_backdated_leave and getdate(self.from_date) < getdate(today()):
			frappe.throw(frappe._("From Date cannot be in the past."))

		if self.total_days > config.max_leave_days_per_request:
			frappe.throw(
				frappe._("Leave request exceeds the maximum of {0} days allowed per request.").format(
					config.max_leave_days_per_request
				)
			)

	def validate_leave_balance(self):
		employee_balance = frappe.db.get_value("Employee", self.employee, "annual_leave_balance")
		if self.total_days > employee_balance:
			frappe.throw(
				frappe._("Requested {0} days exceeds available leave balance of {1} days.").format(
					self.total_days, employee_balance
				)
			)

	def validate_overlapping_leave(self):
		overlapping = frappe.db.sql(
			"""
			SELECT name FROM `tabLeave Request`
			WHERE employee = %(employee)s
				AND docstatus = 1
				AND approval_status = 'Approved'
				AND name != %(name)s
				AND from_date <= %(to_date)s
				AND to_date >= %(from_date)s
			""",
			{
				"employee": self.employee,
				"name": self.name or "",
				"from_date": self.from_date,
				"to_date": self.to_date,
			},
		)
		if overlapping:
			frappe.throw(
				frappe._("This overlaps with an existing approved leave request ({0}).").format(
					overlapping[0][0]
				)
			)

	def on_submit(self):
		self.approval_status = "Approved"
		self.approved_by = frappe.session.user
		self.approval_date = now_datetime()

		employee = frappe.get_doc("Employee", self.employee)
		employee.annual_leave_balance -= self.total_days
		employee.save(ignore_permissions=True)

	def on_cancel(self):
		employee = frappe.get_doc("Employee", self.employee)
		employee.annual_leave_balance += self.total_days

		if self.rejection_reason:
			self.approval_status = "Rejected"
		else:
			self.approval_status = "Cancelled"

		if employee.employee_status == "On Leave":
			employee.employee_status = "Active"

		employee.save(ignore_permissions=True)
