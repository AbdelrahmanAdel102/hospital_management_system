from odoo import models, fields , api
from odoo.exceptions import UserError


class CrmInherit(models.Model):
    _inherit = 'res.partner'


    related_patient_id = fields.Many2one(comodel_name='hms.patient',inverse_name='id')

    def unlink(self):
        if self.related_patient_id:
            raise UserError("You Can't Delete While Patient is Related")
        else:
            super(CrmInherit, self).unlink()

    def write(self, vals):
        if 'email' in vals:
            emails = self.env['hms.patient'].search([('email','=',vals['email'])])
            if emails:
                raise UserError('This e-mail is already taken')
            else:
                super().write(vals)

    @api.model
    def create(self, vals):
        if 'email' in vals:
            emails = self.env['hms.patient'].search([('email', '=', vals['email'])])
            if emails:
                raise UserError('This e-mail is already taken')
            else:
                super().create(vals)