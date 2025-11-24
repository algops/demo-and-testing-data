const fs = require('fs');
const dashboardFull = JSON.parse(fs.readFileSync('dashboard-full.json', 'utf8'));

// Generate random 8-digit integer
const generateRandomId = () => {
  return Math.floor(10000000 + Math.random() * 90000000); // 8-digit number (10000000-99999999)
};

// Update all history items with random 8-digit IDs
dashboardFull.history.items = dashboardFull.history.items.map((item) => ({
  ...item,
  id: generateRandomId().toString()
}));

fs.writeFileSync('dashboard-full.json', JSON.stringify(dashboardFull, null, 2));
console.log('Updated history IDs to random 8-digit integers');
console.log('Sample IDs:', dashboardFull.history.items.slice(0, 3).map(i => i.id).join(', '));
