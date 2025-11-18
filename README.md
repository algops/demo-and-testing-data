# Demo and Testing Data

This repository contains comprehensive demo and testing data for the AlgoPS platform, including:

## Data Structure

### Core Data Files
- `object-types.json` - Object type definitions
- `datapoints.json` - Datapoint definitions for each object type
- `factors.json` - Business logic factors (guardrails and use cases)
- `targets.json` - Target definitions for data extraction

### Source Data
- `sources/` - Individual source configurations and sample data
  - Crunchbase API
  - Brightdata Scraper
  - Enrichment Agent
  - MLFlow Lead Scoring Model
  - LinkedIn People Dataset
  - Databricks Documents API
  - RAG Agent
  - ESG Agent
  - ETL Pipeline
  - GitHub API
  - ETL Documents API
  - Trustsoft IT Agent
  - Document Storage API
  - Document Classification Agent
  - RAG Agent with Guardrails

### Activity Data
- `activities/` - Activity configurations and metadata
  - Lead Scoring: Company sourcing, enrichment, scoring, people extraction and enrichment
  - Supplier Compliance: Document sourcing, company extraction, RAG rules, ESG enrichment, contact extraction
  - QA Software Development: GitHub merge requests, document sourcing, RAG enrichment, IT agent evaluation
  - Knowledge Base: Document sourcing, classification, structured rules creation

### Workflow Data
- `workflows/` - Workflow configurations and execution data
  - Lead Scoring for Nurturing (3 phases, 5 activities)
  - Supplier Compliance Check/Monitoring (3 phases, 5 activities)
  - Automate Quality Assurance and Reporting of Software Development (3 phases, 4 activities)
  - Prepare Knowledge Base Directory for Support Chatbot (3 phases, 3 activities)

### Sample Data
- `samples/` - Sample data for development and testing
  - Companies, persons, documents, job posts, organizations
  - Merge requests, knowledge sources, regulations, contacts

### Legacy Data
- `1.0/` - Legacy data files for reference

## Usage

This data is designed to be used as a git submodule in the UI repository for local development and testing. The data structure follows the AlgoPS platform schema and can be imported directly into the application for development purposes.

## Data Generation

This data was generated following the comprehensive data generation plan outlined in the implementation docs repository. It includes:

- Realistic business data with proper relationships
- Edge cases for comprehensive testing
- Complete factor-source mappings
- Validation utilities and error handling
- Cross-system integration testing data

## File Organization

- **Main JSON files**: Core data definitions at the root level
- **Source-specific data**: Organized in `sources/` with individual folders
- **Activity data**: Organized in `activities/` with individual activity files
- **Workflow data**: Organized in `workflows/` with individual workflow files
- **Sample data**: Organized in `samples/` for development use
- **Legacy data**: Organized in `1.0/` for reference

## Integration

This repository is designed to be used as a git submodule in the main UI repository, allowing for:
- Independent versioning of demo data
- Shared access across multiple projects
- Local development with realistic data
- Comprehensive testing scenarios
