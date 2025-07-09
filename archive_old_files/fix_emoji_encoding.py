#!/usr/bin/env python3
"""
 FIX EMOJI ENCODING ISSUES
Remove all emojis from logging to prevent Windows CP1252 crashes
"""

import os
import re
import glob

def remove_emojis_from_file(filepath):
    """Remove emojis from a Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove common emojis from logging statements
        emoji_patterns = [
            r'', r'', r'', r'', r'', r'', r'', r'', r'', 
            r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r'',
            r'', r'', r'', r'', r'', r'', r'', r'', r''
        ]
        
        original_content = content
        
        for emoji in emoji_patterns:
            # Replace emoji in logging statements
            content = re.sub(f'"{emoji}([^"]*)"', r'"\1"', content)
            content = re.sub(f"'{emoji}([^']*)'", r"'\1'", content)
            content = re.sub(f'f"{emoji}([^"]*)"', r'f"\1"', content)
            content = re.sub(f"f'{emoji}([^']*)'", r"f'\1'", content)
        
        # Remove standalone emojis
        for emoji in emoji_patterns:
            content = content.replace(emoji, '')
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed emojis in {filepath}")
            return True
        else:
            print(f"- No emojis found in {filepath}")
            return False
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")
        return False

def main():
    print(" FIXING EMOJI ENCODING ISSUES")
    print("=" * 50)
    
    # Find all Python files
    python_files = []
    for pattern in ['*.py', 'api/*.py', 'services/*.py', 'services/*/*.py']:
        python_files.extend(glob.glob(pattern))
    
    fixed_count = 0
    
    for filepath in python_files:
        if remove_emojis_from_file(filepath):
            fixed_count += 1
    
    print(f"\n SUMMARY:")
    print(f"Files processed: {len(python_files)}")
    print(f"Files fixed: {fixed_count}")
    print("\n Ready to test backend without emoji crashes!")

if __name__ == "__main__":
    main()