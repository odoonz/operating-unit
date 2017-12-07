# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from collections import defaultdict

from odoo.tools.translate import _
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import safe_eval


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=lambda self: self.env.user.default_operating_unit_id,
    )

    @api.model
    def create(self, vals):
        if not vals.get('operating_unit_id') and vals.get('move_id'):
            move = self.env['account.move'].browse(vals['move_id'])
            if move.operating_unit_id:
                vals['operating_unit_id'] = move.operating_unit_id.id
        _super = super(AccountMoveLine, self)
        return _super.create(vals)

    @api.model
    def _query_get(self, domain=None):
        if domain is None:
            domain = []
        if not isinstance(domain, (list, tuple)):
            domain = safe_eval(domain)
        if self._context.get('operating_unit_ids', False):
            domain.append(('operating_unit_id', 'in',
                           self._context.get('operating_unit_ids')))
        return super(AccountMoveLine, self)._query_get(domain)

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and rec.company_id !=
                    rec.operating_unit_id.company_id):
                raise ValidationError(_(
                    'Configuration error!\n'
                    'The Company in the move line and '
                    'Operating Unit must be the same.'))

    @api.multi
    @api.constrains('operating_unit_id', 'move_id')
    def _check_move_operating_unit(self):
        for rec in self:
            if (rec.move_id and rec.move_id.operating_unit_id and
                rec.operating_unit_id and rec.move_id.operating_unit_id !=
                    rec.operating_unit_id):
                raise ValidationError(_(
                    'Configuration error!\n'
                    'The Operating Unit in the move line and the move '
                    'must be the same.'))


class AccountMove(models.Model):
    _inherit = "account.move"

    operating_unit_id = fields.Many2one('operating.unit',
                                        'Default operating unit',
                                        help="This operating unit will "
                                             "be defaulted in the move lines.")

    @api.multi
    def _prepare_inter_ou_balancing_move_line(self, move, ou_id,
                                              ou_balances):
        if not move.company_id.inter_ou_clearing_account_id:
            raise ValidationError(_(
                'Error!\n'
                'You need to define an inter-operating '
                'unit clearing account in the company settings'))

        res = {
            'name': 'OU-Balancing',
            'move_id': move.id,
            'journal_id': move.journal_id.id,
            'date': move.date,
            'operating_unit_id': ou_id,
            'account_id': move.company_id.inter_ou_clearing_account_id.id
        }

        if ou_balances[ou_id] < 0.0:
            res['debit'] = abs(ou_balances[ou_id])

        else:
            res['credit'] = ou_balances[ou_id]
        return res

    @api.multi
    def _check_ou_balance(self, move):
        # Look for the balance of each OU
        ou_balance = defaultdict(float)
        for line in move.line_ids:
            ou_balance[line.operating_unit_id.id] += (line.debit - line.credit)
        return ou_balance

    @api.multi
    def post(self):
        ml_obj = self.env['account.move.line']
        for move in self:
            # If all move lines point to the same operating unit, there's no
            # need to create a balancing move line
            if len(move.line_ids.mapped(
                    lambda r: r.operating_unit_id or
                    self.env['operating.unit'])) <= 1:
                continue
            # Create balancing entries for un-balanced OU's.
            ou_balances = self._check_ou_balance(move)
            amls = []
            for ou_id in ou_balances.keys():
                # If the OU is already balanced, then do not continue
                if move.company_id.currency_id.is_zero(ou_balances[ou_id]):
                    continue
                # Create a balancing move line in the operating unit
                # clearing account
                line_data = self._prepare_inter_ou_balancing_move_line(
                    move, ou_id, ou_balances)
                if line_data:
                    amls.append(ml_obj.with_context(skip_ou_check=True).
                                create(line_data))
            if amls:
                move.with_context(skip_ou_check=False).write(
                    {'line_ids': [(4, aml.id) for aml in amls]})

        return super(AccountMove, self).post()

    def assert_balanced(self):
        if self.env.context.get('skip_ou_check'):
            return True
        return super(AccountMove, self).assert_balanced()

    @api.multi
    @api.constrains('line_ids')
    def _check_ou(self):
        for move in self:
            for line in move.line_ids:
                if not line.operating_unit_id:
                    raise ValidationError(_(
                        'Configuration error!\n'
                        'The operating unit must be completed for each line '
                        'if the operating unit has been defined as '
                        'self-balanced at company level.'))
