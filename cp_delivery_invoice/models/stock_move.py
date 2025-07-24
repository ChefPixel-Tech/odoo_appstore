# -*- coding: utf-8 -*-
#
#  ┌────────────────────────────────────────────────────────────────────┐
#  │   Developed by: CHEF PIXEL                                         │
#  │   Website: https://chef-pixel.fr                                   │
#  │   Support: hello@chef-pixel.fr                                     │
#  │   Description: Show delivery numbers on invoices product-wise      │
#  └────────────────────────────────────────────────────────────────────┘
#
#  📦 Link deliveries with invoice lines for better traceability!

from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    is_invoiced = fields.Boolean(string="Is Invoiced", default=False, copy=False)
