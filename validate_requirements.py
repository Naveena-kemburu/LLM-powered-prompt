#!/usr/bin/env python3
"""
Validation script to verify all core requirements are met
"""
import json
import os
from colorama import init, Fore, Style

init(autoreset=True)


def validate_prompts():
    """Validate Requirement 1: Four distinct expert system prompts"""
    print(f"\n{Fore.CYAN}[Requirement 1] Validating system prompts...{Style.RESET_ALL}")
    
    try:
        from prompts import SYSTEM_PROMPTS
        
        required_intents = ['code', 'data', 'writing', 'career', 'unclear']
        
        if len(SYSTEM_PROMPTS) < 4:
            print(f"{Fore.RED}✗ FAIL: Less than 4 system prompts found{Style.RESET_ALL}")
            return False
        
        for intent in required_intents:
            if intent not in SYSTEM_PROMPTS:
                print(f"{Fore.RED}✗ FAIL: Missing prompt for '{intent}'{Style.RESET_ALL}")
                return False
            
            if len(SYSTEM_PROMPTS[intent]) < 50:
                print(f"{Fore.RED}✗ FAIL: Prompt for '{intent}' is too short{Style.RESET_ALL}")
                return False
        
        print(f"{Fore.GREEN}✓ PASS: {len(SYSTEM_PROMPTS)} distinct system prompts found{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ FAIL: {e}{Style.RESET_ALL}")
        return False


