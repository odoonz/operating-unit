# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'


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

    def _make_po_select_supplier(self, values, suppliers):
        """ Method intended to be overridden by customized modules to implement any logic in the
            selection of supplier.
        """
        def _ou_suppliers(r):
            return (not r.operating_unit_id or
                    r.operating_unit_id == self.location_id.operating_unit_id)

        if self.location_id.operating_unit_id:
            suppliers = suppliers.filtered(_ou_suppliers)
        return super(
            ProcurementRule, self)._make_po_select_supplier(values, suppliers)

    def _run_buy(self, product_id, product_qty, product_uom, location_id,
                 name, origin, values):
        return super(ProcurementRule, self.with_context(
                operating_unit=self.location_id.operating_unit_id))._run_buy(
                    product_id, product_qty, product_uom, location_id,
                    name, origin, values)
