const fs = require('fs');

// Read source data
const activities = JSON.parse(fs.readFileSync('activities/activities.json', 'utf8'));
const workflows = JSON.parse(fs.readFileSync('workflows/workflows.json', 'utf8'));
const sources = JSON.parse(fs.readFileSync('sources/sources.json', 'utf8'));

// Calculate totals
const totalActivities = activities.activities.length;
const totalRequests = activities.activities.reduce((sum, a) => sum + (a.total_requests || 0), 0);
const successfulRequests = activities.activities.reduce((sum, a) => sum + (a.successful_requests || 0), 0);
const failedRequests = activities.activities.reduce((sum, a) => sum + (a.failed_requests || 0), 0);

const totalWorkflows = workflows.workflows.length;
const totalExecutions = workflows.workflows.reduce((sum, w) => sum + (w.total_executions || 0), 0);
const successfulExecutions = workflows.workflows.reduce((sum, w) => sum + (w.successful_executions || 0), 0);
const failedExecutions = workflows.workflows.reduce((sum, w) => sum + (w.failed_executions || 0), 0);

const totalSources = sources.sources.length;
const totalRuns = sources.sources.reduce((sum, s) => sum + (s.total_runs || 0), 0);
const successfulRuns = sources.sources.reduce((sum, s) => sum + (s.successful_runs || 0), 0);
const failedRuns = sources.sources.reduce((sum, s) => sum + (s.failed_runs || 0), 0);

// Estimate objects: 20-30 per successful request, average 25
const estimatedObjects = Math.round(successfulRequests * 25);

// Generate monthly data for last 6 months with significant variation
const now = new Date();
const months = [];
for (let i = 5; i >= 0; i--) {
  const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
  months.push(date.toLocaleDateString('en-US', { month: 'short' }));
}

// Distribute totals across 6 months with significant variation (±40%)
// Data should represent executions/requests, not counts
const distributeValue = (total, months, baseVariation = 0.4) => {
  const base = Math.floor(total / months.length);
  const remainder = total % months.length;
  const values = Array(months.length).fill(base);
  // Add remainder to first few months
  for (let i = 0; i < remainder; i++) {
    values[i] += 1;
  }
  // Add significant variation with trend
  return values.map((v, index) => {
    // Create a trend: lower in middle months, higher at start and end
    const trendFactor = index < 2 ? 1.2 : index < 4 ? 0.75 : 1.15;
    // Add random variation
    const randomVariation = (Math.random() - 0.5) * baseVariation;
    const variation = Math.floor(v * (trendFactor - 1 + randomVariation));
    return Math.max(0, v + variation);
  });
};

// For workflows, make them much smaller (executions are fewer than requests/runs)
// Scale down workflows to be 1-5% of activities
const activitiesMonthly = distributeValue(totalRequests, months, 0.4);
const sourcesMonthly = distributeValue(totalRuns, months, 0.4);
// Workflows should be much smaller - scale to be realistic (executions are rarer)
const workflowScale = totalExecutions / totalRequests; // ~0.023 (2.3%)
const workflowsMonthly = distributeValue(totalExecutions, months, 0.5).map(v => Math.max(1, v));

// Categories in stacking order: Sources (bottom), Activities (middle), Workflows (top)
const categories = ["Sources", "Activities", "Workflows"];

// Generate dashboard.json
const dashboardData = {
  metrics: [
    {
      id: "requests",
      title: "Requests",
      description: "Total number of API requests",
      value: totalRequests.toLocaleString()
    },
    {
      id: "executions",
      title: "Executions",
      description: "Total number of workflow executions",
      value: totalExecutions.toLocaleString()
    },
    {
      id: "objects",
      title: "Objects",
      description: "Total number of objects created",
      value: estimatedObjects.toLocaleString()
    },
    {
      id: "sources",
      title: "Sources",
      description: "Total number of data sources",
      value: totalSources.toString()
    }
  ],
  usage: {
    title: "Platform Usage",
    categories: categories,
    data: months.map((month, index) => ({
      month,
      Sources: sourcesMonthly[index],
      Activities: activitiesMonthly[index],
      Workflows: workflowsMonthly[index]
    }))
  }
};

