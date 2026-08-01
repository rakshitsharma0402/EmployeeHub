frappe.listview_settings["Employee"] = {
	add_fields: ["employee_status"],

	get_indicator: function (doc) {
		const status_colors = {
			Active: "green",
			"On Leave": "orange",
			Inactive: "gray",
			Terminated: "red",
		};
		const color = status_colors[doc.employee_status] || "gray";
		return [__(doc.employee_status), color, `employee_status,=,${doc.employee_status}`];
	},
};
