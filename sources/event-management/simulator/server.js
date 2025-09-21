const express = require('express');
const bodyParser = require('body-parser');
const { v4: uuidv4 } = require('uuid');
const { generateEvent } = require('./data-generators');
const { logRequest, logResponse, logError } = require('../../../shared/logging');

const app = express();
const PORT = 3007;
const SOURCE_NAME = 'Event Management';
const TIMEOUT_DURATION = 70 * 1000; // 70 seconds

app.use(bodyParser.json());

const runs = {}; // Store active runs

// Health Check Endpoint
app.get('/api/health', (req, res) => {
    logRequest(SOURCE_NAME, '/api/health', 'GET', null);
    const response = {
        status: 'healthy',
        uptime: process.uptime(),
        source_type: 'Integration',
        max_concurrent_runs: 20,
        timeout: TIMEOUT_DURATION / 1000
    };
    logResponse(SOURCE_NAME, '/api/health', 'GET', response);
    res.json(response);
});

// Run Request Endpoint (Webhook-based)
app.post('/v1/events/search', (req, res) => {
    const { filters, max_results, callback_url, request_id: external_run_id } = req.body;
    logRequest(SOURCE_NAME, '/v1/events/search', 'POST', req.body);

    if (!external_run_id) {
        logError(SOURCE_NAME, '/v1/events/search', 'POST', 'Missing request_id in request body');
        return res.status(400).json({ error: 'Missing request_id in request body' });
    }

    const internalRunId = uuidv4();
    const estimatedDuration = TIMEOUT_DURATION / 1000;

    runs[internalRunId] = {
        status: 'waiting',
        progress: 0,
        data: [],
        filters,
        max_objects: max_results || 40,
        webhook_url: callback_url,
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
        request_id: internalRunId,
        estimated_duration: estimatedDuration
    };
    logResponse(SOURCE_NAME, '/v1/events/search', 'POST', response);
    res.status(202).json(response);

    // Simulate status progression and data generation
    runs[internalRunId].dataGenerationTimer = setTimeout(() => {
        runs[internalRunId].startedAt = new Date();
        runs[internalRunId].status = 'in_progress';
        runs[internalRunId].progress = 20;

        let generatedCount = 0;
        const interval = setInterval(() => {
            if (generatedCount < runs[internalRunId].max_objects) {
                runs[internalRunId].data.push(generateEvent(runs[internalRunId].filters));
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
                logError(SOURCE_NAME, `/v1/requests/${internalRunId}/status`, 'GET', `Run ${internalRunId} timed out.`);
            }
        }, TIMEOUT_DURATION);

    }, faker.number.int({ min: 1000, max: 5000 }));
});

// Status Check Endpoint
app.get('/v1/requests/:run_id/status', (req, res) => {
    const { run_id } = req.params;
    logRequest(SOURCE_NAME, `/v1/requests/${run_id}/status`, 'GET', null);

    const run = runs[run_id];
    if (!run) {
        logError(SOURCE_NAME, `/v1/requests/${run_id}/status`, 'GET', `Run ${run_id} not found.`);
        return res.status(404).json({ error: 'Run not found' });
    }

    const response = {
        status: run.status,
        progress: run.progress,
        timestamp: new Date().toISOString()
    };
    logResponse(SOURCE_NAME, `/v1/requests/${run_id}/status`, 'GET', response);
    res.json(response);
});

// Delivery Endpoint
app.get('/v1/requests/:run_id/results', (req, res) => {
    const { run_id } = req.params;
    logRequest(SOURCE_NAME, `/v1/requests/${run_id}/results`, 'GET', null);

    const run = runs[run_id];
    if (!run) {
        logError(SOURCE_NAME, `/v1/requests/${run_id}/results`, 'GET', `Run ${run_id} not found.`);
        return res.status(404).json({ error: 'Run not found' });
    }

    if (run.status === 'ready' || run.status === 'completed') {
        const response = {
            status: 'done',
            data: run.data,
            total_records: run.data.length,
            generated_at: run.completedAt.toISOString()
        };
        logResponse(SOURCE_NAME, `/v1/requests/${run_id}/results`, 'GET', response);
        res.json(response);
    } else if (run.status === 'failed' || run.status === 'timedout') {
        logError(SOURCE_NAME, `/v1/requests/${run_id}/results`, 'GET', `Run ${run_id} failed or timed out.`);
        res.status(500).json({ error: `Run ${run_id} ${run.status}` });
    } else {
        logError(SOURCE_NAME, `/v1/requests/${run_id}/results`, 'GET', `Run ${run_id} not ready yet. Current status: ${run.status}`);
        res.status(409).json({ error: `Run ${run_id} not ready yet. Current status: ${run.status}` });
    }
});

app.listen(PORT, () => {
    console.log(`[${SOURCE_NAME}] Simulator running on port ${PORT}`);
});
