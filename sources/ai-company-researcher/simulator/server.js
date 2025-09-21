/**
 * AI Company Researcher Simulator Server
 * Simulates AI Company Researcher API endpoints (webhook-based)
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const { v4: uuidv4 } = require('uuid');
const AICompanyResearcherGenerator = require('./data-generators');
const { SimulatorLogger } = require('../../shared/logging');

const app = express();
const PORT = process.env.PORT || 3003;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Initialize components
const dataGenerator = new AICompanyResearcherGenerator();
const logger = new SimulatorLogger('ai-company-researcher');

// Store for active runs
const activeRuns = new Map();

/**
 * Health check endpoint
 */
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    uptime: process.uptime(),
    source_type: 'Agent',
    max_concurrent_runs: 5,
    timeout: 180,
    simulator_name: 'ai-company-researcher'
  });
});

/**
 * Run request endpoint - POST /api/analyze
 */
app.post('/api/analyze', (req, res) => {
  const startTime = Date.now();
  const runId = uuidv4();
  
  try {
    const { query, webhook_url, run_id } = req.body;
    
    // Validate request
    if (!query) {
      return res.status(400).json({
        error: 'Invalid request',
        message: 'query is required'
      });
    }
    
    // Store run information
    const runInfo = {
      id: runId,
      external_id: run_id || runId,
      status: 'waiting',
      created_at: new Date().toISOString(),
      estimated_duration: 95, // 95 seconds as per plan
      request_params: { query, webhook_url },
      webhook_url: webhook_url
    };
    
    activeRuns.set(runId, runInfo);
    
    // Log API call
    logger.logApiCall(runId, '/api/analyze', 'POST', 'success', Date.now() - startTime);
    
    // Start background processing
    processRunAsync(runId, query);
    
    // Return immediate response
    res.json({
      status: 'waiting',
      run_id: runId,
      estimated_duration: 95
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
async function processRunAsync(runId, query) {
  const runInfo = activeRuns.get(runId);
  if (!runInfo) return;
  
  try {
    // Update status to processing
    runInfo.status = 'processing';
    runInfo.started_at = new Date().toISOString();
    
    logger.logStatusTransition(runId, 'waiting', 'processing', 0);
    
    // Simulate processing time (95 seconds as per plan)
    const processingTime = 95000; // 95 seconds
    await new Promise(resolve => setTimeout(resolve, processingTime));
    
    // Generate data
    const response = dataGenerator.generateApiResponse(query, 100);
    
    // Update run info with results
    runInfo.status = 'ready';
    runInfo.data = response.data;
    runInfo.record_count = response.total_records;
    runInfo.completed_at = new Date().toISOString();
    runInfo.metadata = response.metadata;
    
    logger.logStatusTransition(runId, 'processing', 'ready', processingTime);
    
    // Log data generation
    logger.logDataGeneration(
      runId, 
      'company', 
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
      run_id: runId,
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
      run_id: runId,
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
  console.log(`AI Company Researcher Simulator running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log(`API endpoint: http://localhost:${PORT}/api/analyze`);
  console.log(`Delivery type: Webhook (no status check endpoint)`);
});

module.exports = app;
