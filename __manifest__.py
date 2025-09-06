# -*- coding: utf-8 -*-
{
    'name': 'Car Service Manager',
    'version': '18.0.1.0.0',
    'summary': 'Manage cars, mechanics, service types, and service orders',
    'description': 'Module to manage car maintenance services, including mechanics and service orders.',
    'category': 'Services',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': ['base', 'om_account_accountant', 'mail'],
    'data': [
        'security/security.xml',
        'data/car_service_sequence.xml',
        'views/car_service_views.xml',
        'views/car_mechanic_views.xml',
        'views/car_service_type_views.xml',
        'views/car_service_order_views.xml',
        'views/car_service_menu.xml',
        'report/car_service_order_report.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
