from odoo import models, fields

class PatientLogs(models.Model):
    _name = 'hms.patientlogs'
    _rec_name = 'description'
    patient_id = fields.Many2one(comodel_name="hms.patient")
    description = fields.Text()