#!/usr/bin/env python3
"""
Script to update all source files based on sources.json mapping.
"""
import json
import os
from pathlib import Path

# Load sources.json to get ID to name mapping
with open('sources/sources.json', 'r') as f:
    sources_data = json.load(f)

# Create mapping of ID to source info
source_map = {s['id']: s for s in sources_data['sources']}

# Get all individual source files
sources_dir = Path('sources')
source_files = [f for f in sources_dir.glob('*.json') 
                if f.name not in ['source-template.json', 'sources.json']]

print(f"Found {len(source_files)} individual source files")
print(f"Found {len(source_map)} sources in sources.json")

updated = 0
for source_file in source_files:
    try:
        with open(source_file, 'r') as f:
            source = json.load(f)
        
        source_id = source.get('id', '')
        if source_id in source_map:
            source_info = source_map[source_id]
            
            # Update basic fields
            source['name'] = source_info['name']
            source['description'] = source_info['description']
            source['source_type'] = source_info.get('source_type', '').lower()
            source['delivery_type'] = source_info.get('delivery_type', '').lower()
            
            # Update setup if it exists
            if 'setup' in source:
                # Update request template with realistic URL
                if 'run_request' in source['setup']:
                    if 'request_template' not in source['setup']['run_request']:
                        source['setup']['run_request']['request_template'] = {}
                    
                    template = source['setup']['run_request']['request_template']
                    if not template.get('url'):
                        # Generate realistic URL based on source name
                        name_lower = source_info['name'].lower()
                        if 'api' in name_lower:
                            template['url'] = f"https://api.{name_lower.replace(' ', '').replace('api', '')}.com/v1/endpoint"
                        elif 'agent' in name_lower:
                            template['url'] = "https://agents.internal/api/v1/process"
                        elif 'scraper' in name_lower:
                            template['url'] = "https://scraper.internal/api/v1/scrape"
                        else:
                            template['url'] = "https://api.internal/v1/endpoint"
                        
                        template['method'] = 'POST' if 'agent' in name_lower or 'scraper' in name_lower else 'GET'
                        template['headers'] = {
                            "Content-Type": "application/json",
                            "Authorization": "Bearer <<$api_key>>"
                        }
                        template['body'] = {} if template['method'] == 'GET' else {"query": "<<$run_setup>>"}
            
            # Write back
            with open(source_file, 'w') as f:
                json.dump(source, f, indent=2)
            
            updated += 1
            if updated % 10 == 0:
                print(f"Updated {updated} files...")
                
    except Exception as e:
        print(f"Error processing {source_file.name}: {e}")

print(f"\nSuccessfully updated {updated} source files")

