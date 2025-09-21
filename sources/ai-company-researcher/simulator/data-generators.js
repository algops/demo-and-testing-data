/**
 * AI Company Researcher Simulator - Data Generators
 * Generates realistic company data for AI research
 */

const { generateObject } = require('../../shared/data-generators');
const { calculateFieldCompleteness, calculateDataQualityMetrics } = require('../../shared/logging');

/**
 * AI Company Researcher data generators
 */
class AICompanyResearcherGenerator {
  constructor() {
    this.objectType = 'company';
    this.requiredFields = [
      'name', 'website', 'industry', 'employee_count', 'founded_year', 
      'revenue', 'funding', 'currency', 'city', 'state', 'country', 
      'technologies', 'status'
    ];
  }

  /**
   * Generate company records based on query parameters
   */
  generateCompanyRecords(query, maxObjects = 100) {
    const startTime = Date.now();
    
    // Parse query parameters
    const filters = this.parseQuery(query);
    const recordCount = this.calculateRecordCount(filters, maxObjects);
    
    // Generate base records
    let records = generateObject(this.objectType, recordCount);
    
    // Apply AI research specific filters
    records = this.applyAIResearchFilters(records, filters);
    
    // Add AI research specific enhancements
    records = this.enhanceAIResearchData(records);
    
    const generationTime = Date.now() - startTime;
    
    // Calculate quality metrics
    const fieldCompleteness = calculateFieldCompleteness(records, this.requiredFields);
    const dataQuality = calculateDataQualityMetrics(records, this.objectType);
    
    return {
      records,
      metadata: {
        total_records: records.length,
        generation_time_ms: generationTime,
        field_completeness: fieldCompleteness,
        data_quality: dataQuality,
        query_processed: query,
        filters_applied: filters
      }
    };
  }

  /**
   * Parse query string for company research
   */
  parseQuery(query) {
    const filters = {};
    
    if (typeof query === 'string') {
      // Extract industry focus
      const industryKeywords = ['technology', 'healthcare', 'finance', 'manufacturing', 'retail', 'education'];
      industryKeywords.forEach(keyword => {
        if (query.toLowerCase().includes(keyword)) {
          filters.industry_focus = keyword;
        }
      });
      
      // Extract funding stage
      const fundingStages = ['seed', 'series a', 'series b', 'series c', 'series d', 'ipo', 'public'];
      fundingStages.forEach(stage => {
        if (query.toLowerCase().includes(stage)) {
          filters.funding_stage = stage;
        }
      });
      
      // Extract employee count range
      const employeeMatch = query.match(/(\d+)-(\d+)\s*employees?/i);
      if (employeeMatch) {
        filters.employee_range = {
          min: parseInt(employeeMatch[1]),
          max: parseInt(employeeMatch[2])
        };
      }
      
      // Extract location
      const locationMatch = query.match(/(in|at|from)\s+([A-Za-z\s,]+)/i);
      if (locationMatch) {
        filters.location = locationMatch[2].trim();
      }
    }
    
    return filters;
  }

  /**
   * Calculate number of records to generate based on query complexity
   */
  calculateRecordCount(filters, maxObjects) {
    let baseCount = Math.floor(Math.random() * 80) + 20; // 20-100 base records
    
    // Adjust based on query complexity
    if (filters.industry_focus) {
      baseCount = Math.floor(baseCount * 0.6); // Fewer matches with specific industry
    }
    
    if (filters.funding_stage) {
      baseCount = Math.floor(baseCount * 0.5); // Fewer matches with specific funding stage
    }
    
    if (filters.employee_range) {
      baseCount = Math.floor(baseCount * 0.7); // Fewer matches with specific employee range
    }
    
    if (filters.location) {
      baseCount = Math.floor(baseCount * 0.8); // Fewer matches with specific location
    }
    
    return Math.min(baseCount, maxObjects);
  }

  /**
   * Apply AI research specific filters
   */
  applyAIResearchFilters(records, filters) {
    return records.filter(record => {
      // Industry focus filter
      if (filters.industry_focus && !this.matchesIndustry(record, filters.industry_focus)) {
        return false;
      }
      
      // Funding stage filter
      if (filters.funding_stage && !this.matchesFundingStage(record, filters.funding_stage)) {
        return false;
      }
      
      // Employee range filter
      if (filters.employee_range && !this.matchesEmployeeRange(record, filters.employee_range)) {
        return false;
      }
      
      // Location filter
      if (filters.location && !this.matchesLocation(record, filters.location)) {
        return false;
      }
      
      return true;
    });
  }