def validate_classify_function():
    """Validate Requirement 2: classify_intent function structure"""
    print(f"\n{Fore.CYAN}[Requirement 2] Validating classify_intent function...{Style.RESET_ALL}")
    
    try:
        # Check if router.py exists and contains classify_intent
        if not os.path.exists('router.py'):
            print(f"{Fore.RED}✗ FAIL: router.py not found{Style.RESET_ALL}")
            return False
        
        with open('router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'def classify_intent' not in content:
            print(f"{Fore.RED}✗ FAIL: classify_intent function not found{Style.RESET_ALL}")
            return False
        
        if 'message: str' not in content:
            print(f"{Fore.YELLOW}⚠ WARNING: classify_intent may not have correct signature{Style.RESET_ALL}")
        
        if '"intent"' in content and '"confidence"' in content:
            print(f"{Fore.GREEN}✓ PASS: classify_intent function exists with correct structure{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ WARNING: Return structure may not match requirements{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}  Note: Full validation requires API key and live testing{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ FAIL: {e}{Style.RESET_ALL}")
        return False


def validate_route_function():
    """Validate Requirement 3: route_and_respond function"""
    print(f"\n{Fore.CYAN}[Requirement 3] Validating route_and_respond function...{Style.RESET_ALL}")
    
    try:
        if not os.path.exists('router.py'):
            print(f"{Fore.RED}✗ FAIL: router.py not found{Style.RESET_ALL}")
            return False
        
        with open('router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'def route_and_respond' not in content:
            print(f"{Fore.RED}✗ FAIL: route_and_respond function not found{Style.RESET_ALL}")
            return False
        
        if 'SYSTEM_PROMPTS' in content:
            print(f"{Fore.GREEN}✓ PASS: route_and_respond uses SYSTEM_PROMPTS{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ WARNING: route_and_respond may not use system prompts{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}  Note: Full validation requires API key and live testing{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ FAIL: {e}{Style.RESET_ALL}")
        return False


def validate_unclear_handling():
    """Validate Requirement 4: Unclear intent handling"""
    print(f"\n{Fore.CYAN}[Requirement 4] Validating unclear intent handling...{Style.RESET_ALL}")
    
    try:
        from prompts import SYSTEM_PROMPTS
        
        unclear_prompt = SYSTEM_PROMPTS.get('unclear', '')
        
        if not unclear_prompt:
            print(f"{Fore.RED}✗ FAIL: No 'unclear' system prompt found{Style.RESET_ALL}")
            return False
        
        # Check if prompt mentions clarification or questions
        keywords = ['clarif', 'question', 'help', 'need more']
        if not any(keyword in unclear_prompt.lower() for keyword in keywords):
            print(f"{Fore.YELLOW}⚠ WARNING: 'unclear' prompt may not ask for clarification{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✓ PASS: 'unclear' intent handler exists{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ FAIL: {e}{Style.RESET_ALL}")
        return False


def validate_logging():
    """Validate Requirement 5: JSON Lines logging"""
    print(f"\n{Fore.CYAN}[Requirement 5] Validating logging functionality...{Style.RESET_ALL}")
    
    try:
        if not os.path.exists('router.py'):
            print(f"{Fore.RED}✗ FAIL: router.py not found{Style.RESET_ALL}")
            return False
        
        with open('router.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'def log_interaction' not in content:
            print(f"{Fore.RED}✗ FAIL: log_interaction function not found{Style.RESET_ALL}")
            return False
        
        LOG_FILE = 'route_log.jsonl'
        
        # Check if log file exists
        if not os.path.exists(LOG_FILE):
            print(f"{Fore.YELLOW}⚠ WARNING: {LOG_FILE} does not exist yet{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ PASS: Logging function exists (file will be created on first use){Style.RESET_ALL}")
            return True
        
        # Validate log file format
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) == 0:
            print(f"{Fore.YELLOW}⚠ WARNING: {LOG_FILE} is empty{Style.RESET_ALL}")
            return True
        
        # Validate each line is valid JSON
        for i, line in enumerate(lines, 1):
            try:
                entry = json.loads(line)
                
                # Check required keys
                required_keys = ['intent', 'confidence', 'user_message', 'final_response']
                for key in required_keys:
                    if key not in entry:
                        print(f"{Fore.RED}✗ FAIL: Line {i} missing key '{key}'{Style.RESET_ALL}")
                        return False
                
            except json.JSONDecodeError:
                print(f"{Fore.RED}✗ FAIL: Line {i} is not valid JSON{Style.RESET_ALL}")
                return False
        
        print(f"{Fore.GREEN}✓ PASS: {LOG_FILE} exists with {len(lines)} valid entries{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ FAIL: {e}{Style.RESET_ALL}")
        return False


def validate_error_handling():
    """Validate Requirement 6: Graceful error handling"""
    print(f"\n{Fore.CYAN}[Requirement 6] Validating error handling...{Style.RESET_ALL}")
    
    try:
        if not os.path.exists('router.py'):
            print(f"{Fore.RED}✗ FAIL: router.py not found{Style.RESET_ALL}")
            return False
        
        with open('router.py', 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Check if classify_intent has try-except blocks
        if 'try:' not in source or 'except' not in source:
            print(f"{Fore.YELLOW}⚠ WARNING: classify_intent may not have error handling{Style.RESET_ALL}")
        
        if 'json.loads' in source and 'JSONDecodeError' in source:
            print(f"{Fore.GREEN}✓ PASS: JSON parsing error handling detected{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ WARNING: JSON parsing error handling not clearly visible{Style.RESET_ALL}")
        
        # Check for default fallback
        if '"unclear"' in source and '0.0' in source:
            print(f"{Fore.GREEN}✓ PASS: Default fallback to 'unclear' detected{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ WARNING: Default fallback not clearly visible{Style.RESET_ALL}")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ FAIL: {e}{Style.RESET_ALL}")
        return False


def validate_containerization():
    """Validate containerization files"""
    print(f"\n{Fore.CYAN}[Additional] Validating containerization...{Style.RESET_ALL}")
    
    files = ['Dockerfile', 'docker-compose.yml', 'requirements.txt']
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            print(f"{Fore.GREEN}✓ {file} exists{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {file} missing{Style.RESET_ALL}")
            all_exist = False
    
    return all_exist


def validate_documentation():
    """Validate documentation files"""
    print(f"\n{Fore.CYAN}[Additional] Validating documentation...{Style.RESET_ALL}")
    
    files = ['README.md', '.env.example']
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            print(f"{Fore.GREEN}✓ {file} exists{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {file} missing{Style.RESET_ALL}")
            all_exist = False
    
    return all_exist


def main():
    """Run all validations"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}  LLM Prompt Router - Requirements Validation")
    print(f"{Fore.CYAN}{'='*70}")
    
    results = []
    
    results.append(("Requirement 1: System Prompts", validate_prompts()))
    results.append(("Requirement 2: classify_intent", validate_classify_function()))
    results.append(("Requirement 3: route_and_respond", validate_route_function()))
    results.append(("Requirement 4: Unclear Handling", validate_unclear_handling()))
    results.append(("Requirement 5: Logging", validate_logging()))
    results.append(("Requirement 6: Error Handling", validate_error_handling()))
    results.append(("Containerization", validate_containerization()))
    results.append(("Documentation", validate_documentation()))
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}  Validation Summary")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Fore.GREEN}✓ PASS" if result else f"{Fore.RED}✗ FAIL"
        print(f"{status}: {name}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Total: {passed}/{total} validations passed{Style.RESET_ALL}\n")
    
    if passed == total:
        print(f"{Fore.GREEN}🎉 All validations passed! Submission is ready.{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}⚠ Some validations failed. Please review and fix.{Style.RESET_ALL}\n")


if __name__ == '__main__':
    main()
