# Copyright (c) 2026, Rakshit Sharma and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


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
		total_days: DF.Date | None
	# end: auto-generated types

	_DOCTYPE_NAME = "Leave Request"
