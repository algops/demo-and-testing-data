#!/usr/bin/env python3
"""
Comprehensive script to populate all sources from sources.json with complete setup.
"""
import json
from pathlib import Path

# Load sources.json
with open('sources/sources.json', 'r') as f:
    sources_data = json.load(f)

source_map = {s['id']: s for s in sources_data['sources']}

# URL templates based on source names
def get_url_template(name, source_type, delivery_type):
    name_lower = name.lower()
    
    if 'linkedin' in name_lower:
        if 'people' in name_lower or 'person' in name_lower:
            return "https://api.linkedin.com/v2/people"
        elif 'company' in name_lower:
            return "https://api.linkedin.com/v2/organizations"
        else:
            return "https://api.linkedin.com/v2/endpoint"
    elif 'crunchbase' in name_lower:
        return "https://api.crunchbase.com/v4/entities/organizations"
    elif 'clearbit' in name_lower:
        if 'company' in name_lower:
            return "https://company.clearbit.com/v2/companies/find"
        elif 'person' in name_lower:
            return "https://person.clearbit.com/v2/combined/find"
        elif 'reveal' in name_lower:
            return "https://reveal.clearbit.com/v1/companies/find"
    elif 'zoominfo' in name_lower:
        if 'company' in name_lower:
            return "https://api.zoominfo.com/v1/company"
        elif 'contact' in name_lower:
            return "https://api.zoominfo.com/v1/contact"
    elif 'rag' in name_lower or 'agent' in name_lower:
        if 'rag' in name_lower:
            return "https://agents.internal/api/v1/rag/process"
        elif 'esg' in name_lower:
            return "https://agents.internal/api/v1/esg/compliance"
        elif 'compliance' in name_lower or 'it' in name_lower:
            return "https://agents.internal/api/v1/compliance/analyze"
        elif 'extraction' in name_lower:
            return "https://agents.internal/api/v1/extract"
        elif 'enrichment' in name_lower or 'enrich' in name_lower:
            return "https://agents.internal/api/v1/enrich"
        else:
            return "https://agents.internal/api/v1/process"
    elif 'github' in name_lower:
        return "https://api.github.com/repos/{owner}/{repo}/pulls"
    elif 'gitlab' in name_lower:
        return "https://api.gitlab.com/v4/projects/{id}/merge_requests"
    elif 'databricks' in name_lower:
        return "https://api.databricks.com/v1/documents"
    elif 'sharepoint' in name_lower:
        return "https://api.sharepoint.com/v1/documents"
    elif 'salesforce' in name_lower:
        return "https://api.salesforce.com/services/data/v57.0/sobjects/User"
    elif 'hubspot' in name_lower:
        return "https://api.hubapi.com/contacts/v1/contact"
    elif 'apollo' in name_lower:
        return "https://api.apollo.io/v1/people/search"
    elif 'lusha' in name_lower:
        return "https://api.lusha.com/person"
    elif 'rocketreach' in name_lower:
        return "https://api.rocketreach.co/v2/api/lookupProfile"
    elif 'hunter' in name_lower:
        return "https://api.hunter.io/v2/domain-search"
    elif 'brightdata' in name_lower:
        return "https://api.brightdata.com/linkedin/profiles"
    elif 'sonarqube' in name_lower:
        return "https://api.sonarqube.org/api/measures/component"
    elif 'codeclimate' in name_lower:
        return "https://api.codeclimate.com/v1/repos"
    elif 'mlflow' in name_lower or 'model' in name_lower:
        return "https://mlflow.internal/api/v1/models/lead-scoring-v2/invocations"
    elif 'erp' in name_lower or 'ariba' in name_lower:
        return "https://api.erp.internal/v1/suppliers"
    elif 'storage' in name_lower or 'document' in name_lower:
        return "https://api.storage.internal/v1/documents"
    elif 'user' in name_lower or 'database' in name_lower:
        return "https://api.internal/users"
    elif 'etl' in name_lower:
        return "https://api.etl.internal/v1/pipeline"
    else:
        return "https://api.internal/v1/endpoint"

def get_method(source_type, delivery_type):
    if delivery_type.lower() == 'webhook' or source_type.lower() in ['agent', 'scraper']:
        return "POST"
    else:
        return "GET"

