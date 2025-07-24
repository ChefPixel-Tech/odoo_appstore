# -*- coding: utf-8 -*-
#
#  ┌────────────────────────────────────────────────────────────────────┐
#  │   Developed by: CHEF PIXEL                                         │
#  │   Website: https://chef-pixel.fr                                   │
#  │   Support: hello@chef-pixel.fr                                     │
#  │   Description: Show delivery numbers on invoices product-wise      │
#  └────────────────────────────────────────────────────────────────────┘
#
#  📦 Improve traceability by linking deliveries with invoice lines!

{
    "name": "Display Delivery Number on the Invoice",
    "version": "17.0.1.0.0",
    "summary": "Display delivery numbers per product on customer invoices",
    "description": """
        Display Delivery Number on the Invoice
        ======================================

        This module enhances the invoice view by showing delivery (picking)
        numbers associated with each product line. It improves traceability 
        between sales, stock movements, and accounting documents.

        Key Features
        ------------
        - Display related delivery numbers on invoice lines
        - Improve visibility of logistics in accounting
        - Adds cross-reference between delivery and invoicing

        Ideal for:
        - Companies with multiple deliveries per invoice
        - Warehouses and accounting teams working closely
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
