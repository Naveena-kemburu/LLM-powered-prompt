#!/usr/bin/env python3
"""
LLM-Powered Prompt Router - Main Application
"""
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from router import process_message
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route('/classify', methods=['POST'])
def classify():
    """
    Endpoint to process a user message through the routing pipeline.
    
    Expected JSON body:
    {
        "message": "user message here"
    }
    
    Returns:
    {
        "intent": "code|data|writing|career|unclear",
        "confidence": 0.0-1.0,
        "response": "generated response"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field in request body"}), 400
        
        message = data['message']
        
        if not message or not message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Process the message
        result = process_message(message)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/batch', methods=['POST'])
def batch_classify():
    """
    Endpoint to process multiple messages in batch.
    
    Expected JSON body:
    {
        "messages": ["message1", "message2", ...]
    }
    
    Returns:
    {
        "results": [
            {"intent": "...", "confidence": ..., "response": "..."},
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({"error": "Missing 'messages' field in request body"}), 400
        
        messages = data['messages']
        
        if not isinstance(messages, list):
            return jsonify({"error": "'messages' must be a list"}), 400
        
        results = []
        for message in messages:
            if message and message.strip():
                result = process_message(message)
                results.append(result)
        
        return jsonify({"results": results}), 200
        
    except Exception as e:
        logger.error(f"Error processing batch request: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Verify API key is set based on provider
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "groq":
        if not os.getenv("GROQ_API_KEY"):
            logger.error("GROQ_API_KEY environment variable is not set!")
            logger.info("Get your free key at: https://console.groq.com")
            exit(1)
    else:
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OPENAI_API_KEY environment variable is not set!")
            exit(1)
    
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
