const { faker } = require('@faker-js/faker');
const { generateUUID } = require('../../../shared/data-generators');

function generateESGData(query = {}) {
    const companyName = faker.company.name();
    const industry = faker.commerce.department();
    const esgScore = faker.number.int({ min: 0, max: 100 });
    const environmentalScore = faker.number.int({ min: 0, max: 100 });
    const socialScore = faker.number.int({ min: 0, max: 100 });
    const governanceScore = faker.number.int({ min: 0, max: 100 });
    
    const riskLevel = esgScore >= 80 ? 'Low' : esgScore >= 60 ? 'Medium' : 'High';
    const rating = esgScore >= 90 ? 'AAA' : esgScore >= 80 ? 'AA' : esgScore >= 70 ? 'A' : esgScore >= 60 ? 'BBB' : 'BB';
    
    return {
        id: generateUUID(),
        company_name: companyName,
        industry: industry,
        esg_score: esgScore,
        environmental_score: environmentalScore,
        social_score: socialScore,
        governance_score: governanceScore,
        risk_level: riskLevel,
        rating: rating,
        carbon_footprint: faker.number.int({ min: 100, max: 10000 }),
        renewable_energy_percentage: faker.number.int({ min: 0, max: 100 }),
        diversity_score: faker.number.int({ min: 0, max: 100 }),
        board_independence: faker.number.int({ min: 0, max: 100 }),
        transparency_score: faker.number.int({ min: 0, max: 100 }),
        last_updated: faker.date.recent({ days: 30 }).toISOString(),
        data_source: faker.helpers.arrayElement(['Bloomberg', 'Refinitiv', 'MSCI', 'Sustainalytics']),
        compliance_status: faker.helpers.arrayElement(['Compliant', 'Partially Compliant', 'Non-Compliant'])
    };
}

module.exports = {
    generateESGData
};
