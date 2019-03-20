# -*- coding: utf-8 -*-
# Copyright 2017 Open For Small Business Ltd
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class StockMove(models.Model):

    _inherit = 'stock.move'

    def _get_transaction_ou(self):
        """
        Currently only handles Sales
        :return:
        """
        if self._is_out() and self.sale_line_id:
            return self.sale_line_id.operating_unit_id
        return self.operating_unit_id or self.operating_unit_dest_id or self.sale_line_id.operating_unit_id

    def _xfer_price_get(self, product, qty, partner):
        """Hook Method to allow custom pricing algorithms.
        Uses pricelist set on partner"""
        product = product.with_context(
            partner=partner,
            quantity=qty,
            pricelist=partner.property_product_pricelist.id,
            uom=product.uom_id.id)
        return product.price * qty

    def _apply_intra_ou_transfer_pricing(self, xfer_value, qty, transaction_ou,
                                         inventory_ou):
        xfer_price = self._xfer_price_get(
            self.product_id, abs(qty), transaction_ou.partner_id) or xfer_value
        xfer_lines = []
        contribution_amount = xfer_price - xfer_value
        transfer_account = self.company_id.inter_ou_transfer_account_id
        clearing_account = self.company_id.inter_ou_clearing_account_id
        due_from_transaction_ou = {
            'name': '%s Inter OU Clearing' % self.name,
            'product_id': self.product_id.id,
            'quantity': qty,
            'partner_id': transaction_ou.partner_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': self.picking_id.name,
            'operating_unit_id': inventory_ou.id,
            'debit': xfer_price if xfer_price > 0 else 0,
            'credit': -xfer_price if xfer_price < 0 else 0,
            'account_id': clearing_account.id,
        }
        xfer_lines.append((0, 0, due_from_transaction_ou))
        due_to_inventory_ou = {
            'name': '%s Inter OU Clearing' % self.name,
            'product_id': self.product_id.id,
            'quantity': qty,
            'partner_id': inventory_ou.partner_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': self.picking_id.name,
            'operating_unit_id': transaction_ou.id,
            'debit': -xfer_price if xfer_price < 0 else 0,
            'credit': xfer_price if xfer_price > 0 else 0,
            'account_id': clearing_account.id,
            }
        xfer_lines.append((0, 0, due_to_inventory_ou))
        if not contribution_amount:
            return xfer_lines

        contribution_from_transaction_ou = {
            'name': '%s Inter OU Contribution' % self.name,
            'product_id': self.product_id.id,
            'quantity': qty,
            'partner_id': transaction_ou.partner_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': self.picking_id.name,
            'operating_unit_id': inventory_ou.id,
            'debit': -contribution_amount if contribution_amount < 0 else 0,
            'credit': contribution_amount if contribution_amount > 0 else 0,
            'account_id': transfer_account.id,
        }
        xfer_lines.append((0, 0, contribution_from_transaction_ou))

        contribution_to_inventory_ou = {
            'name': '%s Inter OU Contribution' % self.name,
            'product_id': self.product_id.id,
            'quantity': qty,
            'partner_id': inventory_ou.partner_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': self.picking_id.name,
            'operating_unit_id': transaction_ou.id,
            'debit': contribution_amount if contribution_amount > 0 else 0,
            'credit': -contribution_amount if contribution_amount < 0 else 0,
            'account_id': transfer_account.id,
        }
        xfer_lines.append((0, 0, contribution_to_inventory_ou))

        return xfer_lines

    def _create_transaction_ou_move(self, lines, transaction_ou):
        self.ensure_one()
        AccountMove = self.env['account.move']
        xact_lines = []
        other_lines = []
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        for line in lines:
            if line[2].get('operating_unit_id', 0) == transaction_ou.id:
                xact_lines.append(line)
            else:
                other_lines.append(line)

        if xact_lines:
            date = self._context.get('force_period_date', fields.Date.context_today(self))
            new_account_move = AccountMove.create({
                'journal_id': accounts_data['stock_journal'].id,
                'line_ids': xact_lines,
                'date': date,
                'ref': self.picking_id.name,
                'stock_move_id': self.id,
                'operating_unit_id': transaction_ou.id,
            })
            new_account_move.post()
        return other_lines

    def _prepare_account_move_line(self, qty, cost, credit_account_id,
                                   debit_account_id):
        lines = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id)
        inventory_ou = self.operating_unit_id or self.location_id.operating_unit_id or self.location_dest_id.operating_unit_id or self.sale_line_id.operating_unit_id

        transaction_ou = self._get_transaction_ou()
        if transaction_ou and inventory_ou != transaction_ou:
            xfer_value = 0.0
            for line in lines:
                if line[2]['debit']:
                    line[2]['operating_unit_id'] = transaction_ou.id
                elif line[2]['credit']:
                    line[2]['operating_unit_id'] = inventory_ou.id
                    xfer_value += line[2]['credit']
            xfer_lines = self._apply_intra_ou_transfer_pricing(
                xfer_value, qty, transaction_ou, inventory_ou)
            lines = self._create_transaction_ou_move(
                lines + xfer_lines, transaction_ou)
        else:
            for line in lines:
                line[2]["operating_unit_id"] = transaction_ou.id
        return lines
