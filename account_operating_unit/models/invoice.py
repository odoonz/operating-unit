# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=lambda self: self.env['res.users'].operating_unit_default_get(
            self._uid),
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
    )

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        move_lines = super(AccountInvoice,
                           self).finalize_invoice_move_lines(move_lines)
        if self.operating_unit_id:
            for line_tuple in move_lines:
                if not line_tuple[2].get('operating_unit_id'):
                    line_tuple[2]['operating_unit_id'] = self.operating_unit_id.id
        return move_lines

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        if self.filtered(lambda s: (s.operating_unit_id and
                                    s.company_id !=
                                    s.operating_unit_id.company_id)):
            raise ValidationError(_('The Company in the Invoice and in '
                                    'Operating Unit must be the same.'))
        return True

    @api.model
    def invoice_line_move_line_get(self):
        res = super().invoice_line_move_line_get()
        inv_line_ou = {l.id: l.operating_unit_id.id for l in self.invoice_line_ids}
        for line in res:
            line['operating_unit_id'] = inv_line_ou.get(line['invl_id'], self.operating_unit_id.id)
        return res
    
    def action_invoice_open(self):
        seen_ou = set()
        for inv in self:
            seen_ou.add(inv.operating_unit_id.id)
            for line in inv.invoice_line_ids:
                if not line.operating_unit_id:
                    line.operating_unit_id = inv.operating_unit_id
        ctx = {}
        if len(seen_ou) == 1:
            ctx.update(default_operating_unit=seen_ou.pop())
        return super(AccountInvoice, self.with_context(**ctx)).action_invoice_open()


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        default=lambda s: s.env.context.get('operating_unit') or s.invoice_id.operating_unit_id,
        string='Operating Unit',
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        res = super()._convert_prepared_anglosaxon_line(line, partner)
        res.update({'operating_unit_id': line.get('operating_unit_id')})
        return res
