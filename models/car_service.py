from odoo import models, fields

class CarService(models.Model):
    _name = 'car.service'
    _description = 'Car'

    name = fields.Char(string="License Plate", required=True)
    partner_id = fields.Many2one('res.partner', string="Owner Name")
    brand = fields.Char(string="Brand")
    model = fields.Char(string="Model")
    year = fields.Integer(string="Year")
    next_service_due = fields.Char(string="Next Periodic Maintanance (km)")
    service_order_ids = fields.One2many('car.service.order', 'car_id', string="Service Orders")

    partner_id = fields.Many2one(
        'res.partner',
        string="Customer",
        required=True,
        help="Owner of the car (customer)."
    )