#!/usr/bin/env python3
"""
Script to populate sources and factors with realistic data from the plan.
"""
import json
import os
import glob
from pathlib import Path

# Source definitions from the plan
SOURCE_DEFINITIONS = {
    # Workflow 1: Target Account List
    "LinkedIn People Dataset Scraper": {
        "name": "LinkedIn People Dataset Scraper",
        "description": "Webhook-based scraper for LinkedIn professional profiles, extracting contact information, job roles, skills, and experience data",
        "source_type": "scraper",
        "delivery_type": "webhook",
        "url_template": "https://api.linkedin.com/v2/people",
        "method": "POST"
    },
    "Brightdata LinkedIn Scraper": {
        "name": "Brightdata LinkedIn Scraper",
        "description": "Fallback webhook scraper for LinkedIn data when primary scraper fails",
        "source_type": "scraper",
        "delivery_type": "webhook",
        "url_template": "https://api.brightdata.com/linkedin/profiles",
        "method": "POST"
    },
    "Apollo.io People API": {
        "name": "Apollo.io People API",
        "description": "Endpoint API for supplementary people data including contact information and professional details",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.apollo.io/v1/people/search",
        "method": "GET"
    },
    "Company Extraction Agent": {
        "name": "Company Extraction Agent",
        "description": "Webhook-based AI agent that extracts company information from unstructured data sources",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/extract/company",
        "method": "POST"
    },
    "Crunchbase Company API": {
        "name": "Crunchbase Company API",
        "description": "Endpoint API for company validation and enrichment with funding, employees, and industry data",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.crunchbase.com/v4/entities/organizations",
        "method": "GET"
    },
    "Company Enrichment from LinkedIn Profiles": {
        "name": "Company Enrichment from LinkedIn Profiles",
        "description": "Webhook agent that enriches company data using information extracted from LinkedIn profiles",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/enrich/company/linkedin",
        "method": "POST"
    },
    "Clearbit Company Enrichment API": {
        "name": "Clearbit Company Enrichment API",
        "description": "Endpoint API for supplementary company enrichment with firmographic and technographic data",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://company.clearbit.com/v2/companies/find",
        "method": "GET"
    },
    "ZoomInfo Company API": {
        "name": "ZoomInfo Company API",
        "description": "Endpoint API for B2B company data validation and enrichment",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.zoominfo.com/v1/company",
        "method": "GET"
    },
    "Company Enrichment API": {
        "name": "Company Enrichment API",
        "description": "Primary endpoint API for comprehensive company enrichment with complete profile information",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.enrichment.internal/v1/companies",
        "method": "POST"
    },
    "FullContact Company API": {
        "name": "FullContact Company API",
        "description": "Endpoint API for supplementary company data including social media and contact information",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.fullcontact.com/v3/company.enrich",
        "method": "POST"
    },
    "PeopleDataLabs Company API": {
        "name": "PeopleDataLabs Company API",
        "description": "Endpoint API for company validation and professional data enrichment",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.peopledatalabs.com/v5/company/enrich",
        "method": "GET"
    },
    "Hunter.io Company API": {
        "name": "Hunter.io Company API",
        "description": "Endpoint API for email verification and company contact discovery",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.hunter.io/v2/domain-search",
        "method": "GET"
    },
    "Decision Maker Extraction Agent": {
        "name": "Decision Maker Extraction Agent",
        "description": "Webhook-based AI agent that identifies and extracts key decision makers from company data",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/extract/decision-makers",
        "method": "POST"
    },
    "LinkedIn Sales Navigator API": {
        "name": "LinkedIn Sales Navigator API",
        "description": "Endpoint API for decision maker validation and seniority information",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.linkedin.com/v2/salesNavigator/people",
        "method": "GET"
    },
    "Lusha Decision Maker API": {
        "name": "Lusha Decision Maker API",
        "description": "Endpoint API for supplementary decision maker contact information",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.lusha.com/person",
        "method": "GET"
    },
    "Person Enrichment API": {
        "name": "Person Enrichment API",
        "description": "Primary endpoint API for comprehensive person enrichment with complete contact and professional data",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.enrichment.internal/v1/persons",
        "method": "POST"
    },
    "Clearbit Person API": {
        "name": "Clearbit Person API",
        "description": "Endpoint API for supplementary person professional data enrichment",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://person.clearbit.com/v2/combined/find",
        "method": "GET"
    },
    "RocketReach Person API": {
        "name": "RocketReach Person API",
        "description": "Endpoint API for person contact data and email discovery",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.rocketreach.co/v2/api/lookupProfile",
        "method": "GET"
    },
    # Workflow 2: Account Scoring
    "User Database API": {
        "name": "User Database API",
        "description": "Primary endpoint API for sourcing user data from internal systems",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.internal/users",
        "method": "GET"
    },
    "Salesforce User API": {
        "name": "Salesforce User API",
        "description": "Endpoint API for CRM integration and user data from Salesforce",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.salesforce.com/services/data/v57.0/sobjects/User",
        "method": "GET"
    },
    "HubSpot Contacts API": {
        "name": "HubSpot Contacts API",
        "description": "Endpoint API for marketing integration and user data from HubSpot",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.hubapi.com/contacts/v1/contact",
        "method": "GET"
    },
    "Company Extraction from User Data": {
        "name": "Company Extraction from User Data",
        "description": "Webhook agent that extracts company information from user data",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/extract/company/user",
        "method": "POST"
    },
    "Clearbit Reveal API": {
        "name": "Clearbit Reveal API",
        "description": "Endpoint API for IP-based company enrichment and identification",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://reveal.clearbit.com/v1/companies/find",
        "method": "GET"
    },
    "DiscoverOrg Company API": {
        "name": "DiscoverOrg Company API",
        "description": "Endpoint API for technographic company data and technology stack information",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.discoverorg.com/v1/companies",
        "method": "GET"
    },
    "Custom Random Forest Model": {
        "name": "Custom Random Forest Model",
        "description": "Webhook-based ML model for lead scoring validation and ensemble predictions",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://ml.internal/api/v1/models/random-forest/invocations",
        "method": "POST"
    },
    "Gradient Boosting Model": {
        "name": "Gradient Boosting Model",
        "description": "Webhook-based ML model for ensemble lead scoring predictions",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://ml.internal/api/v1/models/gradient-boosting/invocations",
        "method": "POST"
    },
    # Workflow 3: Supplier Evaluation
    "ERP Supplier Database API": {
        "name": "ERP Supplier Database API",
        "description": "Primary endpoint API for sourcing supplier data from ERP systems",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.erp.internal/v1/suppliers",
        "method": "GET"
    },
    "SAP Ariba Supplier API": {
        "name": "SAP Ariba Supplier API",
        "description": "Endpoint API for procurement system integration and supplier data",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.ariba.com/v1/suppliers",
        "method": "GET"
    },
    "LinkedIn Company Scraper": {
        "name": "LinkedIn Company Scraper",
        "description": "Primary webhook scraper for LinkedIn company pages including employee count and followers",
        "source_type": "scraper",
        "delivery_type": "webhook",
        "url_template": "https://api.linkedin.com/v2/organizations",
        "method": "POST"
    },
    "LinkedIn Company Pages API": {
        "name": "LinkedIn Company Pages API",
        "description": "Endpoint API for official LinkedIn company page data",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.linkedin.com/v2/organizations",
        "method": "GET"
    },
    "Brightdata LinkedIn Company Scraper": {
        "name": "Brightdata LinkedIn Company Scraper",
        "description": "Fallback webhook scraper for LinkedIn company data",
        "source_type": "scraper",
        "delivery_type": "webhook",
        "url_template": "https://api.brightdata.com/linkedin/companies",
        "method": "POST"
    },
    "ESG Compliance Agent": {
        "name": "ESG Compliance Agent",
        "description": "Primary webhook-based AI agent for ESG compliance data enrichment",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/esg/compliance",
        "method": "POST"
    },
    "Sustainalytics ESG API": {
        "name": "Sustainalytics ESG API",
        "description": "Endpoint API for ESG ratings and sustainability scores",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.sustainalytics.com/v1/esg-ratings",
        "method": "GET"
    },
    "MSCI ESG API": {
        "name": "MSCI ESG API",
        "description": "Endpoint API for ESG scores and environmental impact data",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.msci.com/v1/esg-scores",
        "method": "GET"
    },
    "Refinitiv ESG API": {
        "name": "Refinitiv ESG API",
        "description": "Endpoint API for comprehensive ESG data and compliance information",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.refinitiv.com/v1/esg-data",
        "method": "GET"
    },
    "Document Extraction Agent": {
        "name": "Document Extraction Agent",
        "description": "Primary webhook-based AI agent for extracting compliance documents from various sources",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/extract/documents",
        "method": "POST"
    },
    "Databricks Documents API": {
        "name": "Databricks Documents API",
        "description": "Endpoint API for document storage and retrieval from Databricks",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.databricks.com/v1/documents",
        "method": "GET"
    },
    "SharePoint Documents API": {
        "name": "SharePoint Documents API",
        "description": "Endpoint API for enterprise document storage and retrieval",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.sharepoint.com/v1/documents",
        "method": "GET"
    },
    "Document Enrichment Agent": {
        "name": "Document Enrichment Agent",
        "description": "Primary webhook-based AI agent for enriching documents with structured data",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/enrich/documents",
        "method": "POST"
    },
    "RAG Agent Document Processing": {
        "name": "RAG Agent Document Processing",
        "description": "Webhook-based RAG agent for document content analysis and structured data extraction",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/rag/process",
        "method": "POST"
    },
    "OpenAI Document Analysis API": {
        "name": "OpenAI Document Analysis API",
        "description": "Endpoint API for AI-powered document analysis and content understanding",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.openai.com/v1/chat/completions",
        "method": "POST"
    },
    "Contact Extraction Agent": {
        "name": "Contact Extraction Agent",
        "description": "Primary webhook-based AI agent for extracting contact information from company data",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/extract/contacts",
        "method": "POST"
    },
    "ZoomInfo Contact API": {
        "name": "ZoomInfo Contact API",
        "description": "Endpoint API for B2B contact information and professional data",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.zoominfo.com/v1/contact",
        "method": "GET"
    },
    "Contact Enrichment API": {
        "name": "Contact Enrichment API",
        "description": "Primary endpoint API for comprehensive contact enrichment with complete profile data",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.enrichment.internal/v1/contacts",
        "method": "POST"
    },
    "Lusha Contact API": {
        "name": "Lusha Contact API",
        "description": "Endpoint API for contact verification and email discovery",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.lusha.com/contact",
        "method": "GET"
    },
    # Workflow 4: Feature Compliance
    "GitHub API": {
        "name": "GitHub API",
        "description": "Primary endpoint API for sourcing merge requests from GitHub repositories",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.github.com/repos/{owner}/{repo}/pulls",
        "method": "GET"
    },
    "GitLab API": {
        "name": "GitLab API",
        "description": "Endpoint API for fallback merge request sourcing from GitLab repositories",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.gitlab.com/v4/projects/{id}/merge_requests",
        "method": "GET"
    },
    "IT Compliance Agent": {
        "name": "IT Compliance Agent",
        "description": "Primary webhook-based AI agent for IT compliance and code quality analysis (currently experiencing timeout issues)",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/compliance/analyze",
        "method": "POST"
    },
    "SonarQube Code Quality API": {
        "name": "SonarQube Code Quality API",
        "description": "Endpoint API for code quality analysis and fallback when IT Compliance Agent fails",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.sonarqube.org/api/measures/component",
        "method": "GET"
    },
    "CodeClimate Quality API": {
        "name": "CodeClimate Quality API",
        "description": "Endpoint API for alternative code quality analysis and metrics",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.codeclimate.com/v1/repos",
        "method": "GET"
    },
    # Workflow 6: Knowledge-Base Clean-Up
    "Document Storage API": {
        "name": "Document Storage API",
        "description": "Primary endpoint API for sourcing documents from storage systems",
        "source_type": "api",
        "delivery_type": "endpoint",
        "url_template": "https://api.storage.internal/v1/documents",
        "method": "GET"
    },
    "RAG Agent Document Enrichment": {
        "name": "RAG Agent Document Enrichment",
        "description": "Primary webhook-based RAG agent for enriching documents with structured content and metadata",
        "source_type": "agent",
        "delivery_type": "webhook",
        "url_template": "https://agents.internal/api/v1/rag/enrich",
        "method": "POST"
    },
}

