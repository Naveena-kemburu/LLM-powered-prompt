#!/usr/bin/env python3
"""
Test suite for the LLM-Powered Prompt Router
"""
import os
from dotenv import load_dotenv
from router import process_message
from colorama import init, Fore, Style

# Load environment variables from .env file
load_dotenv()

init(autoreset=True)

# Test messages as specified in the requirements
TEST_MESSAGES = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "This paragraph sounds awkward, can you help me fix it?",
    "I'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12, 45, 23, 67, 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose."
]


def run_tests():
    """Run all test messages through the router"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}  Running Test Suite - {len(TEST_MESSAGES)} Test Messages")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "groq":
        if not os.getenv("GROQ_API_KEY"):
            print(f"{Fore.RED}Error: GROQ_API_KEY environment variable is not set!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Get a FREE key at: https://console.groq.com{Style.RESET_ALL}")
            return
    else:
        if not os.getenv("OPENAI_API_KEY"):
            print(f"{Fore.RED}Error: OPENAI_API_KEY environment variable is not set!{Style.RESET_ALL}")
            return
    
    results_summary = {
        'code': 0,
        'data': 0,
        'writing': 0,
        'career': 0,
        'unclear': 0
    }
    
    for i, message in enumerate(TEST_MESSAGES, 1):
        print(f"{Fore.YELLOW}[Test {i}/{len(TEST_MESSAGES)}]{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Message: {message}{Style.RESET_ALL}")
        
        try:
            result = process_message(message)
            
            intent = result['intent']
            confidence = result['confidence']
            
            results_summary[intent] += 1
            
            # Color code by intent
            intent_colors = {
                'code': Fore.GREEN,
                'data': Fore.BLUE,
                'writing': Fore.MAGENTA,
                'career': Fore.YELLOW,
                'unclear': Fore.RED
            }
            
            color = intent_colors.get(intent, Fore.WHITE)
            print(f"{color}Intent: {intent.upper()} | Confidence: {confidence:.2f}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'-'*70}\n")
            
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")
    
    # Print summary
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}  Test Results Summary")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    for intent, count in results_summary.items():
        color = {
            'code': Fore.GREEN,
            'data': Fore.BLUE,
            'writing': Fore.MAGENTA,
            'career': Fore.YELLOW,
            'unclear': Fore.RED
        }.get(intent, Fore.WHITE)
        
        print(f"{color}{intent.upper()}: {count} messages{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}All test results have been logged to route_log.jsonl{Style.RESET_ALL}\n")


if __name__ == '__main__':
    run_tests()
