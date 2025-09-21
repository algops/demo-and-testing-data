/**
 * LinkedIn People Dataset Simulator - Data Generators
 * Generates realistic person profiles with professional information
 */

const { generateObject } = require('../../shared/data-generators');
const { calculateFieldCompleteness, calculateDataQualityMetrics } = require('../../shared/logging');

/**
 * LinkedIn-specific data generators
 */
class LinkedInDataGenerator {
  constructor() {
    this.objectType = 'person';
    this.requiredFields = [
      'name', 'email', 'role', 'department', 'salary', 'hourly_rate', 
      'skills', 'phone', 'linkedin', 'website', 'experience_years', 
      'education', 'specialization'
    ];
  }

  /**
   * Generate person records based on request parameters
   */
  generatePeopleRecords(requestParams, maxObjects = 500) {
    const startTime = Date.now();
    
    // Parse request parameters
    const filters = this.parseFilters(requestParams);
    const recordCount = this.calculateRecordCount(filters, maxObjects);
    
    // Generate base records
    let records = generateObject(this.objectType, recordCount);
    
    // Apply LinkedIn-specific filters
    records = this.applyLinkedInFilters(records, filters);
    
    // Add LinkedIn-specific enhancements
    records = this.enhanceLinkedInData(records);
    
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
        filters_applied: filters
      }
    };
  }

  /**
   * Parse request filters from run_setup
   */
  parseFilters(requestParams) {
    const filters = {};
    
    if (requestParams.filter && requestParams.filter.filters) {
      const filterData = typeof requestParams.filter.filters === 'string' 
        ? JSON.parse(requestParams.filter.filters) 
        : requestParams.filter.filters;
        
      if (filterData.location) filters.location = filterData.location;
      if (filterData.experience_years) filters.experience_years = filterData.experience_years;
      if (filterData.skills) filters.skills = Array.isArray(filterData.skills) ? filterData.skills : [filterData.skills];
      if (filterData.department) filters.department = filterData.department;
      if (filterData.role) filters.role = filterData.role;
    }
    
    return filters;
  }

  /**
   * Calculate number of records to generate based on filters
   */
  calculateRecordCount(filters, maxObjects) {
    let baseCount = Math.floor(Math.random() * 400) + 50; // 50-450 base records
    
    // Adjust based on filters
    if (filters.skills && filters.skills.length > 0) {
      baseCount = Math.floor(baseCount * 0.7); // Fewer matches with specific skills
    }
    
    if (filters.experience_years) {
      baseCount = Math.floor(baseCount * 0.8); // Fewer matches with experience filter
    }
    
    if (filters.department) {
      baseCount = Math.floor(baseCount * 0.6); // Fewer matches with department filter
    }
    
    return Math.min(baseCount, maxObjects);
  }

  /**
   * Apply LinkedIn-specific filters to generated records
   */
  applyLinkedInFilters(records, filters) {
    return records.filter(record => {
      // Location filter
      if (filters.location && !this.matchesLocation(record, filters.location)) {
        return false;
      }
      
      // Experience years filter
      if (filters.experience_years && !this.matchesExperience(record, filters.experience_years)) {
        return false;
      }
      
      // Skills filter
      if (filters.skills && !this.matchesSkills(record, filters.skills)) {
        return false;
      }
      
      // Department filter
      if (filters.department && !this.matchesDepartment(record, filters.department)) {
        return false;
      }
      
      // Role filter
      if (filters.role && !this.matchesRole(record, filters.role)) {
        return false;
      }
      
      return true;
    });
  }

  /**
   * Check if record matches location filter
   */
  matchesLocation(record, locationFilter) {
    // For LinkedIn, we'll use a simple city-based match
    const cities = ['San Francisco', 'New York', 'Austin', 'Seattle', 'Boston', 'Chicago', 'Denver', 'Los Angeles', 'Miami', 'Portland'];
    const recordLocation = cities[Math.floor(Math.random() * cities.length)];
    return recordLocation.toLowerCase().includes(locationFilter.toLowerCase());
  }

  /**
   * Check if record matches experience filter
   */
  matchesExperience(record, experienceFilter) {
    const experience = record.experience_years;
    
    if (experienceFilter.includes('>')) {
      const minYears = parseInt(experienceFilter.replace('>', ''));
      return experience > minYears;
    } else if (experienceFilter.includes('<')) {
      const maxYears = parseInt(experienceFilter.replace('<', ''));
      return experience < maxYears;
    } else if (experienceFilter.includes('-')) {
      const [min, max] = experienceFilter.split('-').map(Number);
      return experience >= min && experience <= max;
    } else {
      const targetYears = parseInt(experienceFilter);
      return Math.abs(experience - targetYears) <= 2; // Within 2 years
    }
  }

  /**
   * Check if record matches skills filter
   */
  matchesSkills(record, requiredSkills) {
    return requiredSkills.some(skill => 
      record.skills.some(recordSkill => 
        recordSkill.toLowerCase().includes(skill.toLowerCase())
      )
    );
  }

  /**
   * Check if record matches department filter
   */
  matchesDepartment(record, departmentFilter) {
    return record.department.toLowerCase().includes(departmentFilter.toLowerCase());
  }

  /**
   * Check if record matches role filter
   */
  matchesRole(record, roleFilter) {
    return record.role.toLowerCase().includes(roleFilter.toLowerCase());
  }

  /**
   * Enhance records with LinkedIn-specific data
   */
  enhanceLinkedInData(records) {
    return records.map(record => {
      // Add LinkedIn-specific fields
      record.linkedin_profile_views = Math.floor(Math.random() * 1000) + 10;
      record.connections_count = Math.floor(Math.random() * 500) + 50;
      record.endorsements_count = Math.floor(Math.random() * 100) + 5;
      record.recommendations_count = Math.floor(Math.random() * 20) + 1;
      
      // Add current company (derived from email domain)
      const emailDomain = record.email.split('@')[1];
      record.current_company = this.generateCompanyFromDomain(emailDomain);
      
      // Add location (derived from phone area code)
      record.location = this.generateLocationFromPhone(record.phone);
      
      // Add profile completeness score
      record.profile_completeness = this.calculateProfileCompleteness(record);
      
      // Add last activity date
      record.last_activity = this.generateLastActivityDate();
      
      return record;
    });
  }

  /**
   * Generate company name from email domain
   */
  generateCompanyFromDomain(domain) {
    const domainToCompany = {
      'gmail.com': 'Freelancer',
      'yahoo.com': 'Independent Consultant',
      'outlook.com': 'Microsoft Partner',
      'company.com': 'Company Inc',
      'techcorp.com': 'TechCorp Solutions'
    };
    
    return domainToCompany[domain] || domain.split('.')[0].charAt(0).toUpperCase() + domain.split('.')[0].slice(1) + ' Corp';
  }

  /**
   * Generate location from phone area code
   */
  generateLocationFromPhone(phone) {
    const areaCodeToCity = {
      '212': 'New York, NY',
      '415': 'San Francisco, CA',
      '310': 'Los Angeles, CA',
      '312': 'Chicago, IL',
      '617': 'Boston, MA',
      '404': 'Atlanta, GA',
      '305': 'Miami, FL',
      '713': 'Houston, TX',
      '214': 'Dallas, TX',
      '206': 'Seattle, WA'
    };
    
    const areaCode = phone.match(/\d{3}/)[0];
    return areaCodeToCity[areaCode] || 'San Francisco, CA';
  }

  /**
   * Calculate profile completeness score
   */
  calculateProfileCompleteness(record) {
    let score = 0;
    const fields = ['name', 'email', 'role', 'department', 'skills', 'phone', 'linkedin', 'education', 'specialization'];
    
    fields.forEach(field => {
      if (record[field] && record[field] !== '') {
        score += 1;
      }
    });
    
    return Math.round((score / fields.length) * 100);
  }

  /**
   * Generate last activity date
   */
  generateLastActivityDate() {
    const now = new Date();
    const daysAgo = Math.floor(Math.random() * 30) + 1; // 1-30 days ago
    const activityDate = new Date(now.getTime() - (daysAgo * 24 * 60 * 60 * 1000));
    return activityDate.toISOString();
  }

  /**
   * Generate API response based on request
   */
  generateApiResponse(requestParams, maxObjects = 500) {
    const { records, metadata } = this.generatePeopleRecords(requestParams, maxObjects);
    
    return {
      status: 'done',
      data: records,
      total_records: records.length,
      generated_at: new Date().toISOString(),
      metadata: metadata
    };
  }
}

module.exports = LinkedInDataGenerator;
