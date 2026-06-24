#!/usr/bin/env python3
"""
Script to populate factor descriptions based on their names and types.
"""
import json

# Load factors.json
with open('factors.json', 'r') as f:
    factors_data = json.load(f)

factors = factors_data.get('factors', [])

print(f"Found {len(factors)} factors")

updated = 0
for factor in factors:
    if not factor.get('description') or factor.get('description').strip() == '':
        name = factor.get('name', '')
        factor_type = factor.get('type', '')
        factor_factor_type = factor.get('factor_type', '')
        
        # Generate description based on name and type
        if factor_type == 'use-case':
            if 'What is' in name or 'What are' in name or 'Who are' in name:
                description = f"Use case question: {name.lower()}"
            elif 'How often' in name or 'How many' in name:
                description = f"Use case question: {name.lower()}"
            else:
                description = f"Use case: {name.lower()}"
        elif factor_type == 'guardrail':
            if 'validation' in name.lower():
                description = f"Guardrail validation rule: {name.lower()}"
            elif 'format' in name.lower():
                description = f"Guardrail format validation: {name.lower()}"
            elif 'range' in name.lower():
                description = f"Guardrail range validation: {name.lower()}"
            else:
                description = f"Guardrail rule: {name.lower()}"
        else:
            description = f"{factor_type} factor: {name.lower()}"
        
        factor['description'] = description
        updated += 1
        
        if updated % 50 == 0:
            print(f"Updated {updated} factors...")

# Save back
with open('factors.json', 'w') as f:
    json.dump(factors_data, f, indent=2)

print(f"\nSuccessfully updated {updated} factors with descriptions")









