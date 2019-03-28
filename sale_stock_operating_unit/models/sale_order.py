# © 2015-17 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('operating_unit_id')
    def onchange_operating_unit_id(self):
        if (self.operating_unit_id and
                self.operating_unit_id not in self.user_id.operating_unit_ids):
            self.user_id = False

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        domain = [('company_id', '=', company)]
        operating_unit = self.env.user.default_operating_unit_id
        if operating_unit and company == operating_unit.company_id.id:
            domain.append(('operating_unit_id', '=', operating_unit.id))
        warehouse_ids = self.env['stock.warehouse'].search(domain, limit=1)
        return warehouse_ids

    warehouse_id = fields.Many2one(default=_default_warehouse_id)


