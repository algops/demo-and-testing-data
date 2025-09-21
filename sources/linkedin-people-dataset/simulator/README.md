# LinkedIn People Dataset Simulator

This simulator provides realistic API endpoints that match the LinkedIn People Dataset source configuration for testing data pipelines.

## Features

- **Realistic Data Generation**: Generates person profiles with professional information
- **API Compatibility**: Matches exact LinkedIn API patterns from source templates
- **Comprehensive Logging**: Detailed logs for cross-checking with backend ETL
- **Filter Support**: Supports location, experience, skills, department, and role filters
- **Webhook Integration**: Sends completion notifications via webhooks

## API Endpoints

### Health Check
```
GET /api/health
```
Returns simulator status and configuration.

### Run Request
```
POST /v2/people/search
```
Initiates a people search request.

**Request Body:**
```json
{
  "filter": {
    "filters": {
      "location": "San Francisco",
      "experience_years": ">5",
      "skills": ["Python", "JavaScript"],
      "department": "Engineering"
    }
  },
  "max_objects": 500,
  "webhook_url": "https://callback.example.com/webhook",
  "run_id": "unique-run-id"
}
```

**Response:**
```json
{
  "status": "waiting",
  "run_id": "generated-run-id",
  "estimated_duration": 45
}
```

### Status Check
```
GET /v2/runs/{runId}/status
```
Checks the status of a running request.

**Response:**
```json
{
  "status": "in_progress",
  "progress": 75,
  "timestamp": "2025-01-20T10:30:00Z"
}
```

### Data Delivery
```
GET /v2/runs/{runId}/download
```
Downloads the generated data when ready.

**Response:**
```json
{
  "status": "done",
  "data": [...],
  "total_records": 150,
  "generated_at": "2025-01-20T10:35:00Z"
}
```

## Data Generation

### Person Object Fields
- `name`: Full name
- `email`: Email address (derived from name)
- `phone`: US phone number with area code
- `linkedin`: LinkedIn profile URL
- `skills`: Array of professional skills
- `experience_years`: Years of experience (1-25)
- `role`: Job role/position
- `department`: Department name
- `salary`: Annual salary ($50k-$200k)
- `hourly_rate`: Hourly rate for contractors ($25-$125)
- `education`: Education background
- `specialization`: Professional specialization

### LinkedIn-Specific Enhancements
- `linkedin_profile_views`: Profile view count
- `connections_count`: Number of connections
- `endorsements_count`: Skill endorsements
- `recommendations_count`: Recommendations received
- `current_company`: Company derived from email domain
- `location`: Location derived from phone area code
- `profile_completeness`: Profile completeness percentage
- `last_activity`: Last activity date

## Filter Support

### Location Filter
Matches records based on city location:
```json
{
  "location": "San Francisco"
}
```

### Experience Filter
Supports various experience year formats:
```json
{
  "experience_years": ">5"     // More than 5 years
  "experience_years": "<10"    // Less than 10 years
  "experience_years": "3-7"    // Between 3 and 7 years
  "experience_years": "5"      // Around 5 years (±2)
}
```

### Skills Filter
Matches records with any of the specified skills:
```json
{
  "skills": ["Python", "JavaScript", "React"]
}
```

### Department Filter
Matches records by department:
```json
{
  "department": "Engineering"
}
```

### Role Filter
Matches records by job role:
```json
{
  "role": "Software Engineer"
}
```

## Configuration

### Environment Variables
- `PORT`: Server port (default: 3001)
- `NODE_ENV`: Environment (development/production)

### Performance Settings
- **Max Records**: 500 per request
- **Processing Time**: 45 seconds
- **Concurrent Runs**: 50
- **Timeout**: 60 seconds

## Logging

The simulator generates comprehensive logs in JSON format for cross-checking with backend ETL:

### Log Types
- **API Calls**: Request/response logging with correlation IDs
- **Data Generation**: Record counts, field completeness, data quality metrics
- **Performance**: Response times, generation duration, throughput
- **Status Transitions**: Status change tracking with timing
- **Errors**: Error logging with recovery attempts

### Log Format
```json
{
  "run_id": "uuid",
  "timestamp": "2025-01-20T10:30:00.000Z",
  "simulator_name": "linkedin-people-dataset",
  "event_type": "api_call",
  "endpoint": "/v2/people/search",
  "method": "POST",
  "status": "success",
  "duration_ms": 150,
  "record_count": 150
}
```

## Installation

```bash
cd ui/data/sources/linkedin-people-dataset/simulator
npm install
```

## Usage

### Development
```bash
npm run dev
```

### Production
```bash
npm start
```

## Testing

```bash
npm test
```

## Integration

This simulator is designed to work with the AlgOps data pipeline:

1. **Edge Functions**: Maps real LinkedIn API URLs to localhost:3001
2. **Database**: Generates data compatible with the `value` table schema
3. **Activities**: Links generated data to activity runs and workflow executions
4. **Webhooks**: Sends completion notifications for webhook-based sources

## Error Handling

The simulator includes comprehensive error handling:

- **Validation Errors**: Invalid request parameters
- **Processing Errors**: Data generation failures
- **Webhook Errors**: Failed webhook deliveries
- **Recovery**: Automatic retry with exponential backoff

## Monitoring

Monitor simulator performance through:

- Health check endpoint for uptime
- Log analysis for performance metrics
- Error rate tracking
- Data quality metrics
