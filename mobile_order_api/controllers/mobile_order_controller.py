# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class MobileOrderAPIController(http.Controller):
    """Mobile Order API - Fetch user's sales orders"""

    # COMMENTED OUT - JWT Token Authentication (will be enabled later)
    # def _get_user_from_token(self):
    #     """
    #     Extract and authenticate user from JWT Bearer token
    #
    #     Returns:
    #         res.users record
    #
    #     Raises:
    #         ValidationError: If token is invalid or expired
    #     """
    #     auth_header = request.httprequest.headers.get('Authorization', '')
    #
    #     if not auth_header.startswith('Bearer '):
    #         raise ValidationError('Missing or invalid authorization header')
    #
    #     access_token = auth_header.replace('Bearer ', '').strip()
    #
    #     # Verify token and get user
    #     jwt_manager = request.env['jwt.manager'].sudo()
    #     user = jwt_manager.get_user_from_token(access_token)
    #
    #     if not user:
    #         raise ValidationError('Invalid or expired token')
    #
    #     return user

    @http.route('/api/v1/mobile/orders/my-orders', type='json', auth='public', methods=['POST'], csrf=False)
    def get_my_orders(self, **kwargs):
        """
        Fetch sales orders for user with optional status filtering

        TEMPORARY: Using user_id from request body (JWT token authentication commented out)

        Request Body:
        {
            "user_id": 123,               # REQUIRED - user ID
            "status": "sale",             # single status OR
            "status": ["sale", "done"],   # multiple statuses
            "limit": 20,                  # default 50
            "offset": 0                   # for pagination
        }

        Examples:
        ---------
        1. Get all orders:
           Body: {"user_id": 123}

        2. Get orders by single status:
           Body: {"user_id": 123, "status": "sale"}

        3. Get orders by multiple statuses:
           Body: {"user_id": 123, "status": ["sale", "done"]}

        4. Get with pagination:
           Body: {"user_id": 123, "status": "sale", "limit": 10, "offset": 0}
        """
        try:
            # TEMPORARY: Get user from user_id in request body
            # (JWT token authentication is commented out)
            user_id = kwargs.get('user_id')

            if not user_id:
                return {
                    "success": False,
                    "error": "user_id is required in request body",
                    "code": "MISSING_USER_ID"
                }

            # Fetch user by user_id
            current_user = request.env['res.users'].sudo().browse(int(user_id))

            if not current_user.exists():
                return {
                    "success": False,
                    "error": f"User with ID {user_id} not found",
                    "code": "USER_NOT_FOUND"
                }

            # COMMENTED OUT - JWT Token Authentication
            # current_user = self._get_user_from_token()
            #
            # # Optional: validate user_id from body matches token user
            # user_id = kwargs.get('user_id')
            # if user_id and int(user_id) != current_user.id:
            #     return {
            #         "success": False,
            #         "error": "User ID does not match authenticated token",
            #         "code": "AUTH_MISMATCH"
            #     }

            partner = current_user.partner_id

            if not partner:
                return {
                    "success": False,
                    "error": "User not authenticated or has no partner",
                    "code": "AUTH_ERROR"
                }

            # Build domain to fetch ONLY this user's orders
            domain = [('partner_id', '=', partner.id)]

            # Filter by status if provided
            status_filter = kwargs.get('status')
            if status_filter:
                if isinstance(status_filter, list):
                    domain.append(('state', 'in', status_filter))
                else:
                    domain.append(('state', '=', status_filter))

            # Pagination
            limit = kwargs.get('limit', 50)
            offset = kwargs.get('offset', 0)

            # Fetch orders - sudo() to read order details
            orders = request.env['sale.order'].sudo().search(
                domain,
                order='date_order desc',
                limit=limit,
                offset=offset
            )

            total_count = request.env['sale.order'].sudo().search_count(domain)

            _logger.info(f"User {current_user.login} fetched {len(orders)} orders (filter: {status_filter})")

            return {
                "success": True,
                "user": current_user.login,
                "partner": partner.name,
                "total": total_count,
                "count": len(orders),
                "offset": offset,
                "limit": limit,
                "has_more": (offset + len(orders)) < total_count,
                "status_filter": status_filter if status_filter else "all",
                "orders": [self._serialize_order(order) for order in orders]
            }

        except ValidationError as e:
            _logger.warning(f"Authentication error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "code": "AUTH_ERROR"
            }
        except Exception as e:
            _logger.error(f"Error fetching orders: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "code": "SERVER_ERROR"
            }

    def _serialize_order(self, order):
        """Convert sale.order to JSON-friendly dict"""
        return {
            "id": order.id,
            "name": order.name,
            "state": order.state,
            "state_label": dict(order._fields['state'].selection).get(order.state, order.state),
            "partner_id": order.partner_id.id,
            "partner_name": order.partner_id.name,
            "date_order": order.date_order.isoformat() if order.date_order else None,
            "amount_untaxed": order.amount_untaxed,
            "amount_tax": order.amount_tax,
            "amount_total": order.amount_total,
            "currency": order.currency_id.name,
            "order_line_count": len(order.order_line),
            "create_date": order.create_date.isoformat() if order.create_date else None,
        }
