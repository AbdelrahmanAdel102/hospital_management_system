from odoo import models, fields, api
from datetime import date
from odoo.exceptions import UserError
import re


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    birthdate = fields.Date()
    age = fields.Integer(compute='_compute_age')
    address = fields.Text()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('type1', 'Type1'),
        ('type2', 'Type2'),
        ('type3', 'Type3'),
    ])
    history = fields.Html()
    pcr = fields.Boolean()
    image = fields.Image()
    departmnet_ids = fields.Many2one(comodel_name='hms.department')
    state = fields.Selection([
        ('undetermined','Undetermined'),
        ('good','Good'),
        ('fair','Fair'),
        ('serious','Serious'),
    ])
    doctor = fields.Many2many(comodel_name='hms.doctors')
    email = fields.Char()
    logs_history = fields.One2many(comodel_name='hms.patientlogs',inverse_name='id')



    _sql_constraints = [
        ('email_unique_constraint','UNIQUE(email)','Email is already exists'),
    ]

    def log_change(self, data):
        print('done')
        self.env['hms.patientlogs'].create({
            'description': 'State changed to {}'.format(data), 'patient_id': self.id})

    def undetermined(self):
        self.state = 'undetermined'
        self.log_change(self.state)
    def good(self):
        self.state = 'good'
        self.log_change(self.state)
    def fair(self):
        self.state = 'fair'
        self.log_change(self.state)
    def serious(self):
        self.state = 'serious'
        self.log_change(self.state)

    @api.onchange('age')
    def _onchange_pcr(self):
        if self.age:
            if self.age <= 30:
                self.pcr = True
                return {
                    'title': 'Alert',
                    'warning' : {'title' : 'warning',
                                 'message':'The PCR Has been Checked'}
            }
            else:
                self.pcr = False

    @api.onchange('birthdate')
    def _compute_age(self):
        if self.birthdate:
            for rec in self:
                rec.age = date.today().year - rec.birthdate.year

    @api.constrains('email')
    def _check_email(self):
        if self.email:
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if not re.fullmatch(regex, self.email):
                raise UserError('Please Enter Valid E-mail')