def update_source_file(filepath, source_def):
    """Update a source file with the provided definition."""
    try:
        with open(filepath, 'r') as f:
            source = json.load(f)
    except:
        return False
    
    # Update basic fields
    source['name'] = source_def['name']
    source['description'] = source_def['description']
    source['source_type'] = source_def['source_type']
    source['delivery_type'] = source_def['delivery_type']
    
    # Update request template
    if 'run_request' in source.get('setup', {}):
        source['setup']['run_request']['request_template'] = {
            "url": source_def.get('url_template', ''),
            "method": source_def.get('method', 'GET'),
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "Bearer <<$api_key>>"
            },
            "body": {} if source_def.get('method') == 'GET' else {
                "query": "<<$run_setup>>"
            }
        }
    
    # Write back
    with open(filepath, 'w') as f:
        json.dump(source, f, indent=2)
    
    return True

def main():
    """Main function to populate sources."""
    sources_dir = Path('sources')
    
    # Get all source files
    source_files = list(sources_dir.glob('*.json'))
    source_files = [f for f in source_files if f.name != 'source-template.json' and f.name != 'sources.json']
    
    print(f"Found {len(source_files)} source files")
    
    # Try to match sources by name (if we can read existing names)
    # Otherwise, we'll need to manually map them
    updated = 0
    for source_file in source_files[:59]:  # Limit to 59 as per plan
        try:
            with open(source_file, 'r') as f:
                data = json.load(f)
                current_name = data.get('name', '').strip()
                
                # Try to find matching definition
                if current_name and current_name in SOURCE_DEFINITIONS:
                    if update_source_file(source_file, SOURCE_DEFINITIONS[current_name]):
                        updated += 1
                        print(f"Updated: {source_file.name} - {current_name}")
        except Exception as e:
            print(f"Error processing {source_file.name}: {e}")
    
    print(f"\nUpdated {updated} source files")
    print(f"Note: Remaining sources may need manual mapping")

if __name__ == '__main__':
    main()









