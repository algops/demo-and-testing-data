/**
 * Real Estate API Simulator - Data Generators
 * Generates realistic property listings data
 */

const { generateObject } = require('../../shared/data-generators');
const { calculateFieldCompleteness, calculateDataQualityMetrics } = require('../../shared/logging');

/**
 * Real Estate API data generators
 */
class RealEstateDataGenerator {
  constructor() {
    this.objectType = 'property';
    this.requiredFields = [
      'listing_id', 'street', 'city', 'state', 'zip_code', 'price', 
      'bedrooms', 'bathrooms', 'square_feet', 'property_type', 
      'listing_date', 'status'
    ];
  }

  /**
   * Generate property records based on request parameters
   */
  generatePropertyRecords(requestParams, maxResults = 300) {
    const startTime = Date.now();
    
    // Parse request parameters
    const filters = this.parseFilters(requestParams);
    const recordCount = this.calculateRecordCount(filters, maxResults);
    
    // Generate base records
    let records = generateObject(this.objectType, recordCount);
    
    // Apply real estate specific filters
    records = this.applyRealEstateFilters(records, filters);
    
    // Add real estate specific enhancements
    records = this.enhanceRealEstateData(records);
    
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
    
    if (requestParams.filters) {
      const filterData = typeof requestParams.filters === 'string' 
        ? JSON.parse(requestParams.filters) 
        : requestParams.filters;
        
      if (filterData.city) filters.city = filterData.city;
      if (filterData.state) filters.state = filterData.state;
      if (filterData.price_range) filters.price_range = filterData.price_range;
      if (filterData.bedrooms) filters.bedrooms = filterData.bedrooms;
      if (filterData.bathrooms) filters.bathrooms = filterData.bathrooms;
      if (filterData.property_type) filters.property_type = filterData.property_type;
      if (filterData.square_feet_range) filters.square_feet_range = filterData.square_feet_range;
      if (filterData.zip_code) filters.zip_code = filterData.zip_code;
    }
    
    return filters;
  }

  /**
   * Calculate number of records to generate based on filters
   */
  calculateRecordCount(filters, maxResults) {
    let baseCount = Math.floor(Math.random() * 250) + 50; // 50-300 base records
    
    // Adjust based on filters
    if (filters.city) {
      baseCount = Math.floor(baseCount * 0.7); // Fewer matches with specific city
    }
    
    if (filters.price_range) {
      baseCount = Math.floor(baseCount * 0.8); // Fewer matches with price range
    }
    
    if (filters.bedrooms || filters.bathrooms) {
      baseCount = Math.floor(baseCount * 0.6); // Fewer matches with room filters
    }
    
    if (filters.property_type) {
      baseCount = Math.floor(baseCount * 0.5); // Fewer matches with property type
    }
    
    return Math.min(baseCount, maxResults);
  }

  /**
   * Apply real estate specific filters to generated records
   */
  applyRealEstateFilters(records, filters) {
    return records.filter(record => {
      // City filter
      if (filters.city && !this.matchesCity(record, filters.city)) {
        return false;
      }
      
      // State filter
      if (filters.state && !this.matchesState(record, filters.state)) {
        return false;
      }
      
      // Price range filter
      if (filters.price_range && !this.matchesPriceRange(record, filters.price_range)) {
        return false;
      }
      
      // Bedrooms filter
      if (filters.bedrooms && !this.matchesBedrooms(record, filters.bedrooms)) {
        return false;
      }
      
      // Bathrooms filter
      if (filters.bathrooms && !this.matchesBathrooms(record, filters.bathrooms)) {
        return false;
      }
      
      // Property type filter
      if (filters.property_type && !this.matchesPropertyType(record, filters.property_type)) {
        return false;
      }
      
      // Square feet range filter
      if (filters.square_feet_range && !this.matchesSquareFeetRange(record, filters.square_feet_range)) {
        return false;
      }
      
      // ZIP code filter
      if (filters.zip_code && !this.matchesZipCode(record, filters.zip_code)) {
        return false;
      }
      
      return true;
    });
  }

  /**
   * Check if record matches city filter
   */
  matchesCity(record, cityFilter) {
    return record.city.toLowerCase().includes(cityFilter.toLowerCase());
  }

  /**
   * Check if record matches state filter
   */
  matchesState(record, stateFilter) {
    return record.state.toLowerCase().includes(stateFilter.toLowerCase());
  }

  /**
   * Check if record matches price range filter
   */
  matchesPriceRange(record, priceRange) {
    const price = record.price;
    
    if (priceRange.min && price < priceRange.min) return false;
    if (priceRange.max && price > priceRange.max) return false;
    
    return true;
  }