fs.writeFileSync('dashboard.json', JSON.stringify(dashboardData, null, 2));
console.log('Generated dashboard.json');

// Generate dashboard-full.json with all time periods and varied data
const generateDailyData = (monthlyTotal) => {
  const daily = Math.floor(monthlyTotal / 7);
  const remainder = monthlyTotal % 7;
  const days = Array(7).fill(daily);
  for (let i = 0; i < remainder; i++) {
    days[i] += 1;
  }
  // Add variation to daily data - weekends are lower
  return days.map((d, i) => {
    const isWeekend = i === 5 || i === 6;
    const variation = isWeekend ? -0.35 : (Math.random() - 0.5) * 0.25;
    return Math.max(0, Math.floor(d * (1 + variation)));
  });
};

const generateQuarterlyData = (monthlyData) => {
  const quarters = [];
  for (let i = 0; i < monthlyData.length; i += 3) {
    const quarterTotal = monthlyData.slice(i, i + 3).reduce((sum, v) => sum + v, 0);
    quarters.push(quarterTotal);
  }
  // Add variation to quarters
  return quarters.map((q, i) => {
    const trend = i === 0 ? 0.85 : i === 1 ? 1.0 : i === 2 ? 1.15 : 1.05;
    return Math.floor(q * trend);
  });
};

const generateYearlyData = (quarterlyData) => {
  const years = [];
  for (let i = 0; i < quarterlyData.length; i += 4) {
    const yearTotal = quarterlyData.slice(i, i + 4).reduce((sum, v) => sum + v, 0);
    years.push(yearTotal);
  }
  // Add growth trend to years
  return years.map((y, i) => {
    const growthFactor = 1 + (i * 0.18); // 18% growth per year
    return Math.floor(y * growthFactor);
  });
};

const currentMonthTotal = activitiesMonthly[activitiesMonthly.length - 1];
const weekData = {
  Sources: generateDailyData(sourcesMonthly[sourcesMonthly.length - 1]),
  Activities: generateDailyData(currentMonthTotal),
  Workflows: generateDailyData(workflowsMonthly[workflowsMonthly.length - 1]).map(v => Math.max(1, v))
};

const quarterData = {
  Sources: generateQuarterlyData(sourcesMonthly),
  Activities: generateQuarterlyData(activitiesMonthly),
  Workflows: generateQuarterlyData(workflowsMonthly).map(v => Math.max(1, v))
};

const yearData = {
  Sources: generateYearlyData(quarterData.Sources),
  Activities: generateYearlyData(quarterData.Activities),
  Workflows: generateYearlyData(quarterData.Workflows).map(v => Math.max(1, v))
};

// Generate costs data
const calculateCosts = (usageData, period) => {
  const activitiesCost = usageData.Activities * 0.10;
  const workflowsCost = usageData.Workflows * 5;
  const sourcesCost = usageData.Sources * 0.05;
  return [
    { name: "Activities", value: activitiesCost },
    { name: "Workflows", value: workflowsCost },
    { name: "Sources", value: sourcesCost }
  ];
};

// Generate random 8-digit integer ID
const generateRandomId = () => {
  return Math.floor(10000000 + Math.random() * 90000000); // 8-digit number (10000000-99999999)
};

// Generate history items from actual data with proper structure
const historyItems = [];
const allItems = [];

// Collect all activity requests
activities.activities.forEach(a => {
  // Generate multiple history items per activity based on total_requests
  const itemsCount = Math.min(5, Math.floor(a.total_requests / 100)); // Up to 5 items per activity
  for (let i = 0; i < itemsCount; i++) {
    const isSuccess = Math.random() > (a.failed_requests / a.total_requests);
    const timestamp = new Date(a.last_used_at);
    timestamp.setHours(timestamp.getHours() - Math.floor(Math.random() * 24 * 7)); // Random time in last week
    allItems.push({
      type: "Activity Request",
      name: a.name,
      timestamp: timestamp,
      status: isSuccess ? "success" : "failed",
      user: "System"
    });
  }
});

