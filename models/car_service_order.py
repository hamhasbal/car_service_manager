from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ServiceOrder(models.Model):
    _name = 'car.service.order'
    _description = 'Car Service Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add chatter + activities

    # ===============================
    # Fields
    # ===============================
    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True
    )

    car_id = fields.Many2one(
        'car.service',
        string='Car',
        required=True,
        ondelete="restrict",
        tracking=True
    )

    partner_id = fields.Many2one(
        'res.partner',
        string="Customer",
        required=True,
        ondelete="restrict",
        related='car_id.partner_id',
        tracking=True
    )

    mechanic_id = fields.Many2one(
        'car.mechanic',
        string='Mechanic',
        ondelete="set null",
        tracking=True
    )

    service_type_id = fields.Many2one(
        'car.service.type',
        string='Service Type',
        required=True,
        ondelete="restrict",
        tracking=True
    )

    date_order = fields.Datetime(
        string='Order Date',
        default=fields.Datetime.now,
        tracking=True
    )

    amount = fields.Float(
        string='Total Amount',
        required=True,
        tracking=True
    )

    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        ondelete="set null",
        tracking=True
    )

    notes = fields.Text(string='Notes')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ('invoiced', 'Invoiced'),
    ], string='Status', default='draft', tracking=True)

    invoice_count = fields.Integer(
        string='Invoice Count',
        compute='_compute_invoice_count'
    )

    # ===============================
    # Computed
    # ===============================
    @api.depends('invoice_id')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = 1 if record.invoice_id else 0

    # ===============================
    # Onchange
    # ===============================
    @api.onchange('car_id')
    def _onchange_car(self):
        """Auto-fill customer when car is selected."""
        if self.car_id and getattr(self.car_id, "partner_id", False):
            self.partner_id = self.car_id.partner_id.id
        else:
            self.partner_id = False

    @api.onchange('service_type_id')
    def _onchange_service_type(self):
        """Auto-fill amount based on service type price."""
        if self.service_type_id and hasattr(self.service_type_id, 'price'):
            self.amount = self.service_type_id.price

    # ===============================
    # Invoice Actions
    # ===============================
    def action_create_invoice(self):
        """Create customer invoice manually."""
        self.ensure_one()

        if self.invoice_id:
            raise UserError(_("Invoice already exists for this service order."))

        if self.amount <= 0:
            raise UserError(_("Cannot create invoice with zero or negative amount."))

        if not self.partner_id:
            raise UserError(_("No customer linked with this service order."))

        # ✅ Odoo 18: use company_ids instead of company_id
        income_account = self.env['account.account'].search([
            ('account_type', '=', 'income'),
            ('company_ids', 'in', [self.env.company.id])
        ], limit=1)

        if not income_account:
            raise UserError(_("No income account found for company %s.") % self.env.company.name)

        invoice_line_vals = {
            'name': _("Service: %s for %s") % (
                self.service_type_id.name if self.service_type_id else _("Car Service"),
                self.car_id.name if self.car_id else _("Vehicle")
            ),
            'quantity': 1,
            'price_unit': self.amount,
            'account_id': income_account.id,
        }

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_origin': self.name,
            'ref': self.name,
            'invoice_line_ids': [(0, 0, invoice_line_vals)],
        }

        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id
        self.state = 'invoiced'

        self.message_post(
            body=_("Customer invoice %s created for service order.") % invoice.name,
            message_type='notification'
        )

        return {
            'type': 'ir.actions.act_window',
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current',
        }

    def action_view_invoice(self):
        """View the associated invoice."""
        self.ensure_one()
        if not self.invoice_id:
            raise UserError(_("No invoice found for this service order."))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'target': 'current',
        }

    # ===============================
    # Workflow
    # ===============================
    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_("Only draft orders can be confirmed."))
            record.write({'state': 'confirmed'})

            # Auto-create invoice here
            if record.amount > 0 and not record.invoice_id:
                record.action_create_invoice()

    def action_done(self):
        for record in self:
            if record.state not in ['confirmed', 'invoiced']:
                raise UserError(_("Service order must be confirmed first."))
            record.write({'state': 'done'})

    def action_cancel(self):
        for record in self:
            if record.state == 'done':
                raise UserError(_("Cannot cancel completed service orders."))
            if record.invoice_id and record.invoice_id.state == 'posted':
                raise UserError(_("Cannot cancel service order with posted invoice."))
            record.write({'state': 'cancelled'})

    def action_set_draft(self):
        for record in self:
            if record.invoice_id:
                raise UserError(_("Cannot set to draft when invoice exists. Delete invoice first."))
            record.write({'state': 'draft'})

    # ===============================
    # Override create
    # ===============================
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('car.service.order') or _('New')

        if vals.get("car_id") and not vals.get("partner_id"):
            car = self.env["car.service"].browse(vals["car_id"])
            if car and car.partner_id:
                vals["partner_id"] = car.partner_id.id
            else:
                raise UserError(_("Selected car has no linked customer. Please assign a customer."))

        return super(ServiceOrder, self).create(vals)
    
    # -------------------------------
    # Report Action
    # -------------------------------
    def action_print_report(self):
        """ Trigger PDF Fee Report """
        try:
            return self.env.ref(
                'car_service_manager.action_report_car_service_order'
            ).report_action(self)
        except ValueError:
            raise UserError(_("Report not found. Please ensure the report is correctly defined."))
