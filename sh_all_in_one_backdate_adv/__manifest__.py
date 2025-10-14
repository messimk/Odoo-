# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'All In One Backdate - Advance | Inventory Backdate',
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    'support': 'support@softhealer.com',
    'category': 'Extra Tools',
    'summary': 'Backdate for Inventory Operations - Stock Picking, Scrap, and Adjustments',
    'description': 'Module for backdating inventory operations with remarks and mass assignment capabilities.',
    'version': '17.0.1.0.0',
    'depends': ['stock_account'],
    'data': [
        'sh_stock_backdate/security/ir.model.access.csv',
        'sh_stock_backdate/security/backdate_security.xml',
        'sh_stock_backdate/wizard/picking_backdate_wizard.xml',
        'sh_stock_backdate/wizard/scrap_backdate_wizard.xml',
        # 'sh_stock_backdate/wizard/adjustment_backdate_wizard.xml',  # Removed - stock.inventory doesn't exist in Odoo 17
        'sh_stock_backdate/views/stock_config_settings.xml',
        'sh_stock_backdate/views/stock_picking.xml',
        'sh_stock_backdate/views/stock_move.xml',
        # 'sh_stock_backdate/views/stock_inventory.xml',  # Removed - stock.inventory doesn't exist in Odoo 17
        'sh_stock_backdate/views/stock_scrap.xml',
        'sh_stock_backdate/views/stock_move_line.xml',
        'sh_stock_backdate/views/stock_backdate_multi_action.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
    'images': ['static/description/background.png'],
    'license': 'OPL-1',
    # 'price': 100,
    # 'currency': 'EUR'
}