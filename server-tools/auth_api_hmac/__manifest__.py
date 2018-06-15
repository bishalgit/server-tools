# -*- coding: utf-8 -*-

{
    'name': 'Authenticate API - JWT',
    'summary': 'Verifies API request with keys provided by JWT',
    'version': '11.0.2.0',
    'category': 'Authentication',
    'website': 'https://bishalgit.github.io/server-tools/',
    'author': 'Bishal Pun',
    'license': 'AGPL-3',
    'installable': True,
    'external_dependencies': {
        'python': [
            'jwt',
            'cryptography',
        ],
    },
    'depends': [
        'oauth_provider',
        'oauth_provider_jwt',
    ],
    'data': [
        'views/oauth_provider_client.xml',
    ],
}
