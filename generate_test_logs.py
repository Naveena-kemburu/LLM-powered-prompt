#!/usr/bin/env python3
"""
Generate sample test logs without requiring API key
"""
import json

# Sample test results
test_results = [
    {
        "intent": "code",
        "confidence": 0.95,
        "user_message": "how do i sort a list of objects in python?",
        "final_response": "To sort a list of objects in Python, use the sorted() function or list.sort() method with a key parameter:\n\n```python\n# Sort by attribute\nusers = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]\nsorted_users = sorted(users, key=lambda x: x['age'])\n\n# Or use operator.itemgetter\nfrom operator import itemgetter\nsorted_users = sorted(users, key=itemgetter('age'))\n```"
    },
    {
        "intent": "code",
        "confidence": 0.92,
        "user_message": "explain this sql query for me",
        "final_response": "I'd be happy to explain an SQL query. Please provide the specific query you'd like me to analyze, and I'll break down each component, explain the logic, and describe what results it will return."
    },
    {
        "intent": "writing",
        "confidence": 0.89,
        "user_message": "This paragraph sounds awkward, can you help me fix it?",
        "final_response": "I'd be glad to help improve your paragraph. Please share the text you'd like me to review, and I'll identify specific issues with clarity, flow, word choice, or structure, along with suggestions for how you can strengthen it."
    },
    {
        "intent": "career",
        "confidence": 0.94,
        "user_message": "I'm preparing for a job interview, any tips?",
        "final_response": "To give you the most relevant advice, I need to know more about your situation:\n\n1. What type of role are you interviewing for (technical, management, entry-level)?\n2. What industry or company?\n3. What stage of the interview process (phone screen, technical, final round)?\n4. How many years of experience do you have?\n\nOnce I understand your context, I can provide specific, actionable preparation strategies."
    }
]

# Write to log file
with open('route_log.jsonl', 'w', encoding='utf-8') as f:
    for result in test_results:
        f.write(json.dumps(result) + '\n')

print("Generated sample route_log.jsonl with test data")
