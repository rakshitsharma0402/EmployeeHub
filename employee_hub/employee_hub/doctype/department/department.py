import frappe
from frappe.model.document import Document


class Department(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		department_head: DF.Data | None
		department_name: DF.Data
		description: DF.SmallText | None
		is_active: DF.Check
	# end: auto-generated types

	_DOCTYPE_NAME = "Department"

	def validate(self):
		self.check_duplicate_department_name()

	def check_duplicate_department_name(self):
		all_departments = frappe.get_all(
			"Department", fields=["name", "department_name"]
		)
		for dept in all_departments:
			if (
				dept.department_name.lower() == self.department_name.lower()
				and dept.name != self.name
			):
				frappe.throw(
					frappe._("A Department with the name '{0}' already exists.").format(
						self.department_name
					)
				)
