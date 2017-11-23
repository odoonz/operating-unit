# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2017-TODAY Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):

    _inherit = 'crm.team'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=lambda self: self.env.user.default_operating_unit_id,
        required=True,
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        if self.filtered(lambda t: (
                t.company_id and
                t.company_id != t.operating_unit_id.company_id)):
            raise ValidationError(
                _('Configuration error!\n'
                  'The Company in the Sales Team and in the Operating Unit '
                  'must be the same.'))
