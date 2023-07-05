# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResUsersRole(models.Model):
    _inherit = "res.users.role"

    unrestrict_model_update = fields.Boolean(copy=False)
    is_readonly_user = fields.Boolean(copy=False)

    @api.onchange("is_readonly_user")
    def onchange_is_readonly_user(self):
        for rec in self:
            rec.line_ids.mapped("user_id").write(
                {"is_readonly_user": rec.is_readonly_user}
            )

    @api.onchange("unrestrict_model_update")
    def onchange_unrestrict_model_update(self):
        for rec in self:
            rec.line_ids.mapped("user_id").write(
                {"unrestrict_model_update": rec.unrestrict_model_update}
            )


class ResUsersRoleLine(models.Model):
    _inherit = "res.users.role.line"

    @api.model
    def create(self, vals):
        line = super().create(vals)
        line.user_id.write(
            {
                "is_readonly_user": line.role_id.is_readonly_user,
                "unrestrict_model_update": line.role_id.unrestrict_model_update,
            }
        )
        return line
