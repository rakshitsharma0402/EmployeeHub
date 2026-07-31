# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LeaveConfiguration(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		allow_backdated_leave: DF.Check
		default_annual_balance: DF.Int
		max_casual_leave: DF.Int
		max_earned_leave: DF.Int
		max_leave_days_per_request: DF.Int
		max_sick_leave: DF.Int
	# end: auto-generated types

	_DOCTYPE_NAME = "Leave Configuration"
