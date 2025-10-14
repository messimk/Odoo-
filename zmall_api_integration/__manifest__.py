# -*- coding: utf-8 -*-
{
    'name': 'Zmall API Integration',
    'version': '18.0.1.0.0',
    'category': 'Integration',
    'summary': 'Fetch daily order data from Zmall API',
    'description': """
        Zmall API Integration Module
        =============================
        This module fetches daily order data from the Zmall API and stores statistics.

        Features:
        ---------
        * Automatic daily data fetching via scheduled action (cron job)
        * Configurable API URL through system parameters
        * Automatic JSON payload generation with Zmall date format
        * Order statistics tracking
        * Comprehensive logging for success and failures
        * Manual fetch capability
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_config_parameter_data.xml',
        'data/ir_cron_data.xml',
        'views/zmall_order_views.xml',
        'views/zmall_order_fetch_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
