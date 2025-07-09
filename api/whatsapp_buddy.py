# WhatsApp ZAI Buddy - Mobile AI Assistant
"""
 ZAI WhatsApp Buddy - Your AI brother on mobile!
Connects WhatsApp Business API to ZAI brain for mobile assistance
"""

import asyncio
import json
import hashlib
import hmac
import os
from flask import Flask, request, jsonify
from datetime import datetime
import logging
import aiohttp

# Import our ZAI brain
try:
    from services.zai_orchestration_core import ZaiOrchestrationEngine
    from services.zai_memory_system import ZaiMemoryManager
    from services.zai_model_manager import ZaiModelManager
except ImportError:
    print(" ZAI services not found - make sure you're in the backend directory")

logger = logging.getLogger(__name__)

class WhatsAppZaiBuddy:
    """Your AI buddy that lives in WhatsApp!"""
    
    def __init__(self):
        self.verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN', 'zai_buddy_verify_123')
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.app_secret = os.getenv('WHATSAPP_APP_SECRET')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.authorized_numbers = os.getenv('AUTHORIZED_WHATSAPP_NUMBERS', '').split(',')
        
        # Initialize ZAI brain components (lazy loading)
        self.memory_manager = None
        self.model_manager = None
        self.zai_orchestrator = None
        
        # Mobile-optimized settings
        self.mobile_mode = True
        self.max_response_length = 1000  # Keep messages readable on mobile
        
    async def initialize_zai_brain(self):
        """Initialize the ZAI orchestration system"""
        try:
            # Initialize components if not already done
            if self.memory_manager is None:
                self.memory_manager = ZaiMemoryManager()
            if self.model_manager is None:
                self.model_manager = ZaiModelManager()
                
            # Initialize orchestrator
            if self.zai_orchestrator is None:
                self.zai_orchestrator = ZaiOrchestrationEngine(
                    self.memory_manager, 
                    self.model_manager
                )
            logger.info("🧠 ZAI brain connected to WhatsApp buddy!")
        except Exception as e:
            logger.error(f"Failed to initialize ZAI brain: {e}")
    
    def verify_webhook(self, mode, token, challenge):
        """Verify WhatsApp webhook"""
        if mode == "subscribe" and token == self.verify_token:
            logger.info(" WhatsApp webhook verified!")
            return challenge
        else:
            logger.warning(" WhatsApp webhook verification failed")
            return None
    
    def verify_signature(self, payload, signature):
        """Verify webhook signature for security"""
        if not self.app_secret:
            return True  # Skip if no secret configured
            
        expected_signature = hmac.new(
            self.app_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    def is_authorized_number(self, phone_number):
        """Check if phone number is authorized to use the buddy"""
        if not self.authorized_numbers or self.authorized_numbers == ['']:
            return True  # Allow all if no restrictions set
        return phone_number in self.authorized_numbers
    
    async def send_whatsapp_message(self, to_number, message):
        """Send message via WhatsApp Business API"""
        if not self.access_token or not self.phone_number_id:
            logger.error(" WhatsApp credentials not configured")
            return False
            
        url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Mobile-optimized message format
        formatted_message = self.format_for_mobile(message)
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {
                "body": formatted_message
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        logger.info(f" Message sent to {to_number}")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f" Failed to send message: {error_text}")
                        return False
        except Exception as e:
            logger.error(f" Error sending WhatsApp message: {e}")
            return False
    
    def format_for_mobile(self, message):
        """Format AI response for mobile reading"""
        # Remove excessive emojis and formatting for mobile
        if len(message) > self.max_response_length:
            message = message[:self.max_response_length] + "...\n\n💬 Ask me to continue for more!"
        
        # Add mobile-friendly formatting
        if "```" in message:
            # Convert code blocks to simpler format
            message = message.replace("```", "\n--- CODE ---\n")
        
        return message
    
    async def process_whatsapp_message(self, webhook_data):
        """Process incoming WhatsApp message through ZAI brain"""
        try:
            # Extract message data
            entry = webhook_data.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            
            if 'messages' not in value:
                return  # Not a message event
                
            message_data = value['messages'][0]
            contacts = value.get('contacts', [{}])[0]
            
            # Extract message details
            from_number = message_data.get('from')
            user_name = contacts.get('profile', {}).get('name', 'WhatsApp User')
            message_text = message_data.get('text', {}).get('body', '')
            message_id = message_data.get('id')
            
            # Security check
            if not self.is_authorized_number(from_number):
                await self.send_whatsapp_message(
                    from_number, 
                    "🚫 Sorry, you're not authorized to use this AI buddy. Contact Nathan for access!"
                )
                return
            
            logger.info(f" Message from {user_name} ({from_number}): {message_text}")
            
            # Process through ZAI brain
            if not self.zai_orchestrator:
                await self.initialize_zai_brain()
            
            # Add mobile context to the request
            mobile_context = {
                'platform': 'whatsapp',
                'mobile_mode': True,
                'user_name': user_name,
                'phone_number': from_number,
                'response_format': 'mobile'
            }
            
            # Get AI response
            zai_response = await self.zai_orchestrator.process_user_request(
                message=message_text,
                user_id=f"whatsapp_{from_number}",
                context_hints=mobile_context
            )
            
            # Send response back to WhatsApp
            if zai_response.get('success', False):
                ai_message = zai_response.get('content', 'I had a thought but it escaped me! ')
                await self.send_whatsapp_message(from_number, ai_message)
                
                # Save the interaction
                await self.memory_manager.save_conversation(
                    agent_id='whatsapp_buddy',
                    user_id=f"whatsapp_{from_number}",
                    content=f"User: {message_text}\nZAI: {ai_message}",
                    role='conversation',
                    metadata={
                        'platform': 'whatsapp',
                        'user_name': user_name,
                        'message_id': message_id
                    }
                )
            else:
                # Error fallback
                error_message = " I'm having a moment! Try asking me again in a different way?"
                await self.send_whatsapp_message(from_number, error_message)
                
        except Exception as e:
            logger.error(f" Error processing WhatsApp message: {e}")
            # Send friendly error message
            if 'from_number' in locals():
                await self.send_whatsapp_message(
                    from_number, 
                    " Oops! I had a glitch. Nathan's teaching me to be more reliable! Try again?"
                )

# Flask app for webhook
app = Flask(__name__)
buddy = WhatsAppZaiBuddy()

@app.route('/webhook/whatsapp', methods=['GET', 'POST'])
async def whatsapp_webhook():
    """WhatsApp webhook endpoint"""
    
    if request.method == 'GET':
        # Webhook verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        verification_result = buddy.verify_webhook(mode, token, challenge)
        if verification_result:
            return verification_result, 200
        else:
            return 'Forbidden', 403
    
    elif request.method == 'POST':
        # Process incoming message
        signature = request.headers.get('X-Hub-Signature-256', '')
        
        if not buddy.verify_signature(request.data, signature):
            logger.warning(" Invalid webhook signature")
            return 'Forbidden', 403
        
        webhook_data = request.get_json()
        
        # Process message asynchronously
        asyncio.create_task(buddy.process_whatsapp_message(webhook_data))
        
        return 'OK', 200

@app.route('/buddy/status')
def buddy_status():
    """Check if WhatsApp buddy is alive"""
    status = {
        'status': 'online',
        'buddy_name': 'ZAI WhatsApp Buddy',
        'capabilities': [
            'Chat and conversation',
            'Web browsing and research',
            'Code assistance',
            'Memory and context',
            'Mobile-optimized responses'
        ],
        'connected_to_zai_brain': buddy.zai_orchestrator is not None,
        'whatsapp_configured': bool(buddy.access_token and buddy.phone_number_id),
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(status)

if __name__ == '__main__':
    print(" Starting ZAI WhatsApp Buddy...")
    print(" Your AI brother is getting ready for mobile!")
    app.run(host='0.0.0.0', port=5001, debug=True)
