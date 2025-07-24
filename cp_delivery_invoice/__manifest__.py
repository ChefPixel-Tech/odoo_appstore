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

{
    "name": "Display Delivery Number on the Invoice",
    "version": "18.0.1.0.0",
    "summary": "Shows delivery numbers per product on invoices",
    "description": """
        Display Delivery Number on the Invoice
        ======================================

        This module adds visibility of related delivery numbers for each 
        invoiced product, enhancing traceability between sales, deliveries, 
        and billing.

        Key Features
        ------------
        - Display delivery (picking) numbers on invoice lines
        - Improve auditability of logistics in the accounting process
        - Adds useful information for warehouse, sales, and finance teams

        Ideal for:
        - Companies managing high volumes of deliveries
        - Businesses needing improved delivery-to-invoice traceability
        - Users who require logistics data in accounting documents
    """,
    "author": "CHEF PIXEL",
    "maintainer": "CHEF PIXEL",
    "company": "CHEF PIXEL",
    "website": "https://chef-pixel.fr",
    "support": "hello@chef-pixel.fr",
    "category": "Extra Tools",
    "license": "LGPL-3",
    "depends": ["sale", "account", "sale_stock", "stock"],
    "data": [
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
    "auto_install": False
}
