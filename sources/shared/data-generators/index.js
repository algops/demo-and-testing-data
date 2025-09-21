const { v4: uuidv4 } = require('uuid');

function generateUUID() {
    return uuidv4();
}

function generateRandomString(length = 8) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

function generateRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateRandomFloat(min, max, decimals = 2) {
    return parseFloat((Math.random() * (max - min) + min).toFixed(decimals));
}

function generateRandomBoolean() {
    return Math.random() < 0.5;
}

function generateRandomArrayElement(array) {
    return array[Math.floor(Math.random() * array.length)];
}

function generateRandomArray(array, count) {
    const shuffled = [...array].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}

function generateRandomDate(start, end) {
    return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
}

function generateRandomEmail(domain = 'example.com') {
    const username = generateRandomString(8);
    return `${username}@${domain}`;
}

function generateRandomPhone() {
    const areaCode = generateRandomNumber(200, 999);
    const exchange = generateRandomNumber(200, 999);
    const number = generateRandomNumber(1000, 9999);
    return `${areaCode}-${exchange}-${number}`;
}

function generateRandomUrl(domain = 'example.com') {
    const path = generateRandomString(6);
    return `https://${domain}/${path}`;
}

module.exports = {
    generateUUID,
    generateRandomString,
    generateRandomNumber,
    generateRandomFloat,
    generateRandomBoolean,
    generateRandomArrayElement,
    generateRandomArray,
    generateRandomDate,
    generateRandomEmail,
    generateRandomPhone,
    generateRandomUrl
};
