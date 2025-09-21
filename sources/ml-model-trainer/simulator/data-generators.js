const { faker } = require('@faker-js/faker');
const { generateUUID } = require('../../../shared/data-generators');

function generateTrainingJob(trainingData = {}) {
    const modelTypes = ['Linear Regression', 'Random Forest', 'Neural Network', 'SVM', 'XGBoost', 'LSTM', 'Transformer', 'CNN'];
    const frameworks = ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'XGBoost', 'LightGBM', 'CatBoost'];
    const statuses = ['queued', 'training', 'completed', 'failed', 'cancelled'];
    const metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'auc', 'mse', 'mae', 'r2_score'];
    
    const modelType = faker.helpers.arrayElement(modelTypes);
    const framework = faker.helpers.arrayElement(frameworks);
    const status = faker.helpers.arrayElement(statuses);
    const startTime = faker.date.recent({ days: 7 });
    const endTime = status === 'completed' ? new Date(startTime.getTime() + faker.number.int({ min: 300, max: 3600 }) * 1000) : null;
    
    return {
        id: generateUUID(),
        run_id: faker.string.uuid(),
        experiment_id: faker.string.uuid(),
        run_name: faker.lorem.words(3),
        model_type: modelType,
        framework: framework,
        status: status,
        start_time: startTime.toISOString(),
        end_time: endTime ? endTime.toISOString() : null,
        duration: endTime ? Math.floor((endTime - startTime) / 1000) : null,
        parameters: {
            learning_rate: faker.number.float({ min: 0.001, max: 0.1, fractionDigits: 4 }),
            batch_size: faker.helpers.arrayElement([16, 32, 64, 128, 256]),
            epochs: faker.number.int({ min: 10, max: 100 }),
            hidden_layers: faker.number.int({ min: 1, max: 5 }),
            dropout_rate: faker.number.float({ min: 0.1, max: 0.5, fractionDigits: 2 }),
            regularization: faker.number.float({ min: 0.001, max: 0.1, fractionDigits: 4 })
        },
        metrics: metrics.reduce((acc, metric) => {
            acc[metric] = faker.number.float({ min: 0, max: 1, fractionDigits: 4 });
            return acc;
        }, {}),
        training_data: {
            samples: faker.number.int({ min: 1000, max: 100000 }),
            features: faker.number.int({ min: 10, max: 1000 }),
            validation_split: faker.number.float({ min: 0.1, max: 0.3, fractionDigits: 2 }),
            data_source: faker.helpers.arrayElement(['CSV', 'Database', 'API', 'File Upload'])
        },
        artifacts: {
            model_path: `/models/${faker.string.uuid()}.pkl`,
            logs_path: `/logs/${faker.string.uuid()}.log`,
            metrics_path: `/metrics/${faker.string.uuid()}.json`,
            config_path: `/configs/${faker.string.uuid()}.yaml`
        },
        tags: {
            project: faker.lorem.word(),
            team: faker.helpers.arrayElement(['ML Team', 'Data Science', 'AI Research', 'Engineering']),
            environment: faker.helpers.arrayElement(['dev', 'staging', 'prod']),
            priority: faker.helpers.arrayElement(['low', 'medium', 'high', 'critical'])
        },
        created_at: faker.date.recent({ days: 7 }).toISOString(),
        updated_at: faker.date.recent({ days: 1 }).toISOString()
    };
}

module.exports = {
    generateTrainingJob
};
