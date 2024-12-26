# -*- coding: utf-8 -*-
# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe

import frappe
from frappe.model.document import Document
import json
from frappe.utils import getdate, add_days, get_time,today
from frappe import _
import datetime
from datetime import timedelta, datetime, date

class ExpenseEntry(Document):
	pass
	def validate(self):
		self.calculate_total_debit_amount()
	
	def calculate_total_debit_amount(self):
		total_db = 0
        # Iterate through the child table items to sum up the amounts
		for i in self.cash_expense_entry_accounts:
			total_db += i.amount
        # Assign the calculated value to the total_debit_amount field
		self.total_debit_amount = total_db

	# def before_save(self):
	# 	self.petty_cash_acc()
	# 	self.total_debit_amount()
	def on_submit(self):
		self.create_jv()
	@frappe.whitelist()
	def create_jv(self):
		jv = frappe.new_doc('Journal Entry')
		jv.voucher_type = "Cash Entry"
		jv.company = self.company
		jv.payment_type = "Expense Payment"
		jv.posting_date = self.posting_date
		jv.total_debit = self.total_debit_amount
		jv.total_cridet = self.total_debit_amount
		#jv.cheque_no = self.reference_no
		#jv.cheque_date = self.reference_date
		for jv_detail in self.cash_expense_entry_accounts:
			accounts = jv.append('accounts')
			accounts.account = jv_detail.account
			accounts.user_remark = jv_detail.remakrs
			accounts.debit_in_account_currency = jv_detail.amount
		accountscr = jv.append('accounts')
		accountscr.account = self.petty_cash_account
		accountscr.credit_in_account_currency = self.total_debit_amount
		jv.save()
		jv.submit()
	# def petty_cash_acc(self):
	# 	from erpnext.accounts.utils import get_balance_on
	# 	account_balance = get_balance_on(self.petty_cash_account)
	# 	self.account_balance = account_balance

	