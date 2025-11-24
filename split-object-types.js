const fs = require('fs');
const path = require('path');

// Read object-types.json
const objectTypesData = JSON.parse(fs.readFileSync('object-types.json', 'utf8'));

// Create object-types directory if it doesn't exist
if (!fs.existsSync('object-types')) {
  fs.mkdirSync('object-types');
}

// Map object type names to sample file names
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

// Split into individual files and create index
const objectTypes = [];
objectTypesData.object_types.forEach((objType) => {
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

console.log(`Split ${objectTypes.length} object types into individual files`);
console.log(`Created object-types/object-types.json index`);
