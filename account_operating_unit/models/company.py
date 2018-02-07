# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    inter_ou_clearing_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Inter-operating unit clearing account',
        domain="[('user_type_id.type', '=', 'payable'),"
               "('company_id', '=', id)]",
        help="This payable account maintains balances owing between "
             "Operating Units",
    )

    inter_ou_transfer_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Inter-operating unit transfer account',
        domain="[('user_type_id.type', '=', 'other'),"
               "('company_id', '=', id)]",
        help="This P&L account maintains contributions between "
             "Operating Units",
    )
