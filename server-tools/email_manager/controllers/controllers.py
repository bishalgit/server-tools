# -*- coding: utf-8 -*-
from odoo import http

# class EmailManager(http.Controller):
#     @http.route('/email_manager/email_manager/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/email_manager/email_manager/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('email_manager.listing', {
#             'root': '/email_manager/email_manager',
#             'objects': http.request.env['email_manager.email_manager'].search([]),
#         })

#     @http.route('/email_manager/email_manager/objects/<model("email_manager.email_manager"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('email_manager.object', {
#             'object': obj
#         })