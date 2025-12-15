# -*- coding: utf-8 -*-
{
    'name': 'Mobile Order API',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'REST API - Fetch User Sales Orders by Status',
    'description': """
        Mobile Order API
        ================

        Simple REST API for mobile applications to fetch sales orders.

        Features:
        ---------
        * Fetch logged-in user's sales orders
        * Filter by status (draft, sent, sale, cancel)
        * Filter by single or multiple statuses
        * Pagination support
        * User isolation (each user sees only their orders)

        API Endpoint:
        -------------
        POST /api/v1/mobile/orders/my-orders

        Usage Examples:
        ---------------
        1. Get all orders: {}
        2. Filter by status: {"status": "sale"}
        3. Multiple statuses: {"status": ["sale", "done"]}
        4. With pagination: {"status": "sale", "limit": 10, "offset": 0}
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