  /**
   * Check if record matches industry focus
   */
  matchesIndustry(record, industryFocus) {
    return record.industry.toLowerCase().includes(industryFocus.toLowerCase());
  }

  /**
   * Check if record matches funding stage
   */
  matchesFundingStage(record, fundingStage) {
    const employeeCount = record.employee_count;
    const funding = record.funding;
    
    switch (fundingStage.toLowerCase()) {
      case 'seed':
        return employeeCount <= 10 && funding <= 2000000;
      case 'series a':
        return employeeCount > 10 && employeeCount <= 50 && funding > 2000000 && funding <= 10000000;
      case 'series b':
        return employeeCount > 50 && employeeCount <= 200 && funding > 10000000 && funding <= 50000000;
      case 'series c':
        return employeeCount > 200 && employeeCount <= 500 && funding > 50000000 && funding <= 100000000;
      case 'series d':
        return employeeCount > 500 && funding > 100000000;
      case 'ipo':
      case 'public':
        return record.status === 'public';
      default:
        return true;
    }
  }

  /**
   * Check if record matches employee range
   */
  matchesEmployeeRange(record, employeeRange) {
    const count = record.employee_count;
    return count >= employeeRange.min && count <= employeeRange.max;
  }

  /**
   * Check if record matches location
   */
  matchesLocation(record, location) {
    return record.city.toLowerCase().includes(location.toLowerCase()) ||
           record.state.toLowerCase().includes(location.toLowerCase());
  }

  /**
   * Enhance records with AI research specific data
   */
  enhanceAIResearchData(records) {
    return records.map(record => {
      // Add AI research specific fields
      record.ai_readiness_score = this.calculateAIReadinessScore(record);
      record.tech_stack_modernity = this.calculateTechStackModernity(record);
      record.growth_potential = this.calculateGrowthPotential(record);
      record.market_position = this.calculateMarketPosition(record);
      record.funding_rounds = this.generateFundingRounds(record);
      record.key_metrics = this.generateKeyMetrics(record);
      record.competitive_analysis = this.generateCompetitiveAnalysis(record);
      record.risk_assessment = this.generateRiskAssessment(record);
      
      // Add research metadata
      record.research_confidence = Math.random() * 0.3 + 0.7; // 0.7-1.0
      record.data_freshness = this.generateDataFreshness();
      record.source_reliability = Math.random() * 0.2 + 0.8; // 0.8-1.0
      
      return record;
    });
  }

  /**
   * Calculate AI readiness score based on company characteristics
   */
  calculateAIReadinessScore(record) {
    let score = 0.5; // Base score
    
    // Technology stack bonus
    const modernTechs = ['AI', 'ML', 'Python', 'TensorFlow', 'PyTorch', 'AWS', 'GCP', 'Azure'];
    const hasModernTech = record.technologies.some(tech => 
      modernTechs.some(modern => tech.toLowerCase().includes(modern.toLowerCase()))
    );
    if (hasModernTech) score += 0.2;
    
    // Company size bonus (larger companies more likely to use AI)
    if (record.employee_count > 100) score += 0.1;
    if (record.employee_count > 500) score += 0.1;
    
    // Industry bonus
    const aiFriendlyIndustries = ['technology', 'healthcare', 'finance', 'manufacturing'];
    if (aiFriendlyIndustries.includes(record.industry.toLowerCase())) {
      score += 0.1;
    }
    
    // Funding bonus (well-funded companies more likely to invest in AI)
    if (record.funding > 10000000) score += 0.1;
    
    return Math.min(score, 1.0);
  }

  /**
   * Calculate tech stack modernity score
   */
  calculateTechStackModernity(record) {
    const modernTechnologies = [
      'React', 'Vue', 'Angular', 'Node.js', 'Python', 'Go', 'Rust',
      'Docker', 'Kubernetes', 'AWS', 'GCP', 'Azure', 'MongoDB', 'PostgreSQL'
    ];
    
    const modernCount = record.technologies.filter(tech =>
      modernTechnologies.some(modern => tech.toLowerCase().includes(modern.toLowerCase()))
    ).length;
    
    return Math.min(modernCount / record.technologies.length, 1.0);
  }

