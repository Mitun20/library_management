# Copyright (c) 2025, testing@gmail.coom and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryMembership(Document):

    def validate(self):
        if self.from_date and self.to_date:
            if self.to_date < self.from_date:
                frappe.throw("To Date must be greater than or equal to From Date")

    def before_submit(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                # "from_date": ("<=", self.to_date),	
                "to_date": (">", self.from_date),
            },
        )

        if exists:
            frappe.throw("There is already an active membership for this member")

        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)
	
