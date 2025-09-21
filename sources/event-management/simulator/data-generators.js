const { faker } = require('@faker-js/faker');
const { generateUUID } = require('../../../shared/data-generators');

function generateEvent(filters = {}) {
    const eventName = faker.lorem.words(3);
    const eventType = faker.helpers.arrayElement(['Conference', 'Workshop', 'Webinar', 'Meetup', 'Seminar', 'Training', 'Networking', 'Exhibition']);
    const category = faker.helpers.arrayElement(['Technology', 'Business', 'Education', 'Health', 'Entertainment', 'Sports', 'Arts', 'Science']);
    const startDate = faker.date.future({ days: 90 });
    const endDate = new Date(startDate.getTime() + faker.number.int({ min: 1, max: 3 }) * 24 * 60 * 60 * 1000);
    const location = faker.location.city();
    const state = faker.location.state({ abbreviated: true });
    const capacity = faker.number.int({ min: 10, max: 1000 });
    const price = faker.number.float({ min: 0, max: 500, fractionDigits: 2 });
    const organizer = faker.company.name();
    
    return {
        id: generateUUID(),
        event_id: faker.string.uuid(),
        name: eventName,
        type: eventType,
        category: category,
        description: faker.lorem.paragraphs(2),
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
        timezone: faker.location.timeZone(),
        location: {
            venue: faker.company.name() + ' Center',
            address: faker.location.streetAddress(),
            city: location,
            state: state,
            country: 'USA',
            postal_code: faker.location.zipCode(),
            coordinates: {
                latitude: faker.location.latitude(),
                longitude: faker.location.longitude()
            }
        },
        capacity: capacity,
        registered_count: faker.number.int({ min: 0, max: capacity }),
        price: price,
        currency: 'USD',
        organizer: {
            name: organizer,
            email: faker.internet.email(),
            phone: faker.phone.number(),
            website: faker.internet.url()
        },
        speakers: Array.from({ length: faker.number.int({ min: 1, max: 5 }) }, () => ({
            name: faker.person.fullName(),
            title: faker.person.jobTitle(),
            company: faker.company.name(),
            bio: faker.lorem.sentence()
        })),
        agenda: Array.from({ length: faker.number.int({ min: 3, max: 8 }) }, (_, index) => ({
            time: new Date(startDate.getTime() + index * 60 * 60 * 1000).toISOString(),
            title: faker.lorem.words(4),
            speaker: faker.person.fullName(),
            duration: faker.number.int({ min: 15, max: 90 })
        })),
        requirements: Array.from({ length: faker.number.int({ min: 0, max: 3 }) }, () => faker.lorem.sentence()),
        tags: Array.from({ length: faker.number.int({ min: 2, max: 5 }) }, () => faker.lorem.word()),
        status: faker.helpers.arrayElement(['upcoming', 'ongoing', 'completed', 'cancelled']),
        registration_deadline: faker.date.between({ from: new Date(), to: startDate }).toISOString(),
        created_at: faker.date.past({ days: 30 }).toISOString(),
        updated_at: faker.date.recent({ days: 7 }).toISOString()
    };
}

module.exports = {
    generateEvent
};
