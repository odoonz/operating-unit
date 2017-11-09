# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class AccountingReport(models.TransientModel):

    _inherit = "accounting.report"

    operating_unit_ids = fields.Many2many('operating.unit',
                                          string='Operating Units',
                                          required=False)

    def _build_contexts(self, data):
        result = super(AccountingReport, self)._build_contexts(data)
        result['operating_unit_ids'] = self.read(['operating_unit_ids'])[0]
        return result

    def _build_comparison_context(self, data):
        result = super(AccountingReport, self)._build_comparison_context(data)
        result['operating_unit_ids'] = self.read(['operating_unit_ids'])[0]
        return result

    def _print_report(self, data):
        operating_units = ', '.join(self.operating_unit_ids.mapped('name'))
        data['form'].update({'operating_units': operating_units})
        return super(AccountingReport, self)._print_report(data)
