# -*- coding: utf-8 -*-
# from odoo import http


# class Despacho(http.Controller):
#     @http.route('/despacho/despacho', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/despacho/despacho/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('despacho.listing', {
#             'root': '/despacho/despacho',
#             'objects': http.request.env['despacho.despacho'].search([]),
#         })

#     @http.route('/despacho/despacho/objects/<model("despacho.despacho"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('despacho.object', {
#             'object': obj
#         })
