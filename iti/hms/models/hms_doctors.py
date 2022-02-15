from odoo import models, fields

class HmsDoctors(models.Model):
    _name = 'hms.doctors'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Image()

