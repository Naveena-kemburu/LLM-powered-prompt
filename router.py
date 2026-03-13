import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS, CLASSIFIER_PROMPT

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine which LLM provider to use
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

# Initialize the appropriate client
if LLM_PROVIDER == "groq":
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    DEFAULT_MODEL = "llama-3.3-70b-versatile"
else:  # default to openai
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    DEFAULT_MODEL = "gpt-3.5-turbo"

LOG_FILE = "route_log.jsonl"


def classify_intent(message: str) -> Dict[str, Any]:
    """
    Classify the user's intent using an LLM.
    
    Args:
        message: The user's input message
        
    Returns:
        A dictionary with 'intent' and 'confidence' keys
    """
    try:
        # Format the classifier prompt with the user message
        prompt = CLASSIFIER_PROMPT.format(message=message)
        
        # Make API call to classify intent
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", DEFAULT_MODEL),
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent classification
            max_tokens=100
        )
        
        # Extract the response content
        content = response.choices[0].message.content.strip()
        logger.info(f"Classifier raw response: {content}")
        
        # Parse JSON response
        try:
            result = json.loads(content)
            
            # Validate the structure
            if "intent" not in result or "confidence" not in result:
                logger.warning("Invalid JSON structure from classifier")
                return {"intent": "unclear", "confidence": 0.0}
            
            # Validate intent is one of the expected values
            valid_intents = ["code", "data", "writing", "career", "unclear"]
            if result["intent"] not in valid_intents:
                logger.warning(f"Invalid intent: {result['intent']}")
                return {"intent": "unclear", "confidence": 0.0}
            
            # Validate confidence is a number between 0 and 1
            confidence = float(result["confidence"])
            if confidence < 0.0 or confidence > 1.0:
                logger.warning(f"Invalid confidence: {confidence}")
                confidence = max(0.0, min(1.0, confidence))
            
            return {
                "intent": result["intent"],
                "confidence": confidence
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from classifier: {e}")
            return {"intent": "unclear", "confidence": 0.0}
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid data type in classifier response: {e}")
            return {"intent": "unclear", "confidence": 0.0}
            
    except Exception as e:
        logger.error(f"Error in classify_intent: {e}")
        return {"intent": "unclear", "confidence": 0.0}


def route_and_respond(message: str, intent: Dict[str, Any]) -> str:
    """
    Route the message to the appropriate expert persona and generate a response.
    
    Args:
        message: The user's input message
        intent: The classified intent dictionary with 'intent' and 'confidence' keys
        
    Returns:
        The generated response string
    """
    try:
        intent_label = intent.get("intent", "unclear")
        
        # Get the appropriate system prompt
        system_prompt = SYSTEM_PROMPTS.get(intent_label, SYSTEM_PROMPTS["unclear"])
        
        logger.info(f"Routing to intent: {intent_label}")
        
        # Make API call with the selected expert persona
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", DEFAULT_MODEL),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and return the response
        final_response = response.choices[0].message.content.strip()
        return final_response
        
    except Exception as e:
        logger.error(f"Error in route_and_respond: {e}")
        return "I apologize, but I encountered an error processing your request. Please try again."


def log_interaction(user_message: str, intent: Dict[str, Any], final_response: str) -> None:
    """
    Log the interaction to a JSON Lines file.
    
    Args:
        user_message: The original user message
        intent: The classified intent dictionary
        final_response: The final response sent to the user
    """
    try:
        log_entry = {
            "intent": intent.get("intent", "unclear"),
            "confidence": intent.get("confidence", 0.0),
            "user_message": user_message,
            "final_response": final_response
        }
        
        # Append to JSON Lines file
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
            
        logger.info(f"Logged interaction with intent: {intent.get('intent')}")
        
    except Exception as e:
        logger.error(f"Error logging interaction: {e}")


def process_message(message: str) -> Dict[str, Any]:
    """
    Process a user message through the complete routing pipeline.
    
    Args:
        message: The user's input message
        
    Returns:
        A dictionary containing the intent, confidence, and final response
    """
    # Step 1: Classify the intent
    intent = classify_intent(message)
    
    # Step 2: Route and generate response
    final_response = route_and_respond(message, intent)
    
    # Step 3: Log the interaction
    log_interaction(message, intent, final_response)
    
    return {
        "intent": intent["intent"],
        "confidence": intent["confidence"],
        "response": final_response
    }
