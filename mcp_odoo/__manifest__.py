# -*- coding: utf-8 -*-
#
#  ┌───────────────────────────────────────────────────────────────┐
#  │   Developed by: CHEF PIXEL                                    │
#  │   Website: https://chef-pixel.fr                              │
#  │   Support: hello@chef-pixel.fr                                │
#  │   Description: Chatbot Odoo Integration with MCP Gradio       │
#  └───────────────────────────────────────────────────────────────┘
#
#  🤖 Enables chatbot messaging with Anthropic API via Gradio (MCP)

{
    "name": "Chatbot Custom MCP",
    "version": "18.0.2.0.0",
    "summary": "Base module for a custom Odoo chatbot using MCP Gradio",
    "description": """
        Chatbot Custom MCP
        ==================

        Provides message management and chatbot features using the Anthropic API 
        integrated through the MCP Gradio platform.

        Key Features
        ------------
        - Custom chatbot integration with Anthropic API
        - Gradio interface for live interactions
        - Wizard support for message flow
        - Backend views to manage chatbot messages

        Ideal for:
        - Businesses implementing AI-driven chat support
        - Developers integrating external LLM APIs with Odoo
    """,
    "author": "CHEF PIXEL",
    "maintainer": "CHEF PIXEL",
    "support": "hello@chef-pixel.fr",
    "company": "CHEF PIXEL",
    "website": "https://chef-pixel.fr",
    "category": "Tools",
    "license": "LGPL-3",
    "version": "18.0.2.0.0",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/chatbot_v18.xml",
        "views/chatbot_messages.xml",
        "wizard/chatbot_wizard_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mcp_odoo/static/src/scss/chatbot_modal.scss",
            "mcp_odoo/static/src/js/chatbot_widget.js",
        ],
    },
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
    "auto_install": False
}
