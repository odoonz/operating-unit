# © 2015-2017 Eficent
# - Jordi Ballester Alomar
# © 2015-2017 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResUsers(models.Model):

    _inherit = "res.users"

    @api.model
    def operating_unit_default_get(self, uid2):
        if not uid2:
            uid2 = self._uid
        user = self.env["res.users"].sudo().browse(uid2)
        default_ou = user.default_operating_unit_id
        return (
            default_ou
            if default_ou.company_id == user.company_id
            else user.operating_unit_ids.filtered(
                lambda s: s.company_id == user.company_id
            )[:1]
        )

    @api.model
    def _get_operating_unit(self):
        return self.operating_unit_default_get(self._uid)

    @api.model
    def _get_operating_units(self):
        return self._get_operating_unit()

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "operating_unit_users_rel",
        "user_id",
        "poid",
        "Operating Units",
        default=_get_operating_units,
    )
    default_operating_unit_id = fields.Many2one(
        "operating.unit", "Default Operating Unit", default=_get_operating_unit
    )
