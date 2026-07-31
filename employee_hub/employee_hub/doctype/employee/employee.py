# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

import re

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class Employee(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from employee_hub.employee_hub.doctype.employee_skill.employee_skill import EmployeeSkill
		from frappe.types import DF

		address: DF.SmallText | None
		annual_leave_balance: DF.Int
		date_of_birth: DF.Date
		date_of_joining: DF.Date
		department: DF.Link
		designation: DF.Link
		employee_email: DF.Data
		employee_status: DF.Literal["Active", "Inactive", "On Leave", "Terminated"]
		first_name: DF.Data
		full_name: DF.Data | None
		last_name: DF.Data
		naming_series: DF.Literal["EMP-.YYYY.-.#####"]
		phone: DF.Data | None
		profile_photo: DF.AttachImage | None
		reporting_manager: DF.Link | None
		skills: DF.Table[EmployeeSkill]
	# end: auto-generated types

	_DOCTYPE_NAME = "Employee"

	def before_save(self):
		self.full_name = f"{self.first_name} {self.last_name}".strip()

	def validate(self):
		self.validate_date_of_birth()
		self.validate_date_of_joining()
		self.validate_email_format()

	def validate_date_of_birth(self):
		dob = getdate(self.date_of_birth)
		age_years = (getdate(today()) - dob).days / 365.25
		if age_years < 18:
			frappe.throw(frappe._("Employee must be at least 18 years old."))

	def validate_date_of_joining(self):
		doj = getdate(self.date_of_joining)
		if doj > getdate(today()):
			frappe.throw(frappe._("Date of Joining cannot be in the future."))

		dob = getdate(self.date_of_birth)
		if doj <= dob:
			frappe.throw(frappe._("Date of Joining must be after Date of Birth."))

	def validate_email_format(self):
		pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
		if not re.match(pattern, self.employee_email):
			frappe.throw(frappe._("Please enter a valid email address for Employee Email."))