  /**
   * Calculate growth potential score
   */
  calculateGrowthPotential(record) {
    let score = 0.5;
    
    // Revenue per employee ratio
    const revenuePerEmployee = record.revenue / record.employee_count;
    if (revenuePerEmployee > 200000) score += 0.2;
    if (revenuePerEmployee > 500000) score += 0.1;
    
    // Company age (younger companies have more growth potential)
    const age = 2024 - record.founded_year;
    if (age < 5) score += 0.2;
    else if (age < 10) score += 0.1;
    
    // Industry growth potential
    const highGrowthIndustries = ['technology', 'healthcare', 'fintech', 'edtech'];
    if (highGrowthIndustries.some(industry => 
      record.industry.toLowerCase().includes(industry))) {
      score += 0.1;
    }
    
    return Math.min(score, 1.0);
  }

  /**
   * Calculate market position
   */
  calculateMarketPosition(record) {
    const positions = ['Leader', 'Challenger', 'Follower', 'Niche'];
    const weights = [0.1, 0.3, 0.4, 0.2]; // Most companies are followers or challengers
    
    let cumulative = 0;
    const random = Math.random();
    
    for (let i = 0; i < positions.length; i++) {
      cumulative += weights[i];
      if (random <= cumulative) {
        return positions[i];
      }
    }
    
    return 'Follower';
  }

  /**
   * Generate funding rounds history
   */
  generateFundingRounds(record) {
    const rounds = [];
    const totalFunding = record.funding;
    const currentYear = 2024;
    const foundedYear = record.founded_year;
    
    // Seed round
    if (totalFunding > 0) {
      rounds.push({
        round: 'Seed',
        amount: Math.min(totalFunding * 0.1, 2000000),
        year: foundedYear + Math.floor(Math.random() * 2),
        investors: this.generateInvestors(3)
      });
    }
    
    // Series A
    if (totalFunding > 2000000) {
      rounds.push({
        round: 'Series A',
        amount: Math.min(totalFunding * 0.3, 10000000),
        year: foundedYear + Math.floor(Math.random() * 3) + 1,
        investors: this.generateInvestors(5)
      });
    }
    
    // Series B
    if (totalFunding > 10000000) {
      rounds.push({
        round: 'Series B',
        amount: Math.min(totalFunding * 0.4, 50000000),
        year: foundedYear + Math.floor(Math.random() * 4) + 2,
        investors: this.generateInvestors(8)
      });
    }
    
    return rounds;
  }

  /**
   * Generate investor names
   */
  generateInvestors(count) {
    const investors = [
      'Sequoia Capital', 'Andreessen Horowitz', 'Kleiner Perkins', 'Accel Partners',
      'Bessemer Venture Partners', 'General Catalyst', 'Index Ventures', 'GV',
      'Lightspeed Venture Partners', 'NEA', 'Benchmark', 'First Round Capital'
    ];
    
    return investors
      .sort(() => Math.random() - 0.5)
      .slice(0, Math.min(count, investors.length));
  }

  /**
   * Generate key business metrics
   */
  generateKeyMetrics(record) {
    return {
      annual_revenue: record.revenue,
      revenue_growth_rate: Math.random() * 100, // 0-100%
      employee_count: record.employee_count,
      employee_growth_rate: Math.random() * 50, // 0-50%
      customer_count: Math.floor(record.employee_count * (Math.random() * 10 + 5)), // 5-15x employees
      market_share: Math.random() * 10, // 0-10%
      customer_acquisition_cost: Math.floor(Math.random() * 1000) + 100, // $100-$1100
      lifetime_value: Math.floor(Math.random() * 10000) + 1000 // $1000-$11000
    };
  }

  /**
   * Generate competitive analysis
   */
  generateCompetitiveAnalysis(record) {
    const competitors = this.generateCompetitors(record.industry);
    return {
      direct_competitors: competitors.slice(0, 3),
      competitive_advantages: this.generateCompetitiveAdvantages(),
      market_threats: this.generateMarketThreats(),
      differentiation_score: Math.random() * 0.5 + 0.5 // 0.5-1.0
    };
  }

