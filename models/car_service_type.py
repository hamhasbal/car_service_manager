from odoo import models, fields

class CarServiceType(models.Model):
    _name = 'car.service.type'
    _description = 'Car Service Type'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    service_order_ids = fields.One2many('car.service.order', 'service_type_id', string="Service Orders")
