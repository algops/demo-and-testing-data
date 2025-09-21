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
  - LinkedIn People Dataset
  - AI Company Researcher
  - Real Estate API
  - E-commerce Scraper
  - Job Market Scraper
  - Event Management System
  - Automotive Database
  - ESG Agent

### Activity Data
- `activities/` - Activity configurations and metadata
  - Company enrichment activities
  - Data extraction activities
  - ML training activities
  - Prediction activities

### Workflow Data
- `workflows/` - Workflow configurations and execution data
  - E-commerce product discovery workflows
  - Real estate market analysis workflows
  - Document processing workflows

### Sample Data
- `samples/` - Sample data for development and testing
  - Companies, persons, documents, job posts, organizations

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
