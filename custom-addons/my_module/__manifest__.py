{
    'name': 'My module',
    'version': '1.0',
    'license': 'LGPL-3',
    'sequence': -1002,
    'summary': 'Manage the lifecycle of physical assets assigned to employees',
    'author': 'Meseret Mekuriyaw',
    'category': 'Sales',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'my_module/static/src/components/example/example.xml',
            'my_module/static/src/components/example/example.js',
        ],
    },
    'installable': True,
    'application': False,
}
