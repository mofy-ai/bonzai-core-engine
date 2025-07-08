#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# Load env file
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
print(f"Loading env from: {env_path}")
load_dotenv(env_path)

# Check keys
gemini_key = os.getenv('GEMINI_API_KEY')
mem0_key = os.getenv('MEM0_API_KEY')
port = os.getenv('PORT')

print(f'GEMINI_API_KEY: {repr(gemini_key)}')
print(f'MEM0_API_KEY: {repr(mem0_key)}')
print(f'PORT: {repr(port)}')

# Check validation logic
def is_real_value(value):
    return (value and 
            not value.startswith('your_') and 
            not value.endswith('_here') and
            len(value) > 10 and
            value != 'change_me')

print(f'GEMINI valid: {is_real_value(gemini_key)}')
print(f'MEM0 valid: {is_real_value(mem0_key)}')
print(f'PORT valid: {is_real_value(port)}')