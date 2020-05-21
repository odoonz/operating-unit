# Copyright 2020 O4SB
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrExpenseSheetRegisterPaymentWizard(models.TransientModel):

    _inherit = "hr.expense.sheet.register.payment.wizard"

    def _get_payment_vals(self):
        """
        Add operating unit to payment vals
        :return:
        """
        res = super()._get_payment_vals()

        active_ids = self._context.get("active_ids", [])
        expense_sheet = self.env["hr.expense.sheet"].browse(active_ids)
        operating_unit_id = expense_sheet.operating_unit_id.id
        if not operating_unit_id:
            operating_unit_id = self.env["res.users"]._get_operating_unit().id
        res["operating_unit_id"] = operating_unit_id
        return res
