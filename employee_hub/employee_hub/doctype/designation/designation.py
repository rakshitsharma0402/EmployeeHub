# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Designation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		department: DF.Link | None
		description: DF.SmallText | None
		designation_name: DF.Data
		is_active: DF.Check
		level: DF.Literal["Junior", "Mid", "Senior", "Lead", "Manager"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Designation"
