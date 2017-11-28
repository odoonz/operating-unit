# -*- coding: utf-8 -*-
# Copyright 2017 Open For Small Business Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# flake8: noqa
# as we are copying from odoo core
from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _select_seller(self, partner_id=False, quantity=0.0, date=None, uom_id=False):
        self.ensure_one()
        if date is None:
            date = fields.Date.context_today(self)  # Note - change from naive date

        # Filter for OU Here
        sellers = self.seller_ids
        if self._context.get('operating_unit'):
            sellers = sellers.filtered(
                lambda r: not r.operating_unit_id or
                r.operating_unit_id == self._context['operating_unit'])

        # Cut and paste here
        res = self.env['product.supplierinfo']
        for seller in sellers:
            # Set quantity in UoM of seller
            quantity_uom_seller = quantity
            if quantity_uom_seller and uom_id and uom_id != seller.product_uom:
                quantity_uom_seller = uom_id._compute_quantity(quantity_uom_seller, seller.product_uom)

            if seller.date_start and seller.date_start > date:
                continue
            if seller.date_end and seller.date_end < date:
                continue
            if partner_id and seller.name not in [partner_id, partner_id.parent_id]:
                continue
            if quantity_uom_seller < seller.min_qty:
                continue
            if seller.product_id and seller.product_id != self:
                continue

            res |= seller
            break
        return res
