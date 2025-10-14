# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    zmall_api_url = fields.Char(
        string='Zmall API URL',
        help='URL endpoint for Zmall API to fetch order history',
        config_parameter='zmall.api.url',
        default='https://test.zmallapp.com/api/admin/history',
    )

    zmall_api_timeout = fields.Integer(
        string='API Timeout (seconds)',
        help='Maximum time to wait for API response',
        config_parameter='zmall.api.timeout',
        default=30,
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            zmall_api_url=params.get_param('zmall.api.url', 'https://test.zmallapp.com/api/admin/history'),
            zmall_api_timeout=int(params.get_param('zmall.api.timeout', 30)),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('zmall.api.url', self.zmall_api_url or 'https://test.zmallapp.com/api/admin/history')
        params.set_param('zmall.api.timeout', self.zmall_api_timeout or 30)

    def action_test_zmall_api_connection(self):
        """Test the API connection with current settings"""
        self.ensure_one()

        # Save current settings first
        self.set_values()

        # Try to fetch data for a recent date with data (Oct 2, 2025 based on your example)
        from datetime import date
        # Use October 2, 2025 as test date (from your API example response)
        test_date = date(2025, 10, 2)

        zmall_model = self.env['zmall.order.fetch']
        result = zmall_model.fetch_daily_orders(target_date=test_date)

        if result.get('status') == 'success':
            records_count = result.get('records_count', 0)
            total_pages = result.get('total_pages', 0)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Successful!',
                    'message': f"API test successful! Found {records_count} orders across {total_pages} page(s) for date {test_date}",
                    'type': 'success',
                    'sticky': False,
                }
            }
        elif result.get('status') == 'warning':
            # API responded but returned success=False
            records_count = result.get('records_count', 0)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'API Connected (No Data)',
                    'message': f"API is reachable but returned success=False for date {test_date}. This may mean no orders exist for this date. Try checking Order Fetch History for details.",
                    'type': 'warning',
                    'sticky': True,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Failed',
                    'message': f"API connection test failed: {result.get('message', 'Unknown error')}",
                    'type': 'danger',
                    'sticky': True,
                }
            }
