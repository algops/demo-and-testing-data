const fs = require('fs');
const dashboardFull = JSON.parse(fs.readFileSync('dashboard-full.json', 'utf8'));

// Fix history items to match expected format
const fixedHistory = dashboardFull.history.items.map((item, index) => {
  const date = new Date(item.timestamp || item.date);
  const formattedDate = date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
  
  return {
    id: item.id || `history-${index + 1}`,
    action: item.action || item.type || item.name || 'Unknown Action',
    user: item.user || 'System',
    date: formattedDate,
    status: item.status === 'success' ? 'Success' : item.status === 'failed' ? 'Error' : item.status || 'Success'
  };
});

dashboardFull.history.items = fixedHistory;
fs.writeFileSync('dashboard-full.json', JSON.stringify(dashboardFull, null, 2));
console.log('Fixed history items format');
