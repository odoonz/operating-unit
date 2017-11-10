# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    @api.multi
    @api.constrains('purchase_line_id')
    def _check_purchase_order_operating_unit(self):
        for record in self:
            purchase = record.purchase_line_id.order_id
            location = record.location_id
            if (purchase and
                    purchase.operating_unit_id != location.operating_unit_id):
                raise ValidationError(_(
                    'Configuration error\n'
                    'The Quotation / Purchase Order and the Procurement Order '
                    'must belong to the same Operating Unit.')
                    )

    @api.multi
    def _prepare_purchase_order(self, product_id, product_qty, product_uom,
                                origin, values, partner):
        res = super(ProcurementRule, self)._prepare_purchase_order(
            product_id, product_qty, product_uom, origin, values, partner)
        operating_unit = self.location_id.operating_unit_id
        if operating_unit:
            res.update({
                'operating_unit_id': operating_unit.id,
                'requesting_operating_unit_id': operating_unit.id
            })
        return res