// Collect workflow executions
workflows.workflows.forEach(w => {
  const itemsCount = Math.min(3, Math.floor(w.total_executions / 10)); // Up to 3 items per workflow
  for (let i = 0; i < itemsCount; i++) {
    const isSuccess = Math.random() > (w.failed_executions / w.total_executions);
    const timestamp = new Date(w.last_used_at);
    timestamp.setHours(timestamp.getHours() - Math.floor(Math.random() * 24 * 7));
    allItems.push({
      type: "Workflow Execution",
      name: w.name,
      timestamp: timestamp,
      status: isSuccess ? "success" : "failed",
      user: "System"
    });
  }
});

// Collect source runs
sources.sources.forEach(s => {
  const itemsCount = Math.min(4, Math.floor(s.total_runs / 200)); // Up to 4 items per source
  for (let i = 0; i < itemsCount; i++) {
    const isSuccess = Math.random() > (s.failed_runs / s.total_runs);
    const timestamp = new Date(s.last_used_at);
    timestamp.setHours(timestamp.getHours() - Math.floor(Math.random() * 24 * 7));
    allItems.push({
      type: "Source Run",
      name: s.name,
      timestamp: timestamp,
      status: isSuccess ? "success" : "failed",
      user: "System"
    });
  }
});

// Sort by timestamp and take most recent 30
allItems.sort((a, b) => b.timestamp - a.timestamp);
allItems.slice(0, 30).forEach((item) => {
  const formattedDate = item.timestamp.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
  
  historyItems.push({
    id: generateRandomId().toString(),
    action: item.type,
    user: item.user || "System",
    date: formattedDate,
    status: item.status === "success" ? "Success" : "Error"
  });
});

const dashboardFullData = {
  timePeriods: ["Week", "Month", "Quarter", "Year"],
  charts: {
    usage: {
      categories: categories,
      data: {
        Week: Array.from({ length: 7 }, (_, i) => ({
          day: `Day ${i + 1}`,
          Sources: weekData.Sources[i] || 0,
          Activities: weekData.Activities[i] || 0,
          Workflows: weekData.Workflows[i] || 0
        })),
        Month: months.map((month, index) => ({
          month,
          Sources: sourcesMonthly[index],
          Activities: activitiesMonthly[index],
          Workflows: workflowsMonthly[index]
        })),
        Quarter: quarterData.Sources.map((_, i) => ({
          quarter: `Q${i + 1}`,
          Sources: quarterData.Sources[i] || 0,
          Activities: quarterData.Activities[i] || 0,
          Workflows: quarterData.Workflows[i] || 0
        })),
        Year: yearData.Sources.map((_, i) => ({
          year: `Year ${i + 1}`,
          Sources: yearData.Sources[i] || 0,
          Activities: yearData.Activities[i] || 0,
          Workflows: yearData.Workflows[i] || 0
        }))
      }
    },
    costs: {
      currency: "$",
      data: {
        Week: calculateCosts({
          Sources: weekData.Sources.reduce((a, b) => a + b, 0),
          Activities: weekData.Activities.reduce((a, b) => a + b, 0),
          Workflows: weekData.Workflows.reduce((a, b) => a + b, 0)
        }, "Week"),
        Month: calculateCosts({
          Sources: sourcesMonthly.reduce((a, b) => a + b, 0),
          Activities: activitiesMonthly.reduce((a, b) => a + b, 0),
          Workflows: workflowsMonthly.reduce((a, b) => a + b, 0)
        }, "Month"),
        Quarter: calculateCosts({
          Sources: quarterData.Sources.reduce((a, b) => a + b, 0),
          Activities: quarterData.Activities.reduce((a, b) => a + b, 0),
          Workflows: quarterData.Workflows.reduce((a, b) => a + b, 0)
        }, "Quarter"),
        Year: calculateCosts({
          Sources: yearData.Sources.reduce((a, b) => a + b, 0),
          Activities: yearData.Activities.reduce((a, b) => a + b, 0),
          Workflows: yearData.Workflows.reduce((a, b) => a + b, 0)
        }, "Year")
      }
    }
  },
  history: {
    items: historyItems
  }
};

fs.writeFileSync('dashboard-full.json', JSON.stringify(dashboardFullData, null, 2));
console.log('Generated dashboard-full.json with', historyItems.length, 'history items');
console.log('Sample IDs:', historyItems.slice(0, 3).map(i => i.id).join(', '));
