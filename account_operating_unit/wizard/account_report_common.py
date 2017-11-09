# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class AccountCommonReport(models.TransientModel):
    _inherit = "account.common.report"

    operating_unit_ids = fields.Many2many('operating.unit',
                                          string='Operating Units',
                                          required=False)

    def _build_contexts(self, data):
        result = super(AccountCommonReport, self)._build_contexts(data)
        result['operating_unit_ids'] = self.read(['operating_unit_ids'])[0]
        return result
