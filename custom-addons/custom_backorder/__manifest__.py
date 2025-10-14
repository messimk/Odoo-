{
    'name': 'Custom Backorder Management',
    'version': '1.0',
    'summary': 'Custom backorder confirmation in Odoo 17',
    'description': 'Adds a custom backorder confirmation wizard with Create Backorder and No Backorder options for internal transfers.',
    'category': 'Inventory',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/backorder_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}