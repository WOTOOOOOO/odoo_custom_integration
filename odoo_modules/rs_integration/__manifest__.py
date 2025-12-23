{
    'name': 'RS.ge Integration',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Submit invoices to RS.ge',
    'description': """
        Integration with RS.ge for electronic invoice submission.
        - Adds RS.ge status tracking to invoices
        - Generates and signs XML documents
        - Submits invoices to RS.ge API
    """,
    'author': 'The Company',
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
