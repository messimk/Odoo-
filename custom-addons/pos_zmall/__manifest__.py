# -*- coding: utf-8 -*-
{
    'name': "pos_zmall",
    'version': '1.0.0',
    'license': 'LGPL-3',
    'summary': "Integration of Zmall with Odoo Point of Sale",
    'description': """
        Zmall integration for Odoo POS.
    """,
    'author': "Biniyam Seid /ETTA",
    'website': "https://www.yourcompany.com",
    'category': 'Sales/Point of Sale',
    'sequence': 7,
    'depends': ['base', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_zmall/static/src/app/**/*',
        ],
    },
}



