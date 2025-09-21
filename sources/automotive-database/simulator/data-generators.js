const { faker } = require('@faker-js/faker');
const { generateUUID } = require('../../../shared/data-generators');

function generateVehicle(filters = {}) {
    const makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes-Benz', 'Audi', 'Nissan', 'Hyundai', 'Kia', 'Volkswagen', 'Mazda', 'Subaru', 'Lexus', 'Acura'];
    const models = ['Camry', 'Accord', 'F-150', 'Silverado', '3 Series', 'C-Class', 'A4', 'Altima', 'Elantra', 'Forte', 'Jetta', 'CX-5', 'Outback', 'ES', 'TLX'];
    const bodyTypes = ['Sedan', 'SUV', 'Truck', 'Hatchback', 'Coupe', 'Convertible', 'Wagon', 'Crossover'];
    const fuelTypes = ['Gasoline', 'Hybrid', 'Electric', 'Diesel', 'Plug-in Hybrid'];
    const transmissions = ['Automatic', 'Manual', 'CVT', 'Semi-Automatic'];
    
    const make = faker.helpers.arrayElement(makes);
    const model = faker.helpers.arrayElement(models);
    const year = faker.number.int({ min: 2015, max: 2024 });
    const mileage = faker.number.int({ min: 0, max: 150000 });
    const price = faker.number.int({ min: 15000, max: 80000 });
    const bodyType = faker.helpers.arrayElement(bodyTypes);
    const fuelType = faker.helpers.arrayElement(fuelTypes);
    const transmission = faker.helpers.arrayElement(transmissions);
    
    return {
        id: generateUUID(),
        vehicle_id: faker.string.uuid(),
        make: make,
        model: model,
        year: year,
        trim: faker.helpers.arrayElement(['Base', 'LE', 'XLE', 'Limited', 'Sport', 'Touring', 'Premium']),
        body_type: bodyType,
        fuel_type: fuelType,
        transmission: transmission,
        engine: {
            displacement: faker.number.float({ min: 1.0, max: 6.0, fractionDigits: 1 }) + 'L',
            cylinders: faker.number.int({ min: 3, max: 8 }),
            horsepower: faker.number.int({ min: 100, max: 500 }),
            torque: faker.number.int({ min: 100, max: 600 })
        },
        mileage: mileage,
        price: price,
        currency: 'USD',
        condition: faker.helpers.arrayElement(['Excellent', 'Good', 'Fair', 'Poor']),
        color: faker.color.human(),
        interior_color: faker.color.human(),
        features: Array.from({ length: faker.number.int({ min: 5, max: 15 }) }, () => faker.vehicle.accessories()),
        safety_rating: faker.number.int({ min: 1, max: 5 }),
        mpg_city: faker.number.int({ min: 15, max: 40 }),
        mpg_highway: faker.number.int({ min: 20, max: 50 }),
        vin: faker.vehicle.vin(),
        stock_number: faker.string.alphanumeric(8).toUpperCase(),
        dealer: {
            name: faker.company.name() + ' Auto',
            location: faker.location.city(),
            phone: faker.phone.number(),
            website: faker.internet.url()
        },
        history: {
            accidents: faker.number.int({ min: 0, max: 3 }),
            owners: faker.number.int({ min: 1, max: 4 }),
            service_records: faker.number.int({ min: 0, max: 20 }),
            title_status: faker.helpers.arrayElement(['Clean', 'Salvage', 'Rebuilt', 'Lemon'])
        },
        warranty: {
            remaining_months: faker.number.int({ min: 0, max: 60 }),
            mileage_remaining: faker.number.int({ min: 0, max: 100000 }),
            type: faker.helpers.arrayElement(['Factory', 'Extended', 'CPO', 'None'])
        },
        images: Array.from({ length: faker.number.int({ min: 3, max: 8 }) }, () => faker.image.url()),
        description: faker.lorem.paragraphs(2),
        tags: Array.from({ length: faker.number.int({ min: 3, max: 8 }) }, () => faker.vehicle.type()),
        created_at: faker.date.recent({ days: 30 }).toISOString(),
        updated_at: faker.date.recent({ days: 7 }).toISOString()
    };
}

module.exports = {
    generateVehicle
};