  /**
   * Check if record matches bedrooms filter
   */
  matchesBedrooms(record, bedroomsFilter) {
    if (typeof bedroomsFilter === 'number') {
      return record.bedrooms === bedroomsFilter;
    } else if (bedroomsFilter.min && bedroomsFilter.max) {
      return record.bedrooms >= bedroomsFilter.min && record.bedrooms <= bedroomsFilter.max;
    } else if (bedroomsFilter.min) {
      return record.bedrooms >= bedroomsFilter.min;
    } else if (bedroomsFilter.max) {
      return record.bedrooms <= bedroomsFilter.max;
    }
    
    return true;
  }

  /**
   * Check if record matches bathrooms filter
   */
  matchesBathrooms(record, bathroomsFilter) {
    if (typeof bathroomsFilter === 'number') {
      return record.bathrooms === bathroomsFilter;
    } else if (bathroomsFilter.min && bathroomsFilter.max) {
      return record.bathrooms >= bathroomsFilter.min && record.bathrooms <= bathroomsFilter.max;
    } else if (bathroomsFilter.min) {
      return record.bathrooms >= bathroomsFilter.min;
    } else if (bathroomsFilter.max) {
      return record.bathrooms <= bathroomsFilter.max;
    }
    
    return true;
  }

  /**
   * Check if record matches property type filter
   */
  matchesPropertyType(record, propertyTypeFilter) {
    return record.property_type.toLowerCase().includes(propertyTypeFilter.toLowerCase());
  }

  /**
   * Check if record matches square feet range filter
   */
  matchesSquareFeetRange(record, squareFeetRange) {
    const squareFeet = record.square_feet;
    
    if (squareFeetRange.min && squareFeet < squareFeetRange.min) return false;
    if (squareFeetRange.max && squareFeet > squareFeetRange.max) return false;
    
    return true;
  }

  /**
   * Check if record matches ZIP code filter
   */
  matchesZipCode(record, zipCodeFilter) {
    return record.zip_code.toString().includes(zipCodeFilter.toString());
  }

  /**
   * Enhance records with real estate specific data
   */
  enhanceRealEstateData(records) {
    return records.map(record => {
      // Add real estate specific fields
      record.agent_name = this.generateAgentName();
      record.agent_phone = this.generateAgentPhone();
      record.agent_email = this.generateAgentEmail(record.agent_name);
      record.mls_number = this.generateMLSNumber();
      record.year_built = this.generateYearBuilt();
      record.lot_size = this.generateLotSize(record.square_feet);
      record.property_taxes = this.calculatePropertyTaxes(record.price, record.city);
      record.hoa_fees = this.calculateHOAFees(record.property_type);
      record.utilities = this.generateUtilitiesInfo();
      record.school_district = this.generateSchoolDistrict(record.city);
      record.nearby_amenities = this.generateNearbyAmenities();
      record.transportation = this.generateTransportationInfo(record.city);
      record.market_analysis = this.generateMarketAnalysis(record);
      record.property_features = this.generatePropertyFeatures(record);
      record.photo_urls = this.generatePhotoUrls(record);
      record.virtual_tour_url = this.generateVirtualTourUrl(record);
      record.open_house_dates = this.generateOpenHouseDates();
      record.price_per_sqft = Math.round(record.price / record.square_feet);
      record.days_on_market = Math.floor(Math.random() * 90) + 1; // 1-90 days
      record.price_history = this.generatePriceHistory(record);
      record.comparable_properties = this.generateComparableProperties(record);
      
      return record;
    });
  }

