// Copyright (c) 2026, Rakshit Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Request", {
	refresh(frm) {
		if (frm.doc.employee) {
			set_balance_intro(frm);
		}
	},

	employee(frm) {
		set_balance_intro(frm);
	},

	from_date(frm) {
		calculate_total_days_preview(frm);
	},

	to_date(frm) {
		calculate_total_days_preview(frm);
	},

	before_submit(frm) {
		return new Promise((resolve, reject) => {
			frappe.confirm(
				__(
					"Submit leave request for {0}, from {1} to {2} ({3} days)?",
					[
						frm.doc.employee_name,
						frm.doc.from_date,
						frm.doc.to_date,
						frm.doc.total_days,
					]
				),
				() => resolve(),
				() => reject()
			);
		});
	},
});

function set_balance_intro(frm) {
	if (!frm.doc.employee) {
		frm.set_intro("");
		return;
	}

	frappe.db.get_value("Employee", frm.doc.employee, "annual_leave_balance").then((r) => {
		const balance = r.message.annual_leave_balance;
		frm.set_intro(__("Remaining leave balance: {0} days", [balance]), "blue");
	});
}

function calculate_total_days_preview(frm) {
	if (!frm.doc.from_date || !frm.doc.to_date) return;

	const total = frappe.datetime.get_day_diff(frm.doc.to_date, frm.doc.from_date) + 1;

	if (total <= 0) return;

	frm.set_value("total_days", total);

	frappe.db.get_single_value("Leave Configuration", "max_leave_days_per_request").then((max) => {
		if (total > max) {
			frappe.show_alert(
				{
					message: __("This request exceeds the maximum of {0} days per request.", [max]),
					indicator: "orange",
				},
				7
			);
		}
	});
}
