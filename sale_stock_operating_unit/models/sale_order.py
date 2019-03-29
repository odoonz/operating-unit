# © 2015-17 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('operating_unit_id')
    def onchange_operating_unit_id(self):
        if (self.operating_unit_id and
                self.operating_unit_id not in self.user_id.operating_unit_ids):
            self.user_id = False
