# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class AccountBalanceReport(models.TransientModel):
    _inherit = "account.balance.report"

    operating_unit_ids = fields.Many2many(
        'operating.unit', 'account_balance_report_operating_unit_rel',
        'account_id', 'operating_unit_id', string='Operating Units',
        required=False,
    )

    def _print_report(self, data):
        operating_units = ', '.join(self.operating_unit_ids.mapped('name'))
        data['form'].update({'operating_units': operating_units})
        return super(AccountBalanceReport, self)._print_report(data)
