function logRequest(sourceName, endpoint, method, body) {
    console.log(`[${sourceName} - ${new Date().toISOString()}] REQUEST: ${method} ${endpoint}`);
    if (body) {
        console.log(`  Body: ${JSON.stringify(body)}`);
    }
}

function logResponse(sourceName, endpoint, method, response) {
    console.log(`[${sourceName} - ${new Date().toISOString()}] RESPONSE: ${method} ${endpoint}`);
    console.log(`  Status: ${response.status}`);
    if (response.run_id) {
        console.log(`  Run ID: ${response.run_id}`);
    }
    if (response.request_id) {
        console.log(`  Request ID: ${response.request_id}`);
    }
    if (response.job_id) {
        console.log(`  Job ID: ${response.job_id}`);
    }
    if (response.estimated_duration) {
        console.log(`  Estimated Duration: ${response.estimated_duration}s`);
    }
    if (response.progress !== undefined) {
        console.log(`  Progress: ${response.progress}%`);
    }
    if (response.total_records !== undefined) {
        console.log(`  Total Records: ${response.total_records}`);
    }
}

function logError(sourceName, endpoint, method, errorMessage) {
    console.error(`[${sourceName} - ${new Date().toISOString()}] ERROR: ${method} ${endpoint}`);
    console.error(`  Message: ${errorMessage}`);
}

module.exports = {
    logRequest,
    logResponse,
    logError
};
