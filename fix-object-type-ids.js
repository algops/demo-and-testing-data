const fs = require('fs');
const { v4: uuidv4 } = require('crypto');

// Read object-types.json
const objectTypesData = JSON.parse(fs.readFileSync('object-types.json', 'utf8'));

// Track used IDs to ensure uniqueness
const usedIds = new Set();
const fixedObjectTypes = objectTypesData.object_types.map((objType) => {
  // If ID is already used, generate a new one
  if (usedIds.has(objType.id)) {
    let newId;
    do {
      // Generate UUID v4 format
      newId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    } while (usedIds.has(newId));
    objType.id = newId;
  }
  usedIds.add(objType.id);
  return objType;
});

// Write fixed file
const fixedData = { object_types: fixedObjectTypes };
fs.writeFileSync('object-types.json', JSON.stringify(fixedData, null, 2));
console.log('Fixed duplicate IDs in object-types.json');

// Re-run split script
const path = require('path');
const sampleFileMap = {
  'company': 'companies.json',
  'person': 'persons.json',
  'jobpost': 'jobposts.json',
  'document': 'documents.json',
  'contact': 'contacts.json',
  'organization': 'organizations.json',
  'regulation': 'regulations.json',
  'merge_request': 'merge-requests.json',
  'knowledge_source': 'knowledge-sources.json'
};

// Create object-types directory if it doesn't exist
if (!fs.existsSync('object-types')) {
  fs.mkdirSync('object-types');
}

// Split into individual files and create index
const objectTypes = [];
fixedObjectTypes.forEach((objType) => {
  const fileName = `${objType.id}.json`;
  const filePath = path.join('object-types', fileName);
  
  // Write individual file
  fs.writeFileSync(filePath, JSON.stringify(objType, null, 2));
  
  // Count objects from sample file if it exists
  let object_count = 0;
  const sampleFileName = sampleFileMap[objType.name];
  if (sampleFileName && fs.existsSync(path.join('samples', sampleFileName))) {
    try {
      const sampleData = JSON.parse(fs.readFileSync(path.join('samples', sampleFileName), 'utf8'));
      object_count = Array.isArray(sampleData) ? sampleData.length : (sampleData.objects?.length || 0);
    } catch (e) {
      console.warn(`Could not read sample file for ${objType.name}: ${e.message}`);
    }
  }
  
  // Add to index
  objectTypes.push({
    ...objType,
    object_count
  });
});

// Create index file
const indexData = {
  object_types: objectTypes
};
fs.writeFileSync('object-types/object-types.json', JSON.stringify(indexData, null, 2));

console.log(`Split ${objectTypes.length} object types into individual files with unique IDs`);