# Get all source files
sources_dir = Path('sources')
source_files = [f for f in sources_dir.glob('*.json') 
                if f.name not in ['source-template.json', 'sources.json']]

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
            
            # Ensure setup exists
            if 'setup' not in source:
                source['setup'] = {}
            
            # Update load balancing
            if 'load_balancing' not in source['setup']:
                source['setup']['load_balancing'] = {
                    "concurrency": source_info.get('max_concurrent_runs', 10),
                    "timeout": source_info.get('timeout', 30)
                }
            
            # Update processing options
            if 'processing_options' not in source['setup']:
                source['setup']['processing_options'] = {
                    "input_processing": "ignore"
                }
            
            # Update customization permissions
            if 'customization_permissions' not in source['setup']:
                source['setup']['customization_permissions'] = {
                    "factor_creation": "creator_only"
                }
            
            # Update run_request
            if 'run_request' not in source['setup']:
                source['setup']['run_request'] = {}
            
            run_request = source['setup']['run_request']
            
            # Update request template
            if 'request_template' not in run_request:
                run_request['request_template'] = {}
            
            template = run_request['request_template']
            if not template.get('url'):
                template['url'] = get_url_template(source_info['name'], 
                                                   source_info.get('source_type', ''),
                                                   source_info.get('delivery_type', ''))
                template['method'] = get_method(source_info.get('source_type', ''),
                                                source_info.get('delivery_type', ''))
                template['headers'] = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer <<$api_key>>"
                }
                if template['method'] == 'GET':
                    template['body'] = {}
                else:
                    template['body'] = {
                        "query": "<<$run_setup>>",
                        "webhook_url": "<<$webhook_url>>"
                    }
            
            # Update mappings if missing
            if 'mappings' not in run_request:
                run_request['mappings'] = {
                    "request": {
                        "run_setup": {
                            "path": ["body", "query"] if template['method'] == 'POST' else ["query"],
                            "mapping_status": "mapped"
                        },
                        "webhook_url": {
                            "path": ["body", "webhook_url"] if template['method'] == 'POST' else [],
                            "mapping_status": "mapped" if template['method'] == 'POST' else "remaining"
                        },
                        "run_id": {
                            "path": ["id"],
                            "mapping_status": "mapped"
                        }
                    },
                    "response": {
                        "status": {
                            "path": ["status"],
                            "mapping_status": "mapped"
                        }
                    }
                }
            
            # Update factor_variables if missing
            if 'factor_variables' not in run_request:
                run_request['factor_variables'] = {
                    "run_setup": {
                        "path": ["body", "query"] if template['method'] == 'POST' else ["query"],
                        "example_value": {
                            "filters": {
                                "industry": "Technology",
                                "size": "medium"
                            }
                        }
                    }
                }
            
            # Update response_examples if missing
            if 'response_examples' not in run_request:
                run_request['response_examples'] = []
            
            # Update status_request
            if 'status_request' not in source['setup']:
                source['setup']['status_request'] = {
                    "mappings": {
                        "request": {
                            "run_external_id": {
                                "path": ["url"],
                                "mapping_status": "mapped"
                            }
                        },
                        "response": {
                            "status": {
                                "path": ["status"],
                                "mapping_status": "mapped"
                            }
                        }
                    },
                    "request_template": {
                        "url": template['url'].replace('/endpoint', '/status'),
                        "method": "GET",
                        "headers": template['headers'],
                        "body": {}
                    },
                    "response_examples": []
                }
            
            # Update delivery_request
            if 'delivery_request' not in source['setup']:
                source['setup']['delivery_request'] = {
                    "mappings": {
                        "request": {
                            "run_external_id": {
                                "path": ["url"],
                                "mapping_status": "mapped"
                            }
                        },
                        "response": {
                            "data": {
                                "path": ["data"],
                                "mapping_status": "mapped"
                            }
                        }
                    },
                    "request_template": {
                        "url": template['url'].replace('/endpoint', '/results'),
                        "method": "GET",
                        "headers": template['headers'],
                        "body": {}
                    },
                    "response_examples": [],
                    "response_mappings": {}
                }
            
            # Write back
            with open(source_file, 'w') as f:
                json.dump(source, f, indent=2)
            
            updated += 1
            if updated % 5 == 0:
                print(f"Updated {updated} sources...")
                
    except Exception as e:
        print(f"Error processing {source_file.name}: {e}")

print(f"\nSuccessfully updated {updated} source files with complete setup")









