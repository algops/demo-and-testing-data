const { faker } = require('@faker-js/faker');
const { generateUUID } = require('../../../shared/data-generators');

function generateInferenceResult(inferenceData = {}) {
    const predictionTypes = ['classification', 'regression', 'clustering', 'anomaly_detection', 'recommendation'];
    const predictionType = faker.helpers.arrayElement(predictionTypes);
    
    let prediction = null;
    let confidence = null;
    let probabilities = null;
    
    if (predictionType === 'classification') {
        const classes = ['Class A', 'Class B', 'Class C', 'Class D'];
        prediction = faker.helpers.arrayElement(classes);
        confidence = faker.number.float({ min: 0.5, max: 1.0, fractionDigits: 3 });
        probabilities = classes.reduce((acc, className) => {
            acc[className] = faker.number.float({ min: 0, max: 1, fractionDigits: 3 });
            return acc;
        }, {});
    } else if (predictionType === 'regression') {
        prediction = faker.number.float({ min: 0, max: 100, fractionDigits: 2 });
        confidence = faker.number.float({ min: 0.7, max: 1.0, fractionDigits: 3 });
    } else if (predictionType === 'clustering') {
        prediction = faker.number.int({ min: 0, max: 5 });
        confidence = faker.number.float({ min: 0.6, max: 1.0, fractionDigits: 3 });
    } else if (predictionType === 'anomaly_detection') {
        prediction = faker.datatype.boolean();
        confidence = faker.number.float({ min: 0.5, max: 1.0, fractionDigits: 3 });
    } else if (predictionType === 'recommendation') {
        const recommendations = Array.from({ length: faker.number.int({ min: 3, max: 10 }) }, () => ({
            item_id: faker.string.uuid(),
            score: faker.number.float({ min: 0, max: 1, fractionDigits: 3 }),
            reason: faker.lorem.sentence()
        }));
        prediction = recommendations;
        confidence = faker.number.float({ min: 0.6, max: 1.0, fractionDigits: 3 });
    }
    
    return {
        id: generateUUID(),
        prediction_id: faker.string.uuid(),
        model_id: faker.string.uuid(),
        model_version: faker.system.semver(),
        prediction_type: predictionType,
        prediction: prediction,
        confidence: confidence,
        probabilities: probabilities,
        input_features: Object.keys(inferenceData).length > 0 ? inferenceData : {
            feature_1: faker.number.float({ min: 0, max: 1, fractionDigits: 3 }),
            feature_2: faker.number.float({ min: 0, max: 1, fractionDigits: 3 }),
            feature_3: faker.number.float({ min: 0, max: 1, fractionDigits: 3 })
        },
        processing_time: faker.number.float({ min: 0.001, max: 2.0, fractionDigits: 4 }),
        timestamp: new Date().toISOString(),
        metadata: {
            model_framework: faker.helpers.arrayElement(['TensorFlow', 'PyTorch', 'Scikit-learn', 'XGBoost']),
            model_size: faker.number.int({ min: 1, max: 1000 }) + 'MB',
            gpu_used: faker.datatype.boolean(),
            memory_usage: faker.number.int({ min: 100, max: 8000 }) + 'MB'
        }
    };
}

module.exports = {
    generateInferenceResult
};
