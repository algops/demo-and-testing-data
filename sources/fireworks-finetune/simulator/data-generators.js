const { faker } = require('@faker-js/faker');
const { generateUUID } = require('../../../shared/data-generators');

function generateFineTuningJob(trainingData = {}) {
    const baseModels = ['llama-2-7b', 'llama-2-13b', 'llama-2-70b', 'mistral-7b', 'mistral-8x7b', 'codellama-7b', 'codellama-13b'];
    const statuses = ['queued', 'training', 'completed', 'failed', 'cancelled'];
    const baseModel = faker.helpers.arrayElement(baseModels);
    const status = faker.helpers.arrayElement(statuses);
    const startTime = faker.date.recent({ days: 14 });
    const endTime = status === 'completed' ? new Date(startTime.getTime() + faker.number.int({ min: 1800, max: 7200 }) * 1000) : null;
    
    return {
        id: generateUUID(),
        job_id: faker.string.uuid(),
        base_model: baseModel,
        fine_tuned_model: `${baseModel}-ft-${faker.string.alphanumeric(8)}`,
        status: status,
        start_time: startTime.toISOString(),
        end_time: endTime ? endTime.toISOString() : null,
        duration: endTime ? Math.floor((endTime - startTime) / 1000) : null,
        hyperparameters: {
            learning_rate: faker.number.float({ min: 0.0001, max: 0.01, fractionDigits: 5 }),
            batch_size: faker.helpers.arrayElement([1, 2, 4, 8, 16]),
            num_epochs: faker.number.int({ min: 1, max: 10 }),
            warmup_steps: faker.number.int({ min: 100, max: 1000 }),
            weight_decay: faker.number.float({ min: 0.01, max: 0.1, fractionDigits: 3 }),
            gradient_accumulation_steps: faker.number.int({ min: 1, max: 8 })
        },
        training_data: {
            total_examples: faker.number.int({ min: 100, max: 10000 }),
            prompt_tokens: faker.number.int({ min: 1000, max: 1000000 }),
            completion_tokens: faker.number.int({ min: 1000, max: 1000000 }),
            data_format: faker.helpers.arrayElement(['jsonl', 'csv', 'txt'])
        },
        metrics: {
            training_loss: faker.number.float({ min: 0.1, max: 2.0, fractionDigits: 4 }),
            validation_loss: faker.number.float({ min: 0.1, max: 2.0, fractionDigits: 4 }),
            perplexity: faker.number.float({ min: 1.0, max: 100.0, fractionDigits: 2 }),
            bleu_score: faker.number.float({ min: 0, max: 1, fractionDigits: 3 }),
            rouge_score: faker.number.float({ min: 0, max: 1, fractionDigits: 3 })
        },
        cost: {
            training_cost: faker.number.float({ min: 0.1, max: 100.0, fractionDigits: 2 }),
            inference_cost: faker.number.float({ min: 0.001, max: 0.1, fractionDigits: 4 }),
            currency: 'USD'
        },
        artifacts: {
            model_path: `s3://fireworks-models/${faker.string.uuid()}/`,
            logs_path: `s3://fireworks-logs/${faker.string.uuid()}/`,
            checkpoints_path: `s3://fireworks-checkpoints/${faker.string.uuid()}/`
        },
        tags: {
            project: faker.lorem.word(),
            team: faker.helpers.arrayElement(['AI Team', 'Research', 'Engineering', 'Product']),
            environment: faker.helpers.arrayElement(['dev', 'staging', 'prod']),
            priority: faker.helpers.arrayElement(['low', 'medium', 'high', 'critical'])
        },
        created_at: faker.date.recent({ days: 14 }).toISOString(),
        updated_at: faker.date.recent({ days: 1 }).toISOString()
    };
}

module.exports = {
    generateFineTuningJob
};
