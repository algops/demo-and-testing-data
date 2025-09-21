/**
 * LinkedIn People Dataset Simulator Server
 * Simulates LinkedIn People Dataset API endpoints
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { v4: uuidv4 } = require('uuid');
const LinkedInDataGenerator = require('./data-generators');
const { SimulatorLogger } = require('../../shared/logging');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Initialize components
const dataGenerator = new LinkedInDataGenerator();
const logger = new SimulatorLogger('linkedin-people-dataset');

// Store for active runs
const activeRuns = new Map();

/**
 * Health check endpoint
 */
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    source_type: 'Dataset',
    max_concurrent_runs: 50,
    timeout: 60,
    simulator_name: 'linkedin-people-dataset'
  });
});

/**
 * Run request endpoint - POST /v2/people/search
 */
app.post('/v2/people/search', (req, res) => {
  const startTime = Date.now();
  const runId = uuidv4();
  
  try {
    const { filter, max_objects = 500, webhook_url, run_id } = req.body;
    
    // Validate request
    if (!filter || !filter.filters) {
      return res.status(400).json({
        error: 'Invalid request',
        message: 'filter.filters is required'
      });
    }
    
    // Store run information
    const runInfo = {
      id: runId,
      external_id: run_id || runId,
      status: 'waiting',
      created_at: new Date().toISOString(),
      estimated_duration: 45, // 45 seconds as per plan
      request_params: { filter, max_objects, webhook_url },
      webhook_url: webhook_url
    };
    
    activeRuns.set(runId, runInfo);
    
    // Log API call
    logger.logApiCall(runId, '/v2/people/search', 'POST', 'success', Date.now() - startTime);
    
    // Start background processing
    processRunAsync(runId, filter, max_objects);
    
    // Return immediate response
    res.json({
      status: 'waiting',
      run_id: runId,
      estimated_duration: 45
    });
    
  } catch (error) {
    logger.logError(runId, 'request_processing', error.message);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

/**
 * Status check endpoint - GET /v2/runs/:runId/status
 */
app.get('/v2/runs/:runId/status', (req, res) => {
  const { runId } = req.params;
  const startTime = Date.now();
  
  try {
    const runInfo = activeRuns.get(runId);
    
    if (!runInfo) {
      return res.status(404).json({
        error: 'Run not found',
        message: `Run ${runId} does not exist`
      });
    }
    
    // Log status check
    logger.logApiCall(runId, `/v2/runs/${runId}/status`, 'GET', 'success', Date.now() - startTime);
    
    // Calculate progress based on elapsed time
    const elapsed = Date.now() - new Date(runInfo.created_at).getTime();
    const progress = Math.min(Math.floor((elapsed / (runInfo.estimated_duration * 1000)) * 100), 100);
    
    res.json({
      status: runInfo.status,
      progress: progress,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    logger.logError(runId, 'status_check', error.message);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

/**
 * Delivery endpoint - GET /v2/runs/:runId/download
 */
app.get('/v2/runs/:runId/download', (req, res) => {
  const { runId } = req.params;
  const startTime = Date.now();
  
  try {
    const runInfo = activeRuns.get(runId);
    
    if (!runInfo) {
      return res.status(404).json({
        error: 'Run not found',
        message: `Run ${runId} does not exist`
      });
    }
    
    if (runInfo.status !== 'ready') {
      return res.status(400).json({
        error: 'Run not ready',
        message: `Run ${runId} is not ready for download`
      });
    }
    
    // Log delivery request
    logger.logApiCall(runId, `/v2/runs/${runId}/download`, 'GET', 'success', Date.now() - startTime, runInfo.record_count);
    
    res.json({
      status: 'done',
      data: runInfo.data,
      total_records: runInfo.record_count,
      generated_at: runInfo.completed_at
    });
    
  } catch (error) {
    logger.logError(runId, 'delivery', error.message);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

/**
 * Process run asynchronously
 */
async function processRunAsync(runId, filter, maxObjects) {
  const runInfo = activeRuns.get(runId);
  if (!runInfo) return;
  
  try {
    // Update status to in_progress
    runInfo.status = 'in_progress';
    runInfo.started_at = new Date().toISOString();
    
    logger.logStatusTransition(runId, 'waiting', 'in_progress', 0);
    
    // Simulate processing time (45 seconds as per plan)
    const processingTime = 45000; // 45 seconds
    await new Promise(resolve => setTimeout(resolve, processingTime));
    
    // Generate data
    const response = dataGenerator.generateApiResponse(filter, maxObjects);
    
    // Update run info with results
    runInfo.status = 'ready';
    runInfo.data = response.data;
    runInfo.record_count = response.total_records;
    runInfo.completed_at = new Date().toISOString();
    runInfo.metadata = response.metadata;
    
    logger.logStatusTransition(runId, 'in_progress', 'ready', processingTime);
    
    // Log data generation
    logger.logDataGeneration(
      runId, 
      'person', 
      response.total_records, 
      response.metadata.field_completeness, 
      response.metadata.data_quality
    );
    
    // Send webhook if configured
    if (runInfo.webhook_url) {
      sendWebhook(runId, runInfo);
    }
    
  } catch (error) {
    runInfo.status = 'failed';
    runInfo.error = error.message;
    runInfo.failed_at = new Date().toISOString();
    
    logger.logError(runId, 'data_generation', error.message, true, false);
    
    // Send error webhook if configured
    if (runInfo.webhook_url) {
      sendErrorWebhook(runId, runInfo);
    }
  }
}

/**
 * Send webhook notification
 */
async function sendWebhook(runId, runInfo) {
  try {
    const webhookData = {
      run_id: runId,
      status: 'completed',
      total_records: runInfo.record_count,
      completed_at: runInfo.completed_at,
      data: runInfo.data
    };
    
    // In a real implementation, this would make an HTTP request to the webhook URL
    console.log(`Webhook sent to ${runInfo.webhook_url}:`, JSON.stringify(webhookData, null, 2));
    
  } catch (error) {
    logger.logError(runId, 'webhook_delivery', error.message);
  }
}

/**
 * Send error webhook notification
 */
async function sendErrorWebhook(runId, runInfo) {
  try {
    const webhookData = {
      run_id: runId,
      status: 'failed',
      error: runInfo.error,
      failed_at: runInfo.failed_at
    };
    
    // In a real implementation, this would make an HTTP request to the webhook URL
    console.log(`Error webhook sent to ${runInfo.webhook_url}:`, JSON.stringify(webhookData, null, 2));
    
  } catch (error) {
    logger.logError(runId, 'error_webhook_delivery', error.message);
  }
}

/**
 * Cleanup old runs periodically
 */
setInterval(() => {
  const now = Date.now();
  const maxAge = 24 * 60 * 60 * 1000; // 24 hours
  
  for (const [runId, runInfo] of activeRuns.entries()) {
    const runAge = now - new Date(runInfo.created_at).getTime();
    if (runAge > maxAge) {
      activeRuns.delete(runId);
    }
  }
}, 60 * 60 * 1000); // Cleanup every hour

/**
 * Graceful shutdown
 */
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});

// Start server
app.listen(PORT, () => {
  console.log(`LinkedIn People Dataset Simulator running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`API endpoint: http://localhost:${PORT}/v2/people/search`);
});

module.exports = app;
