const { faker } = require('@faker-js/faker');
const { generateUUID } = require('../../../shared/data-generators');

function generateJobPost(filters = {}) {
    const companyName = faker.company.name();
    const jobTitle = faker.person.jobTitle();
    const location = faker.location.city();
    const state = faker.location.state({ abbreviated: true });
    const salaryMin = faker.number.int({ min: 30000, max: 100000 });
    const salaryMax = salaryMin + faker.number.int({ min: 10000, max: 50000 });
    const jobType = faker.helpers.arrayElement(['Full-time', 'Part-time', 'Contract', 'Internship']);
    const experienceLevel = faker.helpers.arrayElement(['Entry', 'Mid', 'Senior', 'Executive']);
    const remoteWork = faker.helpers.arrayElement(['Remote', 'Hybrid', 'On-site']);
    
    return {
        id: generateUUID(),
        job_id: faker.string.uuid(),
        title: jobTitle,
        company: companyName,
        location: `${location}, ${state}`,
        salary_min: salaryMin,
        salary_max: salaryMax,
        currency: 'USD',
        job_type: jobType,
        experience_level: experienceLevel,
        remote_work: remoteWork,
        description: faker.lorem.paragraphs(3),
        requirements: Array.from({ length: faker.number.int({ min: 3, max: 8 }) }, () => faker.lorem.sentence()),
        benefits: Array.from({ length: faker.number.int({ min: 2, max: 6 }) }, () => faker.lorem.sentence()),
        posted_date: faker.date.recent({ days: 30 }).toISOString(),
        application_deadline: faker.date.future({ days: 30 }).toISOString(),
        status: faker.helpers.arrayElement(['active', 'closed', 'paused']),
        source: faker.helpers.arrayElement(['LinkedIn', 'Indeed', 'Glassdoor', 'Company Website']),
        url: faker.internet.url()
    };
}

module.exports = {
    generateJobPost
};
