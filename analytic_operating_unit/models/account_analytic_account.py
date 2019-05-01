# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class AccountAnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    operating_unit_ids = fields.Many2many(
        comodel_name='operating.unit', string='Operating Units',
        relation='analytic_account_operating_unit_rel',
        column1='analytic_account_id',
        column2='operating_unit_id')

    # Technical field as too hard to put operating unit in reconciliation widget
    switch_to_operating_unit = fields.Many2one(
        comodel_name='operating.unit'
    )
