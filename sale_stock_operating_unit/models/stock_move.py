# © 2015-17 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):
        """
        Override to add Operating Units to Picking.
        """
        vals = super(StockMove, self)._get_new_picking_values()
        sale = self.group_id and self.group_id.sale_id
        vals.update({'operating_unit_id': sale and sale.operating_unit_id.id})
        return vals