  /**
   * Generate real estate agent name
   */
  generateAgentName() {
    const firstNames = ['Sarah', 'Michael', 'Jennifer', 'David', 'Lisa', 'Robert', 'Maria', 'James', 'Patricia', 'John'];
    const lastNames = ['Johnson', 'Smith', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
    const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
    const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
    return `${firstName} ${lastName}`;
  }

  /**
   * Generate agent phone number
   */
  generateAgentPhone() {
    const areaCodes = ['212', '415', '310', '312', '617', '404', '305', '713', '214', '206'];
    const areaCode = areaCodes[Math.floor(Math.random() * areaCodes.length)];
    const exchange = Math.floor(Math.random() * 900) + 100;
    const number = Math.floor(Math.random() * 9000) + 1000;
    return `+1-${areaCode}-${exchange}-${number}`;
  }

  /**
   * Generate agent email
   */
  generateAgentEmail(agentName) {
    const [firstName, lastName] = agentName.toLowerCase().split(' ');
    const domains = ['realestate.com', 'properties.com', 'homes.com', 'realtor.com'];
    const domain = domains[Math.floor(Math.random() * domains.length)];
    return `${firstName}.${lastName}@${domain}`;
  }

  /**
   * Generate MLS number
   */
  generateMLSNumber() {
    return `MLS-${Math.floor(Math.random() * 900000) + 100000}`;
  }

  /**
   * Generate year built
   */
  generateYearBuilt() {
    return Math.floor(Math.random() * 50) + 1975; // 1975-2024
  }

  /**
   * Generate lot size based on square footage
   */
  generateLotSize(squareFeet) {
    const lotSizeMultiplier = Math.random() * 3 + 1; // 1-4x the house size
    return Math.round(squareFeet * lotSizeMultiplier);
  }

  /**
   * Calculate property taxes based on price and location
   */
  calculatePropertyTaxes(price, city) {
    const taxRates = {
      'San Francisco': 0.012,
      'Los Angeles': 0.011,
      'New York': 0.013,
      'Chicago': 0.010,
      'Boston': 0.011,
      'Austin': 0.020,
      'Seattle': 0.009,
      'Denver': 0.008,
      'Miami': 0.010,
      'Portland': 0.011
    };
    
    const taxRate = taxRates[city] || 0.011; // Default 1.1%
    return Math.round(price * taxRate);
  }

  /**
   * Calculate HOA fees based on property type
   */
  calculateHOAFees(propertyType) {
    const hoaRates = {
      'Condo': 200,
      'Townhouse': 150,
      'Single Family': 0,
      'Multi-family': 100
    };
    
    const baseFee = hoaRates[propertyType] || 0;
    return baseFee > 0 ? Math.floor(Math.random() * 200) + baseFee : 0;
  }

  /**
   * Generate utilities information
   */
  generateUtilitiesInfo() {
    return {
      heating: ['Gas', 'Electric', 'Heat Pump'][Math.floor(Math.random() * 3)],
      cooling: ['Central Air', 'Window Units', 'None'][Math.floor(Math.random() * 3)],
      water: 'Public',
      sewer: 'Public',
      trash: 'Public'
    };
  }

  /**
   * Generate school district information
   */
  generateSchoolDistrict(city) {
    const schoolDistricts = {
      'San Francisco': 'San Francisco Unified',
      'Los Angeles': 'Los Angeles Unified',
      'New York': 'New York City Department of Education',
      'Chicago': 'Chicago Public Schools',
      'Boston': 'Boston Public Schools',
      'Austin': 'Austin Independent School District',
      'Seattle': 'Seattle Public Schools',
      'Denver': 'Denver Public Schools',
      'Miami': 'Miami-Dade County Public Schools',
      'Portland': 'Portland Public Schools'
    };
    
    return schoolDistricts[city] || 'Local School District';
  }

  /**
   * Generate nearby amenities
   */
  generateNearbyAmenities() {
    const amenities = [
      'Shopping Center', 'Grocery Store', 'Restaurants', 'Coffee Shop',
      'Park', 'Gym', 'Library', 'Bank', 'Pharmacy', 'Gas Station',
      'Hospital', 'School', 'Public Transportation', 'Bike Path'
    ];
    
    const numAmenities = Math.floor(Math.random() * 8) + 5; // 5-12 amenities
    return amenities
      .sort(() => Math.random() - 0.5)
      .slice(0, numAmenities);
  }

  /**
   * Generate transportation information
   */
  generateTransportationInfo(city) {
    const transportation = {
      'San Francisco': ['BART', 'Muni', 'Caltrain', 'Uber/Lyft'],
      'Los Angeles': ['Metro', 'Bus', 'Uber/Lyft', 'Car Required'],
      'New York': ['Subway', 'Bus', 'Taxi', 'Walking'],
      'Chicago': ['CTA', 'Metra', 'Uber/Lyft', 'Biking'],
      'Boston': ['MBTA', 'Bus', 'Uber/Lyft', 'Walking'],
      'Austin': ['CapMetro', 'Uber/Lyft', 'Biking', 'Car Required'],
      'Seattle': ['Sound Transit', 'Bus', 'Uber/Lyft', 'Biking'],
      'Denver': ['RTD', 'Uber/Lyft', 'Biking', 'Car Required'],
      'Miami': ['Metrorail', 'Bus', 'Uber/Lyft', 'Car Required'],
      'Portland': ['TriMet', 'Uber/Lyft', 'Biking', 'Walking']
    };
    
    return transportation[city] || ['Public Transportation', 'Uber/Lyft', 'Car Required'];
  }

  /**
   * Generate market analysis
   */
  generateMarketAnalysis(record) {
    return {
      market_trend: ['Rising', 'Stable', 'Declining'][Math.floor(Math.random() * 3)],
      price_per_sqft: Math.round(record.price / record.square_feet),
      market_competitiveness: ['High', 'Medium', 'Low'][Math.floor(Math.random() * 3)],
      estimated_days_to_sell: Math.floor(Math.random() * 60) + 15, // 15-75 days
      market_insights: this.generateMarketInsights(record)
    };
  }

  /**
   * Generate market insights
   */
  generateMarketInsights(record) {
    const insights = [
      'Great location with high walkability score',
      'Recently renovated with modern amenities',
      'Strong school district attracts families',
      'Investment opportunity with rental potential',
      'Historic charm with character details',
      'Energy efficient with green features',
      'Low maintenance with updated systems',
      'Prime location near transportation hubs'
    ];
    
    const numInsights = Math.floor(Math.random() * 3) + 2; // 2-4 insights
    return insights
      .sort(() => Math.random() - 0.5)
      .slice(0, numInsights);
  }

  /**
   * Generate property features
   */
  generatePropertyFeatures(record) {
    const features = [
      'Hardwood Floors', 'Updated Kitchen', 'Master Suite', 'Walk-in Closet',
      'Fireplace', 'Balcony', 'Patio', 'Garage', 'Driveway', 'Garden',
      'Pool', 'Hot Tub', 'Deck', 'Basement', 'Attic', 'Laundry Room',
      'Pantry', 'Breakfast Nook', 'Formal Dining', 'Home Office'
    ];
    
    const numFeatures = Math.floor(Math.random() * 10) + 5; // 5-14 features
    return features
      .sort(() => Math.random() - 0.5)
      .slice(0, numFeatures);
  }

  /**
   * Generate photo URLs
   */
  generatePhotoUrls(record) {
    const numPhotos = Math.floor(Math.random() * 15) + 10; // 10-24 photos
    const photos = [];
    
    for (let i = 0; i < numPhotos; i++) {
      photos.push(`https://photos.realestate.com/properties/${record.listing_id}/photo_${i + 1}.jpg`);
    }
    
    return photos;
  }

  /**
   * Generate virtual tour URL
   */
  generateVirtualTourUrl(record) {
    return `https://tours.realestate.com/property/${record.listing_id}/virtual-tour`;
  }

  /**
   * Generate open house dates
   */
  generateOpenHouseDates() {
    const dates = [];
    const numOpenHouses = Math.floor(Math.random() * 3) + 1; // 1-3 open houses
    
    for (let i = 0; i < numOpenHouses; i++) {
      const now = new Date();
      const daysFromNow = Math.floor(Math.random() * 14) + 1; // Next 1-14 days
      const openHouseDate = new Date(now.getTime() + (daysFromNow * 24 * 60 * 60 * 1000));
      
      dates.push({
        date: openHouseDate.toISOString().split('T')[0],
        start_time: '12:00 PM',
        end_time: '3:00 PM'
      });
    }
    
    return dates;
  }

  /**
   * Generate price history
   */
  generatePriceHistory(record) {
    const history = [];
    const currentPrice = record.price;
    const numChanges = Math.floor(Math.random() * 3) + 1; // 1-3 price changes
    
    for (let i = 0; i < numChanges; i++) {
      const priceChange = Math.floor(Math.random() * 50000) - 25000; // ±$25k
      const newPrice = Math.max(currentPrice + priceChange, 100000); // Minimum $100k
      
      const changeDate = new Date();
      changeDate.setDate(changeDate.getDate() - (i + 1) * 30); // 30 days apart
      
      history.push({
        price: newPrice,
        date: changeDate.toISOString(),
        change: priceChange,
        change_percent: Math.round((priceChange / (newPrice - priceChange)) * 100)
      });
    }
    
    return history.reverse(); // Oldest first
  }

  /**
   * Generate comparable properties
   */
  generateComparableProperties(record) {
    const comparables = [];
    const numComparables = Math.floor(Math.random() * 3) + 2; // 2-4 comparables
    
    for (let i = 0; i < numComparables; i++) {
      const priceVariation = Math.floor(Math.random() * 100000) - 50000; // ±$50k
      const comparablePrice = Math.max(record.price + priceVariation, 100000);
      
      comparables.push({
        address: `${Math.floor(Math.random() * 9999) + 1} ${['Oak', 'Pine', 'Maple', 'Elm'][Math.floor(Math.random() * 4)]} St`,
        price: comparablePrice,
        bedrooms: record.bedrooms + Math.floor(Math.random() * 3) - 1, // ±1 bedroom
        bathrooms: record.bathrooms + Math.floor(Math.random() * 2), // 0-1 more bathrooms
        square_feet: record.square_feet + Math.floor(Math.random() * 500) - 250, // ±250 sqft
        sold_date: new Date(Date.now() - Math.floor(Math.random() * 90) * 24 * 60 * 60 * 1000).toISOString()
      });
    }
    
    return comparables;
  }

  /**
   * Generate API response based on request
   */
  generateApiResponse(requestParams, maxResults = 300) {
    const { records, metadata } = this.generatePropertyRecords(requestParams, maxResults);
    
    return {
      status: 'done',
      data: records,
      total_records: records.length,
      generated_at: new Date().toISOString(),
      metadata: metadata
    };
  }
}

module.exports = RealEstateDataGenerator;
