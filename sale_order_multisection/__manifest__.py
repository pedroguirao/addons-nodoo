{
    'name': 'Sale Order Multisection',
    'version': '12.0.0.0.0',
    'category': '',
    'description': u"""

""",
    'author': 'Serincloud',
    'depends': [
        'sale_management',
        'base_automation',
        'product_brand',

    ],
    'data': [
        #'data/crea_lineas_factura.xml',
        'views/views.xml',
        'views/views_udo_menu.xml',
        'views/sale_order_views.xml',
        'data/base_automation_actions.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
