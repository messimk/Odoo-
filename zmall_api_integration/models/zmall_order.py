# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ZmallOrder(models.Model):
    _name = 'zmall.order'
    _description = 'Zmall Order Details'
    _order = 'order_date desc'

    # Basic Order Info
    name = fields.Char(string='Order Reference', compute='_compute_name', store=True)
    zmall_order_id = fields.Char(string='Zmall Order ID', required=True, index=True)
    unique_id = fields.Integer(string='Unique ID')
    order_date = fields.Datetime(string='Order Date')
    completed_date = fields.Datetime(string='Completed Date')
    order_status = fields.Integer(string='Order Status')
    order_type = fields.Integer(string='Order Type')

    # Customer Information
    customer_first_name = fields.Char(string='Customer First Name')
    customer_last_name = fields.Char(string='Customer Last Name')
    customer_email = fields.Char(string='Customer Email')
    customer_phone = fields.Char(string='Customer Phone')
    customer_country_code = fields.Char(string='Country Code')

    # Store Information
    store_name = fields.Char(string='Store Name')
    store_email = fields.Char(string='Store Email')
    store_phone = fields.Char(string='Store Phone')
    store_address = fields.Char(string='Store Address')

    # Payment Information
    total_payment = fields.Float(string='Total Payment', digits=(16, 2))
    cash_payment = fields.Float(string='Cash Payment', digits=(16, 2))
    card_payment = fields.Float(string='Card Payment', digits=(16, 2))
    wallet_payment = fields.Float(string='Wallet Payment', digits=(16, 2))
    payment_method = fields.Char(string='Payment Method')
    currency_code = fields.Char(string='Currency', default='ETB')
    is_payment_paid = fields.Boolean(string='Payment Paid')

    # Delivery Information
    delivery_type = fields.Integer(string='Delivery Type')
    delivery_price = fields.Float(string='Delivery Price', digits=(16, 2))
    delivery_address = fields.Char(string='Delivery Address')

    # Order Items
    order_item_ids = fields.One2many('zmall.order.item', 'order_id', string='Order Items')
    total_items = fields.Integer(string='Total Items', compute='_compute_total_items', store=True)

    # Additional Info
    order_payment_unique_id = fields.Integer(string='Payment Unique ID')
    invoice_number = fields.Char(string='Invoice Number')
    confirmation_code_pickup = fields.Integer(string='Pickup Confirmation Code')
    confirmation_code_complete = fields.Integer(string='Complete Confirmation Code')

    # Provider Information
    provider_name = fields.Char(string='Provider Name')
    provider_email = fields.Char(string='Provider Email')
    provider_phone = fields.Char(string='Provider Phone')

    # Technical
    fetch_id = fields.Many2one('zmall.order.fetch', string='Fetch Record', ondelete='cascade')
    raw_data = fields.Text(string='Raw JSON Data')

    @api.depends('unique_id')
    def _compute_name(self):
        for record in self:
            record.name = f"Order #{record.unique_id}" if record.unique_id else "New Order"

    @api.depends('order_item_ids')
    def _compute_total_items(self):
        for record in self:
            record.total_items = len(record.order_item_ids)


class ZmallOrderItem(models.Model):
    _name = 'zmall.order.item'
    _description = 'Zmall Order Item'
    _order = 'order_id, sequence'

    order_id = fields.Many2one('zmall.order', string='Order', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)

    # Product Information
    product_name = fields.Char(string='Product Name')
    item_name = fields.Char(string='Item Name')
    item_id = fields.Char(string='Item ID')
    product_id = fields.Char(string='Product ID')

    # Pricing
    item_price = fields.Float(string='Unit Price', digits=(16, 2))
    quantity = fields.Integer(string='Quantity', default=1)
    total_price = fields.Float(string='Total Price', digits=(16, 2))
    item_tax = fields.Float(string='Tax', digits=(16, 2))

    # Additional
    note = fields.Text(string='Notes')
    specifications = fields.Text(string='Specifications')
