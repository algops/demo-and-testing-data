const { faker } = require('@faker-js/faker');
const { generateUUID } = require('../../../shared/data-generators');

function generateProduct(filters = {}) {
    const productName = faker.commerce.productName();
    const category = faker.commerce.department();
    const price = parseFloat(faker.commerce.price({ min: 10, max: 1000 }));
    const originalPrice = price + faker.number.int({ min: 0, max: 200 });
    const discount = Math.round(((originalPrice - price) / originalPrice) * 100);
    const rating = faker.number.float({ min: 1, max: 5, fractionDigits: 1 });
    const reviewCount = faker.number.int({ min: 0, max: 1000 });
    const stock = faker.number.int({ min: 0, max: 100 });
    const brand = faker.company.name();
    
    return {
        id: generateUUID(),
        product_id: faker.string.uuid(),
        name: productName,
        category: category,
        subcategory: faker.commerce.productAdjective(),
        brand: brand,
        price: price,
        original_price: originalPrice,
        discount_percentage: discount,
        currency: 'USD',
        rating: rating,
        review_count: reviewCount,
        stock_quantity: stock,
        availability: stock > 0 ? 'In Stock' : 'Out of Stock',
        description: faker.commerce.productDescription(),
        features: Array.from({ length: faker.number.int({ min: 3, max: 8 }) }, () => faker.lorem.sentence()),
        specifications: {
            weight: faker.number.float({ min: 0.1, max: 50, fractionDigits: 2 }) + ' lbs',
            dimensions: `${faker.number.int({ min: 5, max: 50 })}x${faker.number.int({ min: 5, max: 50 })}x${faker.number.int({ min: 5, max: 50 })} inches`,
            color: faker.color.human(),
            material: faker.helpers.arrayElement(['Plastic', 'Metal', 'Wood', 'Fabric', 'Glass'])
        },
        images: Array.from({ length: faker.number.int({ min: 1, max: 5 }) }, () => faker.image.url()),
        seller: {
            name: faker.company.name(),
            rating: faker.number.float({ min: 1, max: 5, fractionDigits: 1 }),
            location: faker.location.city()
        },
        shipping: {
            free_shipping: faker.datatype.boolean(),
            estimated_delivery: faker.helpers.arrayElement(['1-2 days', '3-5 days', '1-2 weeks']),
            return_policy: faker.helpers.arrayElement(['30 days', '60 days', '90 days'])
        },
        tags: Array.from({ length: faker.number.int({ min: 2, max: 6 }) }, () => faker.lorem.word()),
        created_at: faker.date.recent({ days: 180 }).toISOString(),
        updated_at: faker.date.recent({ days: 30 }).toISOString()
    };
}

module.exports = {
    generateProduct
};
