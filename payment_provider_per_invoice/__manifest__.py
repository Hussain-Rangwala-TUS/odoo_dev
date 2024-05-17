{
    'name': 'Payment Provider per Invoice',
    'author': 'TechUltra Solutions Pvt. Ltd.',
    'website': 'https://techultrasolutions.com',
    'license': 'OPL-1',
    'version': '16.0.1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 5,
    'summary': 'Select different payment provider for each invoice',
    'depends': ['account_payment','account','payment'],
    'data': [
        'views/account_move_views.xml',
        'views/res_config_setting.xml',
        'views/payment_provider.xml',
    ],

    'application': True,
    'installable': True,
}
