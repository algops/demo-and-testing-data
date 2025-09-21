const express = require('express');
const bodyParser = require('body-parser');
const { v4: uuidv4 } = require('uuid');
const { generateESGData } = require('./data-generators');
const { logRequest, logResponse, logError } = require('../../../shared/logging');

const app = express();
const PORT = 3004;
const SOURCE_NAME = 'ESG Agent';
const TIMEOUT_DURATION = 120 * 1000; // 120 seconds

app.use(bodyParser.json());

const runs = {}; // Store active runs

// Health Check Endpoint
app.get('/api/health', (req, res) => {
    logRequest(SOURCE_NAME, '/api/health', 'GET', null);
    const response = {
        status: 'healthy',
        uptime: process.uptime(),
        source_type: 'Agent',
        max_concurrent_runs: 8,
        timeout: TIMEOUT_DURATION / 1000
    };
    logResponse(SOURCE_NAME, '/api/health', 'GET', response);
    res.json(response);
});

// Run Request Endpoint (Webhook-based)
app.post('/api/analyze', (req, res) => {
    const { query, webhook_url, run_id: external_run_id } = req.body;
    logRequest(SOURCE_NAME, '/api/analyze', 'POST', req.body);

    if (!external_run_id) {
        logError(SOURCE_NAME, '/api/analyze', 'POST', 'Missing run_id in request body');
        return res.status(400).json({ error: 'Missing run_id in request body' });
    }

    const internalRunId = uuidv4();
    const estimatedDuration = TIMEOUT_DURATION / 1000;

    runs[internalRunId] = {
        status: 'waiting',
        progress: 0,
        data: [],
        query,
        webhook_url,
        external_run_id,
        estimatedDuration,
        createdAt: new Date(),
        startedAt: null,
        completedAt: null,
        timeoutTimer: null,
        dataGenerationTimer: null,
        max_objects: faker.number.int({ min: 15, max: 150 }) // Randomize max objects for this webhook source
    };

    const response = {
        status: 'waiting',
        run_id: internalRunId,
        estimated_duration: estimatedDuration
    };
    logResponse(SOURCE_NAME, '/api/analyze', 'POST', response);
    res.status(202).json(response);

    // Simulate status progression and data generation
    runs[internalRunId].dataGenerationTimer = setTimeout(() => {
        runs[internalRunId].startedAt = new Date();
        runs[internalRunId].status = 'analyzing'; // Custom status for ESG Agent
        runs[internalRunId].progress = 20;

        let generatedCount = 0;
        const interval = setInterval(() => {
            if (generatedCount < runs[internalRunId].max_objects) {
                runs[internalRunId].data.push(generateESGData(runs[internalRunId].query));
                generatedCount++;
                runs[internalRunId].progress = Math.min(90, Math.floor((generatedCount / runs[internalRunId].max_objects) * 100));
            } else {
                clearInterval(interval);
                runs[internalRunId].status = 'ready';
                runs[internalRunId].progress = 100;
                runs[internalRunId].completedAt = new Date();

                // Simulate webhook delivery
                if (runs[internalRunId].webhook_url) {
                    console.log(`[${SOURCE_NAME}] Delivering results for run ${internalRunId} to webhook: ${runs[internalRunId].webhook_url}`);
                    // In a real scenario, you'd make an HTTP POST request to the webhook_url
                    // For simulation, we just log it.
                }
            }
        }, TIMEOUT_DURATION / runs[internalRunId].max_objects);

        runs[internalRunId].timeoutTimer = setTimeout(() => {
            if (runs[internalRunId].status !== 'ready' && runs[internalRunId].status !== 'completed') {
                runs[internalRunId].status = 'timedout';
                runs[internalRunId].completedAt = new Date();
                clearInterval(interval);
                console.warn(`[${SOURCE_NAME}] Run ${internalRunId} timed out.`);
                logError(SOURCE_NAME, `/api/status/${internalRunId}`, 'GET', `Run ${internalRunId} timed out.`);
            }
        }, TIMEOUT_DURATION);

    }, faker.number.int({ min: 1000, max: 5000 }));
});

// Status Check Endpoint (Internal, not directly used by webhook delivery)
app.get('/api/status/:run_id', (req, res) => {
    const { run_id } = req.params;
    logRequest(SOURCE_NAME, `/api/status/${run_id}`, 'GET', null);

    const run = runs[run_id];
    if (!run) {
        logError(SOURCE_NAME, `/api/status/${run_id}`, 'GET', `Run ${run_id} not found.`);
        return res.status(404).json({ error: 'Run not found' });
    }

    const response = {
        status: run.status,
        progress: run.progress,
        timestamp: new Date().toISOString()
    };
    logResponse(SOURCE_NAME, `/api/status/${run_id}`, 'GET', response);
    res.json(response);
});

// Delivery Endpoint (Internal, not directly used by webhook delivery)
app.get('/api/delivery/:run_id', (req, res) => {
    const { run_id } = req.params;
    logRequest(SOURCE_NAME, `/api/delivery/${run_id}`, 'GET', null);

    const run = runs[run_id];
    if (!run) {
        logError(SOURCE_NAME, `/api/delivery/${run_id}`, 'GET', `Run ${run_id} not found.`);
        return res.status(404).json({ error: 'Run not found' });
    }

    if (run.status === 'ready' || run.status === 'completed') {
        const response = {
            status: 'ready',
            data: run.data,
            total_records: run.data.length,
            generated_at: run.completedAt.toISOString()
        };
        logResponse(SOURCE_NAME, `/api/delivery/${run_id}`, 'GET', response);
        res.json(response);
    } else if (run.status === 'failed' || run.status === 'timedout') {
        logError(SOURCE_NAME, `/api/delivery/${run_id}`, 'GET', `Run ${run_id} failed or timed out.`);
        res.status(500).json({ error: `Run ${run_id} ${run.status}` });
    } else {
        logError(SOURCE_NAME, `/api/delivery/${run_id}`, 'GET', `Run ${run_id} not ready yet. Current status: ${run.status}`);
        res.status(409).json({ error: `Run ${run_id} not ready yet. Current status: ${run.status}` });
    }
});

app.listen(PORT, () => {
    console.log(`[${SOURCE_NAME}] Simulator running on port ${PORT}`);
});
