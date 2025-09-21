const express = require('express');
const bodyParser = require('body-parser');
const { v4: uuidv4 } = require('uuid');
const { generateFineTuningJob } = require('./data-generators');
const { logRequest, logResponse, logError } = require('../../../shared/logging');

const app = express();
const PORT = 3011;
const SOURCE_NAME = 'Fireworks Fine-tuning';
const TIMEOUT_DURATION = 3600 * 1000; // 60 minutes

app.use(bodyParser.json());

const runs = {}; // Store active runs

// Health Check Endpoint
app.get('/api/health', (req, res) => {
    logRequest(SOURCE_NAME, '/api/health', 'GET', null);
    const response = {
        status: 'healthy',
        uptime: process.uptime(),
        source_type: 'LLM Platform',
        max_concurrent_runs: 2,
        timeout: TIMEOUT_DURATION / 1000
    };
    logResponse(SOURCE_NAME, '/api/health', 'GET', response);
    res.json(response);
});

// Run Request Endpoint (Endpoint-based with parent run_setup)
app.post('/inference/v1/fine_tuning/jobs', (req, res) => {
    const { model, training_data, hyperparameters, webhook_url, job_id: external_run_id } = req.body;
    logRequest(SOURCE_NAME, '/inference/v1/fine_tuning/jobs', 'POST', req.body);

    if (!external_run_id) {
        logError(SOURCE_NAME, '/inference/v1/fine_tuning/jobs', 'POST', 'Missing job_id in request body');
        return res.status(400).json({ error: 'Missing job_id in request body' });
    }

    const internalRunId = uuidv4();
    const estimatedDuration = TIMEOUT_DURATION / 1000;

    runs[internalRunId] = {
        status: 'waiting',
        progress: 0,
        data: null,
        model,
        training_data,
        hyperparameters,
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
        status: 'queued', // Custom status for Fireworks
        job_id: internalRunId,
        estimated_duration: estimatedDuration
    };
    logResponse(SOURCE_NAME, '/inference/v1/fine_tuning/jobs', 'POST', response);
    res.status(202).json(response);

    // Simulate status progression and data generation
    runs[internalRunId].dataGenerationTimer = setTimeout(() => {
        runs[internalRunId].startedAt = new Date();
        runs[internalRunId].status = 'training'; // Custom status for Fireworks
        runs[internalRunId].progress = 20;

        // Simulate training progress
        let progress = 20;
        const progressInterval = setInterval(() => {
            if (progress < 90) {
                progress += faker.number.int({ min: 2, max: 8 });
                runs[internalRunId].progress = Math.min(90, progress);
            } else {
                clearInterval(progressInterval);
                runs[internalRunId].status = 'ready';
                runs[internalRunId].progress = 100;
                runs[internalRunId].completedAt = new Date();
                runs[internalRunId].data = generateFineTuningJob(runs[internalRunId].training_data);

                // Simulate webhook delivery
                if (runs[internalRunId].webhook_url) {
                    console.log(`[${SOURCE_NAME}] Delivering results for run ${internalRunId} to webhook: ${runs[internalRunId].webhook_url}`);
                    // In a real scenario, you'd make an HTTP POST request to the webhook_url
                    // For simulation, we just log it.
                }
            }
        }, TIMEOUT_DURATION / 20); // Distribute progress over 20 intervals

        runs[internalRunId].timeoutTimer = setTimeout(() => {
            if (runs[internalRunId].status !== 'ready' && runs[internalRunId].status !== 'completed') {
                runs[internalRunId].status = 'timedout';
                runs[internalRunId].completedAt = new Date();
                clearInterval(progressInterval);
                console.warn(`[${SOURCE_NAME}] Run ${internalRunId} timed out.`);
                logError(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${internalRunId}`, 'GET', `Run ${internalRunId} timed out.`);
            }
        }, TIMEOUT_DURATION);

    }, faker.number.int({ min: 10000, max: 30000 })); // Initial delay before starting
});

// Status Check Endpoint
app.get('/inference/v1/fine_tuning/jobs/:job_id', (req, res) => {
    const { job_id } = req.params;
    logRequest(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${job_id}`, 'GET', null);

    const run = runs[job_id];
    if (!run) {
        logError(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${job_id}`, 'GET', `Job ${job_id} not found.`);
        return res.status(404).json({ error: 'Job not found' });
    }

    const response = {
        status: run.status,
        progress: run.progress,
        timestamp: new Date().toISOString()
    };
    logResponse(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${job_id}`, 'GET', response);
    res.json(response);
});

// Delivery Endpoint
app.get('/inference/v1/fine_tuning/jobs/:job_id/model', (req, res) => {
    const { job_id } = req.params;
    logRequest(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${job_id}/model`, 'GET', null);

    const run = runs[job_id];
    if (!run) {
        logError(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${job_id}/model`, 'GET', `Job ${job_id} not found.`);
        return res.status(404).json({ error: 'Job not found' });
    }

    if (run.status === 'ready' || run.status === 'completed') {
        const response = {
            status: 'done',
            data: run.data,
            generated_at: run.completedAt.toISOString()
        };
        logResponse(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${job_id}/model`, 'GET', response);
        res.json(response);
    } else if (run.status === 'failed' || run.status === 'timedout') {
        logError(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${job_id}/model`, 'GET', `Job ${job_id} failed or timed out.`);
        res.status(500).json({ error: `Job ${job_id} ${run.status}` });
    } else {
        logError(SOURCE_NAME, `/inference/v1/fine_tuning/jobs/${job_id}/model`, 'GET', `Job ${job_id} not ready yet. Current status: ${run.status}`);
        res.status(409).json({ error: `Job ${job_id} not ready yet. Current status: ${run.status}` });
    }
});

app.listen(PORT, () => {
    console.log(`[${SOURCE_NAME}] Simulator running on port ${PORT}`);
});
