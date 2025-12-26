# Copyright (c) 2025, testing@gmail.coom and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryTransaction(Document):
	def before_submit(self):
		if self.type == "Issue":
			self.validate_issue()
			article = frappe.get_doc("Article", self.article)
			article.status = "Issued"
			article.save()
		elif self.type == "Return":
			self.validate_return()
			article = frappe.get_doc("Article", self.article)
			article.status = "Available"
			article.save()
		
	def validate_issue(self):
		self.validate_membership()
		article = frappe.get_doc("Article", self.article)
		if article.status == "Issued":
			frappe.throw("Article is already issued to another member")

	def validate_return(self):
		article = frappe.get_doc("Article", self.article)
		if article.status == "Available":
			frappe.throw("Article is not issued to any member")
			
	def validate_membership(self):
		validate_membership = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": DocStatus.submitted(),
				"from_date": ("<", self.date),
				"to_date": (">", self.date),
			},
		)
		if not validate_membership:
			frappe.throw("The member does not have a valid membership")