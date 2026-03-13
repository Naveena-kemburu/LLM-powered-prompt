#!/usr/bin/env python3
"""
Command-line interface for the LLM-Powered Prompt Router
"""
import os
import sys
from dotenv import load_dotenv
from router import process_message
from colorama import init, Fore, Style

# Load environment variables from .env file
load_dotenv()

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def print_banner():
    """Print welcome banner"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}  LLM-Powered Prompt Router")
    print(f"{Fore.CYAN}  Intent Classification & Expert Routing")
    print(f"{Fore.CYAN}{'='*60}\n")


def print_result(result):
    """Print the routing result with formatting"""
    intent = result['intent']
    confidence = result['confidence']
    response = result['response']
    
    # Color code by intent
    intent_colors = {
        'code': Fore.GREEN,
        'data': Fore.BLUE,
        'writing': Fore.MAGENTA,
        'career': Fore.YELLOW,
        'unclear': Fore.RED
    }
    
    color = intent_colors.get(intent, Fore.WHITE)
    
    print(f"\n{color}[Intent: {intent.upper()}] [Confidence: {confidence:.2f}]{Style.RESET_ALL}")
    print(f"\n{response}\n")
    print(f"{Fore.CYAN}{'-'*60}\n")


def interactive_mode():
    """Run the CLI in interactive mode"""
    print_banner()
    print(f"{Fore.WHITE}Type your message and press Enter. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            # Get user input
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
                break
            
            # Process the message
            result = process_message(user_input)
            
            # Display the result
            print_result(result)
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}\n")


def single_message_mode(message):
    """Process a single message and exit"""
    result = process_message(message)
    print_result(result)


def main():
    """Main entry point"""
    # Check for API key based on provider
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "groq":
        if not os.getenv("GROQ_API_KEY"):
            print(f"{Fore.RED}Error: GROQ_API_KEY environment variable is not set!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please set your Groq API key:{Style.RESET_ALL}")
            print(f"  export GROQ_API_KEY='your-api-key-here'\n")
            print(f"{Fore.CYAN}Get a FREE key at: https://console.groq.com{Style.RESET_ALL}\n")
            sys.exit(1)
    else:
        if not os.getenv("OPENAI_API_KEY"):
            print(f"{Fore.RED}Error: OPENAI_API_KEY environment variable is not set!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Please set your OpenAI API key:{Style.RESET_ALL}")
            print(f"  export OPENAI_API_KEY='your-api-key-here'\n")
            sys.exit(1)
    
    # Check if message provided as argument
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
        single_message_mode(message)
    else:
        interactive_mode()


if __name__ == '__main__':
    main()
