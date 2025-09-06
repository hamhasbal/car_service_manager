from odoo import models, fields

class CarMechanic(models.Model):
    _name = 'car.mechanic'
    _description = 'Car Mechanic'

    name = fields.Char(string="Name", required=True)
    specialty = fields.Char(string="Specialty")
    phone = fields.Char(string="Phone")
    service_order_ids = fields.One2many('car.service.order', 'mechanic_id', string="Service Orders")
