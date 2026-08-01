// Copyright (c) 2026, Rakshit Sharma and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
	refresh(frm) {
		set_designation_filter(frm);
		set_status_indicator(frm);
		add_create_leave_request_button(frm);
		add_view_skills_summary_button(frm);
	},

	department(frm) {
		frm.set_value("designation", "");
		set_designation_filter(frm);
	},

	first_name(frm) {
		update_full_name_preview(frm);
	},

	last_name(frm) {
		update_full_name_preview(frm);
	},
});

function set_designation_filter(frm) {
	frm.set_query("designation", () => {
		return {
			filters: {
				department: frm.doc.department,
			},
		};
	});
}

function update_full_name_preview(frm) {
	const first = frm.doc.first_name || "";
	const last = frm.doc.last_name || "";
	frm.set_value("full_name", `${first} ${last}`.trim());
}

function set_status_indicator(frm) {
	if (frm.doc.__islocal) return;

	const status_colors = {
		Active: "green",
		"On Leave": "orange",
		Terminated: "red",
		Inactive: "gray",
	};
	const color = status_colors[frm.doc.employee_status] || "gray";
	frm.dashboard.add_indicator(frm.doc.employee_status, color);
}
