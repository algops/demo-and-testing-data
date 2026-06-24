# Source API Simulators

This directory contains a collection of Node.js-based API simulators designed to mimic the behavior of various data sources. These simulators are crucial for local development and testing of the AlgOps data pipeline, allowing for comprehensive testing of data ingestion, processing, and error handling without relying on external APIs.

## Architecture

Each simulator is a standalone Express.js application located within its respective source subfolder (`data/sources/{source-name}/simulator/`). They are designed to:

1. **Replicate API Interfaces:** Exactly match the URL patterns, HTTP methods, headers, and request/response structures defined in the `source-detail.json` files.
2. **Generate Realistic Data:** Use `faker.js` and custom data generation logic to produce diverse and realistic data for their respective object types.
3. **Simulate Asynchronous Operations:** Mimic real-world API behavior with configurable response delays, status progressions, and timeouts.
4. **Support Webhooks and Endpoints:** Handle both webhook-based and endpoint-based delivery mechanisms as defined in the source configurations.
5. **Inject Errors:** Simulate various error conditions (timeouts, malformed responses, authentication failures) to test the robustness of the data pipeline.
6. **Comprehensive Logging:** Generate detailed logs for requests, responses, and errors, enabling cross-checking with backend ETL processes.

## Folder Structure

```
data/sources/
├── shared/                            # Common utilities and logging
│   ├── data-generators/               # Shared data generation helpers
│   └── logging/                       # Centralized logging functions
│
├── linkedin-people-dataset/
│   ├── linkedin-people-dataset.json   # Source detail configuration
│   ├── people.json                    # Sample data
│   ├── mappings.json                  # Field mappings
│   └── simulator/                     # LinkedIn People Dataset Simulator
│       ├── package.json               # Node.js dependencies
│       ├── server.js                  # Express.js application
│       ├── data-generators.js         # Specific data generation logic
│       └── README.md                  # Simulator-specific documentation
│
├── ai-company-researcher/
│   ├── ai-company-researcher.json
│   ├── companies.json
│   ├── mappings.json
│   └── simulator/                     # AI Company Researcher Simulator
│       ├── package.json
│       ├── server.js
│       ├── data-generators.js
│       └── README.md
│
├── real-estate-api/
│   ├── real-estate-api.json
│   ├── properties.json
│   ├── mappings.json
│   └── simulator/                     # Real Estate API Simulator
│       ├── package.json
│       ├── server.js
│       ├── data-generators.js
│       └── README.md
│
├── esg-agent/
│   └── simulator/                     # ESG Agent Simulator
│
├── job-market-scraper/
│   └── simulator/                     # Job Market Scraper Simulator
│
├── e-commerce-scraper/
│   └── simulator/                     # E-commerce Scraper Simulator
│
├── event-management/
│   └── simulator/                     # Event Management Simulator
│
├── automotive-database/
│   └── simulator/                     # Automotive Database Simulator
│
├── ml-model-trainer/
│   └── simulator/                     # ML Model Trainer Simulator
│
├── ml-model-inference/
│   └── simulator/                     # ML Model Inference Simulator
│
└── fireworks-finetune/
    └── simulator/                     # Fireworks Fine-tuning Simulator
```

## Running Simulators

To run a specific simulator:

1. Navigate to the simulator's directory:
   `cd data/sources/{source-name}/simulator/`
2. Install dependencies (if not already installed):
   `npm install`
3. Start the simulator:
   `npm start`

Each simulator will run on a unique port as defined in its `server.js` file and the `data-demo-generation-plan.md`.

## Port Assignments

- **LinkedIn People Dataset**: Port 3001
- **Real Estate API**: Port 3002
- **AI Company Researcher**: Port 3003
- **ESG Agent**: Port 3004
- **Job Market Scraper**: Port 3005
- **E-commerce Scraper**: Port 3006
- **Event Management**: Port 3007
- **Automotive Database**: Port 3008
- **ML Model Trainer**: Port 3009
- **ML Model Inference**: Port 3010
- **Fireworks Fine-tuning**: Port 3011

## Shared Utilities

- **`data/sources/shared/data-generators/index.js`**: Provides common data generation functions, such as `generateUUID()`, `generateRandomString()`, `generateRandomNumber()`, etc.
- **`data/sources/shared/logging/index.js`**: Offers standardized logging functions (`logRequest`, `logResponse`, `logError`) for consistent output across all simulators.

## Simulator Features

### Webhook-based Sources
- **AI Company Researcher** (Port 3003)
- **ESG Agent** (Port 3004)
- **Job Market Scraper** (Port 3005)
- **E-commerce Scraper** (Port 3006)
- **Event Management** (Port 3007)
- **Automotive Database** (Port 3008)
- **ML Model Inference** (Port 3010)

### Endpoint-based Sources
- **LinkedIn People Dataset** (Port 3001)
- **Real Estate API** (Port 3002)
- **ML Model Trainer** (Port 3009)
- **Fireworks Fine-tuning** (Port 3011)

## Data Generation Patterns

Each simulator generates data specific to its domain:

- **People**: Professional profiles with skills, experience, education
- **Companies**: Business information with financials, industry, location
- **Properties**: Real estate listings with pricing, features, location
- **ESG Data**: Environmental, social, and governance metrics
- **Job Posts**: Employment opportunities with requirements, benefits
- **Products**: E-commerce items with pricing, specifications, reviews
- **Events**: Conference and meeting information with schedules, speakers
- **Vehicles**: Automotive listings with specifications, pricing, history
- **ML Training Jobs**: Machine learning model training metadata
- **Inference Results**: ML model prediction outputs
- **Fine-tuning Jobs**: LLM fine-tuning process metadata

## Error Simulation

Simulators can be configured to simulate various error conditions:

- **Timeouts**: Configurable timeout durations for testing timeout handling
- **Authentication Failures**: Invalid API keys or authentication errors
- **Rate Limiting**: Simulated rate limit responses
- **Malformed Data**: Invalid JSON responses or missing required fields
- **Network Errors**: Connection failures and network timeouts

## Testing Scenarios

The simulators support various testing scenarios:

1. **Normal Operation**: Standard data generation and delivery
2. **High Volume**: Large datasets for performance testing
3. **Error Conditions**: Various failure modes for robustness testing
4. **Edge Cases**: Boundary conditions and unusual data patterns
5. **Concurrent Requests**: Multiple simultaneous requests for load testing

## Integration with Backend

Simulators are designed to integrate seamlessly with the AlgOps backend:

- **Webhook Delivery**: Simulate webhook callbacks to the backend
- **Status Polling**: Support status check endpoints for endpoint-based sources
- **Data Retrieval**: Provide data download endpoints for completed runs
- **Logging Integration**: Generate logs compatible with backend monitoring

## Development and Maintenance

- **Modular Design**: Each simulator is independent and can be modified without affecting others
- **Consistent Interface**: All simulators follow the same patterns for easy maintenance
- **Extensible**: New simulators can be added by following the established patterns
- **Configurable**: Timeouts, data volumes, and error rates can be easily adjusted
- **Well-Documented**: Each simulator includes comprehensive documentation

## Monitoring and Debugging

- **Structured Logging**: All requests, responses, and errors are logged with timestamps
- **Progress Tracking**: Real-time progress updates for long-running operations
- **Error Reporting**: Detailed error messages for debugging
- **Performance Metrics**: Response times and throughput monitoring
- **Health Checks**: Endpoint health monitoring for all simulators

This simulator system provides a comprehensive testing environment for the AlgOps data pipeline, enabling thorough validation of all data processing workflows before deployment to production.