  /**
   * Generate competitor companies
   */
  generateCompetitors(industry) {
    const industryCompetitors = {
      'technology': ['TechCorp', 'DataFlow', 'CloudSystems', 'AILabs'],
      'healthcare': ['HealthTech', 'MedFlow', 'BioSystems', 'CareLabs'],
      'finance': ['FinTech', 'PayFlow', 'BankSystems', 'MoneyLabs'],
      'manufacturing': ['ManuTech', 'ProdFlow', 'FactorySystems', 'IndustryLabs']
    };
    
    const competitors = industryCompetitors[industry.toLowerCase()] || 
                      ['CompetitorA', 'CompetitorB', 'CompetitorC'];
    
    return competitors.slice(0, 3);
  }

  /**
   * Generate competitive advantages
   */
  generateCompetitiveAdvantages() {
    const advantages = [
      'Superior technology stack',
      'Strong market position',
      'Experienced leadership team',
      'Unique product offering',
      'Strong customer relationships',
      'Efficient operations',
      'Innovative approach',
      'Strong financial position'
    ];
    
    return advantages
      .sort(() => Math.random() - 0.5)
      .slice(0, Math.floor(Math.random() * 3) + 2); // 2-4 advantages
  }

  /**
   * Generate market threats
   */
  generateMarketThreats() {
    const threats = [
      'Increased competition',
      'Market saturation',
      'Economic downturn',
      'Regulatory changes',
      'Technology disruption',
      'Supply chain issues',
      'Talent shortage',
      'Funding constraints'
    ];
    
    return threats
      .sort(() => Math.random() - 0.5)
      .slice(0, Math.floor(Math.random() * 3) + 1); // 1-3 threats
  }

  /**
   * Generate risk assessment
   */
  generateRiskAssessment(record) {
    return {
      overall_risk_score: Math.random() * 0.4 + 0.3, // 0.3-0.7
      financial_risk: Math.random() * 0.5 + 0.2, // 0.2-0.7
      market_risk: Math.random() * 0.6 + 0.2, // 0.2-0.8
      operational_risk: Math.random() * 0.4 + 0.3, // 0.3-0.7
      technology_risk: Math.random() * 0.5 + 0.2, // 0.2-0.7
      risk_factors: this.generateRiskFactors(),
      mitigation_strategies: this.generateMitigationStrategies()
    };
  }

  /**
   * Generate risk factors
   */
  generateRiskFactors() {
    const factors = [
      'High customer concentration',
      'Dependency on key personnel',
      'Regulatory compliance burden',
      'Technology obsolescence',
      'Market volatility',
      'Competitive pressure',
      'Funding runway concerns',
      'Operational scalability'
    ];
    
    return factors
      .sort(() => Math.random() - 0.5)
      .slice(0, Math.floor(Math.random() * 4) + 2); // 2-5 factors
  }

  /**
   * Generate mitigation strategies
   */
  generateMitigationStrategies() {
    const strategies = [
      'Diversify customer base',
      'Develop succession planning',
      'Invest in compliance systems',
      'Continuous technology updates',
      'Hedge against market volatility',
      'Strengthen competitive moats',
      'Secure additional funding',
      'Improve operational efficiency'
    ];
    
    return strategies
      .sort(() => Math.random() - 0.5)
      .slice(0, Math.floor(Math.random() * 4) + 2); // 2-5 strategies
  }

  /**
   * Generate data freshness timestamp
   */
  generateDataFreshness() {
    const now = new Date();
    const daysAgo = Math.floor(Math.random() * 7) + 1; // 1-7 days ago
    const freshnessDate = new Date(now.getTime() - (daysAgo * 24 * 60 * 60 * 1000));
    return freshnessDate.toISOString();
  }

  /**
   * Generate API response based on query
   */
  generateApiResponse(query, maxObjects = 100) {
    const { records, metadata } = this.generateCompanyRecords(query, maxObjects);
    
    return {
      status: 'completed',
      data: records,
      total_records: records.length,
      generated_at: new Date().toISOString(),
      metadata: metadata
    };
  }
}

module.exports = AICompanyResearcherGenerator;
