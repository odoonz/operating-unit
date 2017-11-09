# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    operating_unit_id = fields.Many2one(comodel_name='operating.unit',
                                        string='Operating Unit',
                                        index=True,
                                        help="Operating Unit that will be "
                                             "used in payments, when this "
                                             "journal is used.")

    @api.onchange('type')
    def onchange_journal_type(self):
        if self.type not in ['bank', 'cash']:
            self.operating_unit_id = False

    @api.multi
    @api.constrains('type')
    def _check_ou(self):
        for journal in self:
            if journal.type in ('bank', 'cash') \
                    and journal.company_id.ou_is_self_balanced \
                    and not journal.operating_unit_id:
                raise ValidationError(_(
                    'Configuration error!\n'
                    'The operating unit must be indicated in bank journals if '
                    'it has been defined as self-balanced at company level.'))
