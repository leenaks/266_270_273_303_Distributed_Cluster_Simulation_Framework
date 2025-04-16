const fs = require('fs').promises;
const path = require('path');

const NODES_FILE = path.join(__dirname, '../../data/nodes.json');

async function loadNodes() {
  try {
    const data = await fs.readFile(NODES_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    if (err.code === 'ENOENT') {
      // File doesn't exist, return empty array
      return [];
    }
    throw err;
  }
}

async function saveNodes(nodes) {
  await fs.writeFile(NODES_FILE, JSON.stringify(nodes, null, 2), 'utf8');
}

module.exports = {
  loadNodes,
  saveNodes
}; 