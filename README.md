# Employee Hub

A Frappe Framework application for managing departments, designations, employees with their skills, and leave requests with an approval workflow. Built as a Month 1 completion assignment covering DocTypes, Controllers, Client Scripts, Permissions, Workflows, Fixtures, Print Formats, and Script Reports.

## Setup

```bash
bench init hr-bench --frappe-branch version-16
cd hr-bench
bench new-site hr.localhost
bench new-app employee_hub
bench --site hr.localhost install-app employee_hub
bench use hr.localhost
bench start
```

Visit `http://hr.localhost:8000` and log in as Administrator.

**Note:** this app was developed on Frappe's `develop` branch (17.x) rather than `version-16`, since the shared bench used for development already hosted other apps pinned to `develop`. No version-16-specific features were required for this assignment — DocTypes, controllers, workflows, and reports built here should install cleanly on a version-16 site as well.

## DocTypes

| DocType | Type | Purpose |
|---|---|---|
| Department | Master | Organizational departments |
| Designation | Master | Job titles, linked to Department |
| Skill | Master | Skill catalogue with category |
| Employee | Transactional | Core employee record with skills child table |
| Employee Skill | Child Table | Skill + proficiency per employee |
| Leave Request | Submittable | Leave lifecycle with approval workflow |
| Leave Configuration | Single | Org-wide leave limits and settings |

## Features

- Autoname-by-name on all master DocTypes, with case-insensitive duplicate checking on Department
- Employee controller: auto-generated full_name, age/joining-date/email validation
- Leave Request controller: total_days calculation, balance and overlap validation, automatic balance deduction/restoration on submit/cancel
- Client scripts: department-designation filtering, live full_name preview, leave balance intro, submission confirmation dialogs
- Leave Approval Workflow (Pending → Approved/Rejected, Approved → Cancelled) with HR Admin and Employee roles
- Employee ID Card Jinja print format
- Department Wise Employee Summary script report with bar chart
- Custom blood_group field on Employee via Customize Form

## Assumptions & Known Deviations from Spec

- **Frappe develop branch used instead of version-16** — see Setup note above.
- **Leave Request's approval_status includes a "Cancelled" state** beyond the spec's Pending/Approved/Rejected, required for the Approved→Cancelled workflow transition.
- **Workflow's "Rejected" state maps to Doc Status 1 (Submitted)**, not 2 (Cancelled) — Frappe's docstatus model only permits sequential 0→1→2 transitions, so a direct Draft→Cancelled jump isn't possible. Rejected and Approved are both docstatus-Submitted, distinguished by the approval_status field value.
- **approval_status, approved_by, approval_date, and rejection_reason all require "Allow on Submit"** rather than staying strictly read-only, since both the Workflow engine and the controller's on_submit/on_cancel logic need to write these fields during the submit lifecycle.
- **Employee role has Write (not just Create) access on Leave Request** — Create alone left the new-document form incomplete on this Frappe build; Write was required for functional document creation, verified through testing. Fields the employee shouldn't control remain protected independently via the Allow-on-Submit/Workflow layer.
- **Row-level "own records only" restriction** (Employee role seeing only their own Employee/Leave Request records) is scoped at the DocType permission level for this assignment rather than via User Permissions, given the time constraints of a single-day build. A production rollout would add User Permission records linking each User to their Employee document.
- Departments with zero employees don't appear in the Script Report, since it aggregates from the Employee table.
