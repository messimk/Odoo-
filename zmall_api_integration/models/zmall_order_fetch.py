# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import requests
import json
import logging
from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ZmallOrderFetch(models.Model):
    _name = 'zmall.order.fetch'
    _description = 'Zmall Order Fetch History'
    _order = 'fetch_date desc'

    name = fields.Char(string='Reference', required=True, default='New', readonly=True)
    fetch_date = fields.Date(string='Fetch Date', required=True, default=fields.Date.context_today, readonly=True)
    start_date = fields.Date(string='Start Date', required=True, readonly=True)
    end_date = fields.Date(string='End Date', required=True, readonly=True)
    records_count = fields.Integer(string='Records Fetched', readonly=True, default=0)
    total_pages = fields.Integer(string='Total Pages', readonly=True, default=0)
    success = fields.Boolean(string='Success', readonly=True, default=False)
    error_message = fields.Text(string='Error Message', readonly=True)
    api_response = fields.Text(string='API Response Summary', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Status', default='draft', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('zmall.order.fetch') or 'New'
        return super(ZmallOrderFetch, self).create(vals)

    @staticmethod
    def _generate_zmall_date_object(date_obj, is_end_of_day=False):
        """
        Generate Zmall-style date object with all required fields.

        Args:
            date_obj (datetime.date): The date to convert
            is_end_of_day (bool): If True, set time to 23:59:59, else 00:00:00

        Returns:
            dict: Zmall date object with date, epoc, formatted, and jsdate
        """
        # Create datetime object with appropriate time
        if is_end_of_day:
            dt = datetime.combine(date_obj, datetime.max.time().replace(microsecond=0))
        else:
            dt = datetime.combine(date_obj, datetime.min.time())

        # Calculate epoch timestamp
        epoch_timestamp = int(dt.timestamp())

        # Format date as MM-DD-YYYY
        formatted_date = dt.strftime('%m-%d-%Y')

        # Format ISO 8601 date (jsdate)
        if is_end_of_day:
            jsdate = dt.strftime('%Y-%m-%dT23:59:59.000Z')
        else:
            jsdate = dt.strftime('%Y-%m-%dT00:00:00.000Z')

        return {
            "date": {
                "day": date_obj.day,
                "month": date_obj.month,
                "year": date_obj.year
            },
            "epoc": epoch_timestamp,
            "formatted": formatted_date,
            "jsdate": jsdate
        }

    @api.model
    def _generate_api_payload(self, start_date, end_date, page=1):
        """
        Generate the API payload with Zmall date format.

        Args:
            start_date (datetime.date): Start date for the query
            end_date (datetime.date): End date for the query
            page (int): Page number for pagination

        Returns:
            dict: Complete API payload
        """
        payload = {
            "created_by": "both",
            "start_date": self._generate_zmall_date_object(start_date, is_end_of_day=False),
            "end_date": self._generate_zmall_date_object(end_date, is_end_of_day=True),
            "order_status_id": "",
            "order_type": "both",
            "page": page,
            "payment_status": "all",
            "pickup_type": "both",
            "search_field": "user_detail.first_name",
            "search_value": ""
        }
        return payload

    def _get_api_url(self):
        """Get the API URL from system parameters."""
        api_url = self.env['ir.config_parameter'].sudo().get_param('zmall.api.url')
        if not api_url:
            raise UserError(_('Zmall API URL is not configured. Please configure it in Settings > System Parameters with key "zmall.api.url"'))
        return api_url

    def _fetch_orders_from_api(self, start_date, end_date):
        """
        Fetch orders from Zmall API.

        Args:
            start_date (datetime.date): Start date
            end_date (datetime.date): End date

        Returns:
            dict: API response or None if failed
        """
        api_url = self._get_api_url()
        payload = self._generate_api_payload(start_date, end_date)

        # Get timeout from system parameters
        timeout = int(self.env['ir.config_parameter'].sudo().get_param('zmall.api.timeout', 30))

        _logger.info(f'Fetching Zmall orders from {start_date} to {end_date}')
        _logger.debug(f'API Payload: {json.dumps(payload, indent=2)}')

        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.post(
                api_url,
                json=payload,
                headers=headers,
                timeout=timeout
            )

            response.raise_for_status()

            data = response.json()
            _logger.info(f'API Response: Success={data.get("success")}, Message={data.get("message")}, Pages={data.get("pages")}')

            return data

        except requests.exceptions.Timeout:
            error_msg = f'API request timeout after {timeout} seconds'
            _logger.error(f'Zmall API Error: {error_msg}')
            return {'error': error_msg}

        except requests.exceptions.RequestException as e:
            error_msg = f'API request failed: {str(e)}'
            _logger.error(f'Zmall API Error: {error_msg}')
            return {'error': error_msg}

        except json.JSONDecodeError as e:
            error_msg = f'Invalid JSON response: {str(e)}'
            _logger.error(f'Zmall API Error: {error_msg}')
            return {'error': error_msg}

        except Exception as e:
            error_msg = f'Unexpected error: {str(e)}'
            _logger.error(f'Zmall API Error: {error_msg}', exc_info=True)
            return {'error': error_msg}

    def _parse_and_store_orders(self, orders_data, fetch_record):
        """
        Parse API orders data and store in zmall.order model.

        Args:
            orders_data (list): List of order dictionaries from API
            fetch_record (zmall.order.fetch): The fetch record

        Returns:
            int: Number of orders stored
        """
        stored_count = 0
        zmall_order_model = self.env['zmall.order']

        for order_data in orders_data:
            try:
                # Extract customer details
                user_detail = order_data.get('user_detail', {})

                # Extract payment details
                payment_detail = order_data.get('order_payment_detail', {})

                # Extract store details
                store_detail = order_data.get('store_detail', {})

                # Extract provider details
                provider_detail = order_data.get('provider_detail', {})

                # Extract cart details for products
                cart_detail = order_data.get('cart_detail', {})
                order_details = cart_detail.get('order_details', [])

                # Prepare order values
                order_vals = {
                    'zmall_order_id': order_data.get('_id', ''),
                    'unique_id': order_data.get('unique_id', 0),
                    'order_date': order_data.get('created_at'),
                    'completed_date': order_data.get('completed_at'),
                    'order_status': order_data.get('order_status', 0),
                    'order_type': order_data.get('order_type', 0),

                    # Customer info
                    'customer_first_name': user_detail.get('first_name', ''),
                    'customer_last_name': user_detail.get('last_name', ''),
                    'customer_email': user_detail.get('email', ''),
                    'customer_phone': user_detail.get('phone', ''),
                    'customer_country_code': user_detail.get('country_phone_code', ''),

                    # Store info
                    'store_name': store_detail.get('name', ''),
                    'store_email': store_detail.get('email', ''),
                    'store_phone': store_detail.get('phone', ''),
                    'store_address': store_detail.get('address', ''),

                    # Payment info
                    'total_payment': payment_detail.get('total', 0.0),
                    'cash_payment': payment_detail.get('cash_payment', 0.0),
                    'card_payment': payment_detail.get('card_payment', 0.0),
                    'wallet_payment': payment_detail.get('wallet_payment', 0.0),
                    'payment_method': order_data.get('paid_by', ''),
                    'currency_code': payment_detail.get('currency_code', 'ETB'),
                    'is_payment_paid': payment_detail.get('is_payment_paid', False),

                    # Delivery info
                    'delivery_type': order_data.get('delivery_type', 0),
                    'delivery_price': payment_detail.get('total_delivery_price', 0.0),
                    'delivery_address': cart_detail.get('destination_addresses', [{}])[0].get('address', '') if cart_detail.get('destination_addresses') else '',

                    # Additional info
                    'order_payment_unique_id': payment_detail.get('unique_id', 0),
                    'invoice_number': payment_detail.get('invoice_number', ''),
                    'confirmation_code_pickup': order_data.get('confirmation_code_for_pick_up_delivery', 0),
                    'confirmation_code_complete': order_data.get('confirmation_code_for_complete_delivery', 0),

                    # Provider info
                    'provider_name': f"{provider_detail.get('first_name', '')} {provider_detail.get('last_name', '')}".strip(),
                    'provider_email': provider_detail.get('email', ''),
                    'provider_phone': provider_detail.get('phone', ''),

                    # Link to fetch record
                    'fetch_id': fetch_record.id,
                    'raw_data': json.dumps(order_data),
                }

                # Create order
                order_record = zmall_order_model.create(order_vals)

                # Create order items
                for idx, product_group in enumerate(order_details, 1):
                    product_name = product_group.get('product_name', '')
                    items = product_group.get('items', [])

                    for item in items:
                        item_vals = {
                            'order_id': order_record.id,
                            'sequence': idx * 10,
                            'product_name': product_name,
                            'item_name': item.get('item_name', ''),
                            'item_id': item.get('item_id', ''),
                            'product_id': product_group.get('product_id', ''),
                            'item_price': item.get('item_price', 0.0),
                            'quantity': item.get('quantity', 1),
                            'total_price': item.get('total_price', 0.0),
                            'item_tax': item.get('item_tax', 0.0),
                            'note': item.get('note_for_item', ''),
                            'specifications': json.dumps(item.get('specifications', [])),
                        }
                        self.env['zmall.order.item'].create(item_vals)

                stored_count += 1

            except Exception as e:
                _logger.error(f'Error parsing order {order_data.get("unique_id", "unknown")}: {str(e)}')
                continue

        return stored_count

    @api.model
    def fetch_daily_orders(self, target_date=None):
        """
        Fetch daily orders from Zmall API.

        Args:
            target_date (datetime.date, optional): The date to fetch. Defaults to yesterday.

        Returns:
            dict: Fetch result with status and message
        """
        if target_date is None:
            # Default to yesterday
            target_date = fields.Date.context_today(self) - timedelta(days=1)

        _logger.info(f'Starting Zmall daily order fetch for date: {target_date}')

        # Create fetch record
        fetch_record = self.create({
            'start_date': target_date,
            'end_date': target_date,
        })

        try:
            # Fetch data from API
            response_data = self._fetch_orders_from_api(target_date, target_date)

            if 'error' in response_data:
                # Handle error
                fetch_record.write({
                    'state': 'failed',
                    'success': False,
                    'error_message': response_data['error'],
                })
                _logger.error(f'Failed to fetch Zmall orders: {response_data["error"]}')
                return {
                    'status': 'error',
                    'message': response_data['error']
                }

            # Process successful response
            success = response_data.get('success', False)
            records_count = response_data.get('message', 0)  # API returns count in 'message' field
            total_pages = response_data.get('pages', 0)
            orders = response_data.get('orders', [])

            # Parse and store orders
            stored_count = 0
            if success and orders:
                stored_count = self._parse_and_store_orders(orders, fetch_record)
                _logger.info(f'Stored {stored_count} orders out of {len(orders)} returned')

            # Build summary
            api_summary = f"Success: {success}\n"
            api_summary += f"Total Records: {records_count}\n"
            api_summary += f"Total Pages: {total_pages}\n"
            api_summary += f"Orders Returned: {len(orders)}\n"
            api_summary += f"Orders Stored: {stored_count}"

            # Update fetch record
            fetch_record.write({
                'state': 'success' if success else 'failed',
                'success': success,
                'records_count': stored_count,  # Store actual stored count
                'total_pages': total_pages,
                'api_response': api_summary,
            })

            if success:
                _logger.info(f'Successfully fetched and stored {stored_count} Zmall orders for {target_date}')
                return {
                    'status': 'success',
                    'message': f'Successfully fetched and stored {stored_count} orders',
                    'records_count': stored_count,
                    'total_pages': total_pages
                }
            else:
                _logger.warning(f'API returned success=False for {target_date}')
                return {
                    'status': 'warning',
                    'message': 'API returned success=False',
                    'records_count': stored_count
                }

        except Exception as e:
            error_msg = f'Unexpected error during fetch: {str(e)}'
            _logger.error(error_msg, exc_info=True)
            fetch_record.write({
                'state': 'failed',
                'success': False,
                'error_message': error_msg,
            })
            return {
                'status': 'error',
                'message': error_msg
            }

    @api.model
    def cron_fetch_daily_orders(self):
        """
        Scheduled action to fetch daily orders.
        Runs daily at 2 AM to fetch previous day's data.
        """
        _logger.info('Zmall daily order fetch cron job started')
        result = self.fetch_daily_orders()
        _logger.info(f'Zmall daily order fetch cron job completed: {result}')
        return result

    def action_manual_fetch(self):
        """Manual fetch action from UI."""
        self.ensure_one()
        result = self.fetch_daily_orders(target_date=self.start_date)

        if result['status'] == 'success':
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': result['message'],
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Error'),
                    'message': result['message'],
                    'type': 'danger',
                    'sticky': True,
                }
            }
