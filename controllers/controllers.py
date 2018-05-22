# -*- coding: utf-8 -*-
from odoo import http

# class OauthProvider(http.Controller):
#     @http.route('/oauth_provider/oauth_provider/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/oauth_provider/oauth_provider/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('oauth_provider.listing', {
#             'root': '/oauth_provider/oauth_provider',
#             'objects': http.request.env['oauth_provider.oauth_provider'].search([]),
#         })

#     @http.route('/oauth_provider/oauth_provider/objects/<model("oauth_provider.oauth_provider"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oauth_provider.object', {
#             'object': obj
#         })