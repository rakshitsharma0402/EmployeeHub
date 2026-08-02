# Employee Hub

Employee Hub is a lightweight Human Resource Management (HRM) application built with the Frappe Framework. It provides a centralized system for managing organizational departments, employee records, skills, and leave requests through role-based access control, approval workflows, reports, and printable documents.

## Features

### Employee Management
- Maintain employee records with personal and employment information.
- Auto-generate employee full names.
- Track employee skills and proficiency levels using a child table.
- Custom Blood Group field.
- Employee ID Card print format.

### Organization Management
- Manage departments and designations.
- Department-specific designation filtering.
- Human-readable naming for master records.
- Duplicate department prevention with case-insensitive validation.

### Leave Management
- Submit leave requests with configurable leave policies.
- Automatic leave duration calculation.
- Leave balance validation.
- Prevention of overlapping leave requests.
- Automatic leave balance deduction on approval.
- Automatic leave balance restoration on cancellation.

### Approval Workflow
- Role-based leave approval process.
- Approval, rejection, and cancellation workflow.
- Automatic recording of approver and approval date.

### User Experience
- Live employee full name preview.
- Dynamic department-based designation filtering.
- Remaining leave balance displayed while creating requests.
- Confirmation dialog before submitting leave requests.

### Reporting & Printing
- Department Wise Employee Summary Script Report.
- Employee ID Card Print Format.
- Department-wise employee distribution bar chart.

---

## Modules

| Module | Description |
|---------|-------------|
| Department | Manage organizational departments. |
| Designation | Maintain job titles linked to departments. |
| Skill | Centralized skill catalog. |
| Employee | Employee profiles, employment information, and skills. |
| Employee Skill | Child table for employee skill proficiency. |
| Leave Request | Leave request lifecycle with workflow approval. |
| Leave Configuration | Organization-wide leave policy configuration. |

---

## Leave Approval Workflow

```
Pending
   │
   ├── Approve (HR Admin)
   ▼
Approved
   │
   └── Cancel
   ▼
Cancelled

Pending
   │
   └── Reject (HR Admin)
   ▼
Rejected
```

---

## Business Rules

- Employees must be at least 18 years old.
- Joining date cannot be in the future.
- Employee email addresses are validated.
- Employee full name is generated automatically.
- Duplicate department names are prevented.
- Leave duration is calculated automatically.
- Leave requests cannot overlap.
- Leave balance is validated before submission.
- Leave balances are updated automatically during approval and cancellation.

---

## Tech Stack

- Frappe Framework
- Python
- MariaDB
- JavaScript
- Jinja2
- HTML/CSS

---

## Installation

### 1. Create a Bench

```bash
bench init test-bench
cd test-bench
```

### 2. Get the Application

Using SSH

```bash
bench get-app git@github.com:rakshitsharma0402/EmployeeHub.git
```

or HTTPS

```bash
bench get-app https://github.com/rakshitsharma0402/EmployeeHub.git
```

### 3. Create a Site

```bash
bench new-site employeehub.localhost
```

### 4. Install the Application

```bash
bench --site employeehub.localhost install-app employee_hub
```

### 5. Start the Bench

```bash
bench start
```

Visit

```
http://employeehub.localhost:8000
```

and log in as **Administrator**.

---

## License

MIT
