const express = require('express');
const bodyParser = require('body-parser');
const { v4: uuidv4 } = require('uuid');
const { generateInferenceResult } = require('./data-generators');
const { logRequest, logResponse, logError } = require('../../../shared/logging');

const app = express();
const PORT = 3010;
const SOURCE_NAME = 'ML Model Inference';
const TIMEOUT_DURATION = 300 * 1000; // 5 minutes

app.use(bodyParser.json());

const runs = {}; // Store active runs

// Health Check Endpoint
app.get('/api/health', (req, res) => {
    logRequest(SOURCE_NAME, '/api/health', 'GET', null);
    const response = {
        status: 'healthy',
        uptime: process.uptime(),
        source_type: 'ML Platform',
        max_concurrent_runs: 10,
        timeout: TIMEOUT_DURATION / 1000
    };
    logResponse(SOURCE_NAME, '/api/health', 'GET', response);
    res.json(response);
});

// Run Request Endpoint (Webhook-based with nested run_setup)
app.post('/api/2.0/mlflow/runs/create', (req, res) => {
    const { experiment_id, run_name, tags, webhook_url, run_id: external_run_id } = req.body;
    logRequest(SOURCE_NAME, '/api/2.0/mlflow/runs/create', 'POST', req.body);

    if (!external_run_id) {
        logError(SOURCE_NAME, '/api/2.0/mlflow/runs/create', 'POST', 'Missing run_id in request body');
        return res.status(400).json({ error: 'Missing run_id in request body' });
    }

    const internalRunId = uuidv4();
    const estimatedDuration = TIMEOUT_DURATION / 1000;

    runs[internalRunId] = {
        status: 'waiting',
        progress: 0,
        data: null,
        experiment_id,
        run_name,
        tags,
        webhook_url,
        external_run_id,
        estimatedDuration,
        createdAt: new Date(),
        startedAt: null,
        completedAt: null,
        timeoutTimer: null,
        dataGenerationTimer: null
    };

    const response = {
        status: 'waiting',
        run_id: internalRunId,
        estimated_duration: estimatedDuration
    };
    logResponse(SOURCE_NAME, '/api/2.0/mlflow/runs/create', 'POST', response);
    res.status(202).json(response);

    // Simulate status progression and data generation
    runs[internalRunId].dataGenerationTimer = setTimeout(() => {
        runs[internalRunId].startedAt = new Date();
        runs[internalRunId].status = 'inferencing'; // Custom status for ML Inference
        runs[internalRunId].progress = 20;

        // Simulate inference processing
        setTimeout(() => {
            runs[internalRunId].status = 'ready';
            runs[internalRunId].progress = 100;
            runs[internalRunId].completedAt = new Date();
            runs[internalRunId].data = generateInferenceResult(runs[internalRunId].tags);

            // Simulate webhook delivery
            if (runs[internalRunId].webhook_url) {
                console.log(`[${SOURCE_NAME}] Delivering results for run ${internalRunId} to webhook: ${runs[internalRunId].webhook_url}`);
                // In a real scenario, you'd make an HTTP POST request to the webhook_url
                // For simulation, we just log it.
            }
        }, faker.number.int({ min: 2000, max: 10000 })); // Quick inference processing

        runs[internalRunId].timeoutTimer = setTimeout(() => {
            if (runs[internalRunId].status !== 'ready' && runs[internalRunId].status !== 'completed') {
                runs[internalRunId].status = 'timedout';
                runs[internalRunId].completedAt = new Date();
                console.warn(`[${SOURCE_NAME}] Run ${internalRunId} timed out.`);
                logError(SOURCE_NAME, `/api/2.0/mlflow/runs/get`, 'GET', `Run ${internalRunId} timed out.`);
            }
        }, TIMEOUT_DURATION);

    }, faker.number.int({ min: 1000, max: 3000 })); // Initial delay before starting
});

// Status Check Endpoint (Internal, not directly used by webhook delivery)
app.get('/api/2.0/mlflow/runs/get', (req, res) => {
    const { run_id } = req.query;
    logRequest(SOURCE_NAME, '/api/2.0/mlflow/runs/get', 'GET', { run_id });

    const run = runs[run_id];
    if (!run) {
        logError(SOURCE_NAME, '/api/2.0/mlflow/runs/get', 'GET', `Run ${run_id} not found.`);
        return res.status(404).json({ error: 'Run not found' });
    }

    const response = {
        status: run.status,
        progress: run.progress,
        timestamp: new Date().toISOString()
    };
    logResponse(SOURCE_NAME, '/api/2.0/mlflow/runs/get', 'GET', response);
    res.json(response);
});

// Delivery Endpoint (Internal, not directly used by webhook delivery)
app.get('/api/2.0/mlflow/artifacts/download', (req, res) => {
    const { run_id } = req.query;
    logRequest(SOURCE_NAME, '/api/2.0/mlflow/artifacts/download', 'GET', { run_id });

    const run = runs[run_id];
    if (!run) {
        logError(SOURCE_NAME, '/api/2.0/mlflow/artifacts/download', 'GET', `Run ${run_id} not found.`);
        return res.status(404).json({ error: 'Run not found' });
    }

    if (run.status === 'ready' || run.status === 'completed') {
        const response = {
            status: 'ready',
            data: run.data,
            generated_at: run.completedAt.toISOString()
        };
        logResponse(SOURCE_NAME, '/api/2.0/mlflow/artifacts/download', 'GET', response);
        res.json(response);
    } else if (run.status === 'failed' || run.status === 'timedout') {
        logError(SOURCE_NAME, '/api/2.0/mlflow/artifacts/download', 'GET', `Run ${run_id} failed or timed out.`);
        res.status(500).json({ error: `Run ${run_id} ${run.status}` });
    } else {
        logError(SOURCE_NAME, '/api/2.0/mlflow/artifacts/download', 'GET', `Run ${run_id} not ready yet. Current status: ${run.status}`);
        res.status(409).json({ error: `Run ${run_id} not ready yet. Current status: ${run.status}` });
    }
});

app.listen(PORT, () => {
    console.log(`[${SOURCE_NAME}] Simulator running on port ${PORT}`);
});
