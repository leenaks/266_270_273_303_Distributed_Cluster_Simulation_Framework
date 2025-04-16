const express = require('express');
const cors = require('cors');
const { loadNodes, saveNodes } = require('../common/storage');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize nodes array
let nodes = [];

// Load existing nodes on startup
loadNodes()
  .then(loadedNodes => {
    nodes = loadedNodes;
    console.log('Loaded existing nodes:', nodes);
  })
  .catch(err => {
    console.error('Error loading nodes:', err);
  });

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// List all nodes
app.get('/nodes', (req, res) => {
  res.json(nodes);
});

// Add a new node
app.post('/nodes', (req, res) => {
  const { name, capacity } = req.body;
  
  if (!name || !capacity) {
    return res.status(400).json({ error: 'Name and capacity are required' });
  }

  const newNode = {
    id: Date.now().toString(),
    name,
    capacity,
    status: 'active',
    pods: []
  };

  nodes.push(newNode);
  saveNodes(nodes)
    .then(() => res.status(201).json(newNode))
    .catch(err => res.status(500).json({ error: 'Failed to save node' }));
});

// Start the server
app.listen(PORT, () => {
  console.log(`API Server running on port ${PORT}`);
}); 