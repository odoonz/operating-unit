# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MRPProduction(models.Model):
    _inherit = 'mrp.production'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        compute='_compute_operating_unit',
        store=True,
        compute_sudo=True,
    )

    @api.depends('location_src_id', 'location_dest_id')
    @api.onchange('location_src_id', 'location_dest_id')
    def _compute_operating_unit(self):
        for record in self:
            operating_unit_id = record.location_src_id.operating_unit_id
            if  operating_unit_id != record.location_dest_id.operating_unit_id:
                raise ValidationError("Manufacturing source and destination "
                                      "locations must belong to the same "
                                      "operating unit")
            else:
                record.operating_unit_id = operating_unit_id


