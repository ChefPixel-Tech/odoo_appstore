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

from odoo import models, fields, api
import requests
import json
import time

class ChatbotWizard(models.TransientModel):
    _name = 'chatbot.wizard'
    _description = 'Interface modale pour le chatbot MCP'

    user_input = fields.Text(string='Votre message', required=True, placeholder="Posez votre question au chatbot...")
    bot_response = fields.Html(string='Réponse du chatbot', readonly=True)
    previous_user_message = fields.Text(string='Message utilisateur précédent', readonly=True)
    config_id = fields.Many2one('chatbot.config', string='Configuration', readonly=True)
    
    # Champs de configuration quick
    show_config = fields.Boolean(string='Afficher configuration', default=False)
    show_history = fields.Boolean(string='Afficher historique', default=False)
    anthropic_api_key = fields.Char(string='Clé API Anthropic', password=True)
    mcp_url = fields.Char(string='URL MCP Gradio')
    
    # Nouveaux champs pour l'historique
    conversation_history = fields.One2many(
        'chatbot_custom.message', 
        compute='_compute_conversation_history',
        string='Historique des conversations'
    )
    current_session_id = fields.Char(string='Session ID courante')
    
    @api.depends('current_session_id')
    def _compute_conversation_history(self):
        """Calculer l'historique des conversations pour l'utilisateur actuel"""
        for wizard in self:
            history = self.env['chatbot_custom.message'].search([
                ('user_id', '=', self.env.user.id)
            ], limit=15, order='timestamp desc')
            wizard.conversation_history = history
    
    @api.model
    def default_get(self, fields_list):
        """Récupérer la configuration active par défaut"""
        defaults = super().default_get(fields_list)
        config = self.env['chatbot.config'].search([('is_active', '=', True)], limit=1)
        if config:
            defaults['config_id'] = config.id
            defaults['anthropic_api_key'] = config.anthropic_api_key
            defaults['mcp_url'] = config.mcp_url
        
        # Générer un ID de session pour cette instance
        defaults['current_session_id'] = self._generate_session_id()
        return defaults
    
    @api.model
    def _generate_session_id(self):
        """Générer un ID de session unique"""
        import uuid
        return str(uuid.uuid4())[:12]
    
    def action_send_message(self):
        """Envoyer le message au chatbot et afficher la réponse"""
        if not self.user_input:
            return
        
        start_time = time.time()
        
        # Sauvegarder le message utilisateur pour l'affichage dans la conversation
        self.previous_user_message = self.user_input
        
        # Récupérer ou créer la configuration
        config = self._get_or_create_config()
        
        if not config:
            self.bot_response = "❌ Configuration manquante"
            # Vider le champ user_input après traitement
            self.user_input = ""
            return self._return_wizard()

        # Créer l'enregistrement du message avec le bon session_id
        message = self.env['chatbot_custom.message'].create({
            'user_input': self.previous_user_message,  # Utiliser le message sauvegardé
            'timestamp': fields.Datetime.now(),
            'session_id': self.current_session_id,
            'status': 'sent',
            'config_used': config.id
        })
        
        try:
            # Utiliser le service Anthropic
            anthropic_service = self.env['anthropic.service']
            bot_response = anthropic_service.call_anthropic_api(self.previous_user_message, config)  # Utiliser le message sauvegardé
            
            # Calculer le temps de réponse
            response_time = time.time() - start_time
            
            # Mettre à jour avec la vraie réponse
            message.write({
                'bot_response': bot_response,
                'status': 'processed',
                'response_time': response_time
            })
            
            self.bot_response = self._format_response(bot_response, response_time)
            
        except Exception as e:
            error_msg = f"❌ Erreur: {str(e)}"
            message.write({
                'bot_response': error_msg,
                'status': 'error',
                'error_message': str(e),
                'response_time': time.time() - start_time
            })
            self.bot_response = self._format_error_message(str(e))
        
        # Vider le champ user_input après traitement du message
        self.user_input = ""
        
        return self._return_wizard()
    
    def _format_error_message(self, error):
        """Formater un message d'erreur"""
        return f"""
        <div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; border-radius: 8px;">
            <h5>❌ Erreur de traitement</h5>
            <p><strong>Détails :</strong> {error}</p>
            <p><strong>Solutions possibles :</strong></p>
            <ul>
                <li>Vérifiez votre configuration MCP</li>
                <li>Assurez-vous que le serveur Gradio est accessible</li>
                <li>Vérifiez votre clé API Anthropic</li>
            </ul>
        </div>
        """
    
    def action_toggle_config(self):
        """Basculer l'affichage de la configuration"""
        self.show_config = not self.show_config
        return self._return_wizard()
    
    def action_toggle_history(self):
        """Basculer l'affichage de l'historique"""
        self.show_history = not self.show_history
        return self._return_wizard()
    
    def action_save_config(self):
        """Sauvegarder la configuration rapide"""
        if self.anthropic_api_key or self.mcp_url:
            config = self.env['chatbot.config'].search([('is_active', '=', True)], limit=1)
            if not config:
                config = self.env['chatbot.config'].create({
                    'name': 'Configuration Chatbot',
                    'is_active': True
                })
            
            vals = {}
            if self.anthropic_api_key:
                vals['anthropic_api_key'] = self.anthropic_api_key
            if self.mcp_url:
                vals['mcp_url'] = self.mcp_url
            
            if vals:
                config.write(vals)
                self.config_id = config.id
                
        self.show_config = False
        return self._return_wizard()
    
    def action_load_history_message(self):
        """Charger un message depuis l'historique"""
        # Cette méthode sera appelée via JavaScript pour charger un message spécifique
        message_id = self.env.context.get('message_id')
        if message_id:
            message = self.env['chatbot_custom.message'].browse(message_id)
            if message.exists():
                self.user_input = message.user_input
                self.bot_response = message.bot_response
        return self._return_wizard()
    
    @api.model
    def process_message_api(self, user_message):
        """API pour traiter un message (utilisée par JavaScript)"""
        config = self.env['chatbot.config'].search([('is_active', '=', True)], limit=1)
        if not config:
            return "❌ Configuration manquante"
        
        try:
            anthropic_service = self.env['anthropic.service']
            return anthropic_service.call_anthropic_api(user_message, config)
        except Exception as e:
            return f"❌ Erreur: {str(e)}"
    
    def _get_or_create_config(self):
        """Récupérer ou créer la configuration"""
        if self.config_id:
            return self.config_id
        
        # Chercher une config active
        config = self.env['chatbot.config'].search([('is_active', '=', True)], limit=1)
        if config:
            return config
        
        # Créer une config temporaire si on a les paramètres
        if self.anthropic_api_key:
            config = self.env['chatbot.config'].create({
                'name': 'Configuration Temporaire',
                'anthropic_api_key': self.anthropic_api_key,
                'mcp_url': self.mcp_url or '',
                'is_active': True
            })
            self.config_id = config.id
            return config
        
        return False
    
    def _format_response(self, response, response_time=None):
        """Formater la réponse pour l'affichage HTML"""
        if not response:
            return ""
        
        # Convertir les sauts de ligne en <br/>
        formatted = response.replace('\n', '<br/>')
        
        # Convertir le markdown basique en HTML
        import re
        formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
        formatted = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted)
        formatted = re.sub(r'`(.*?)`', r'<code>\1</code>', formatted)
        
        # Ajouter des statistiques de performance si disponibles
        footer = ""
        if response_time:
            footer = f"""
            <div style="margin-top: 15px; padding: 10px; background: #f8f9fa; border-radius: 6px; font-size: 12px; color: #6c757d;">
                ⚡ Réponse générée en {response_time:.2f}s • 🤖 Assistant MCP Odoo
            </div>
            """
        
        return f"<div>{formatted}</div>{footer}"
    
    def _return_wizard(self):
        """Retourner le wizard en mode modal"""
        return {
            'type': 'ir.actions.act_window',
            'name': '🤖 Assistant Chatbot MCP',
            'res_model': 'chatbot.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }
    
    def action_clear_conversation(self):
        """Effacer la conversation"""
        self.user_input = ""
        self.bot_response = ""
        self.current_session_id = self._generate_session_id()
        return self._return_wizard()
    
    def action_open_config(self):
        """Ouvrir la configuration complète"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Configuration Chatbot',
            'res_model': 'chatbot.config',
            'view_mode': 'list,form',
            'target': 'current',
        } 
