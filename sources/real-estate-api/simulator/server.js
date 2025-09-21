/**
 * Real Estate API Simulator Server
 * Simulates Real Estate API endpoints (webhook-based)
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { v4: uuidv4 } = require('uuid');
const RealEstateDataGenerator = require('./data-generators');
const { SimulatorLogger } = require('../../shared/logging');

const app = express();
const PORT = process.env.PORT || 3002;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Initialize components
const dataGenerator = new RealEstateDataGenerator();
const logger = new SimulatorLogger('real-estate-api');

// Store for active runs
const activeRuns = new Map();

/**
 * Health check endpoint
 */
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    source_type: 'Integration',
    max_concurrent_runs: 30,
    timeout: 78,
    simulator_name: 'real-estate-api'
  });
});

/**
 * Run request endpoint - POST /v1/properties/search
 */
app.post('/v1/properties/search', (req, res) => {
  const startTime = Date.now();
  const runId = uuidv4();
  
  try {
    const { filters, max_results = 300, callback_url, request_id } = req.body;
    
    // Validate request
    if (!filters) {
      return res.status(400).json({
        error: 'Invalid request',
        message: 'filters is required'
      });
    }
    
    // Store run information
    const runInfo = {
      id: runId,
      external_id: request_id || runId,
      status: 'waiting',
      created_at: new Date().toISOString(),
      estimated_duration: 78, // 78 seconds as per plan
      request_params: { filters, max_results, callback_url },
      webhook_url: callback_url
    };
    
    activeRuns.set(runId, runInfo);
    
    // Log API call
    logger.logApiCall(runId, '/v1/properties/search', 'POST', 'success', Date.now() - startTime);
    
    // Start background processing
    processRunAsync(runId, filters, max_results);
    
    // Return immediate response
    res.json({
      status: 'waiting',
      request_id: runId,
      estimated_duration: 78
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
 * Process run asynchronously (webhook-based, no status check endpoint)
 */
async function processRunAsync(runId, filters, maxResults) {
  const runInfo = activeRuns.get(runId);
  if (!runInfo) return;
  
  try {
    // Update status to in_progress
    runInfo.status = 'in_progress';
    runInfo.started_at = new Date().toISOString();
    
    logger.logStatusTransition(runId, 'waiting', 'in_progress', 0);
    
    // Simulate processing time (78 seconds as per plan)
    const processingTime = 78000; // 78 seconds
    await new Promise(resolve => setTimeout(resolve, processingTime));
    
    // Generate data
    const response = dataGenerator.generateApiResponse(filters, maxResults);
    
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
      'property', 
      response.total_records, 
      response.metadata.field_completeness, 
      response.metadata.data_quality
    );
    
    // Send webhook notification
    if (runInfo.webhook_url) {
      await sendWebhook(runId, runInfo);
    }
    
  } catch (error) {
    runInfo.status = 'failed';
    runInfo.error = error.message;
    runInfo.failed_at = new Date().toISOString();
    
    logger.logError(runId, 'data_generation', error.message, true, false);
    
    // Send error webhook if configured
    if (runInfo.webhook_url) {
      await sendErrorWebhook(runId, runInfo);
    }
  }
}

/**
 * Send webhook notification
 */
async function sendWebhook(runId, runInfo) {
  try {
    const webhookData = {
      request_id: runId,
      status: 'completed',
      total_records: runInfo.record_count,
      completed_at: runInfo.completed_at,
      data: runInfo.data,
      metadata: runInfo.metadata
    };
    
    // In a real implementation, this would make an HTTP request to the webhook URL
    console.log(`Webhook sent to ${runInfo.webhook_url}:`, JSON.stringify(webhookData, null, 2));
    
    // Log webhook delivery
    logger.logApiCall(runId, 'webhook_delivery', 'POST', 'success', 0, runInfo.record_count);
    
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
      request_id: runId,
      status: 'failed',
      error: runInfo.error,
      failed_at: runInfo.failed_at
    };
    
    // In a real implementation, this would make an HTTP request to the webhook URL
    console.log(`Error webhook sent to ${runInfo.webhook_url}:`, JSON.stringify(webhookData, null, 2));
    
    // Log error webhook delivery
    logger.logApiCall(runId, 'error_webhook_delivery', 'POST', 'success', 0);
    
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
  console.log(`Real Estate API Simulator running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`API endpoint: http://localhost:${PORT}/v1/properties/search`);
  console.log(`Delivery type: Webhook (no status check endpoint)`);
});

module.exports = app;
