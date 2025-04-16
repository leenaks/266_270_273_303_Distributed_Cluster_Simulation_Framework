# Distributed Systems Cluster Simulation Framework

A cloud computing project implementing a container orchestration system similar to Kubernetes.

## Project Overview
This project implements a simplified container orchestration system with the following components:
- API Server
- Node Manager
- Pod Scheduler
- Health Monitor
- Node Heartbeat Mechanism

## Weekly Milestones

### Week 1 (15 Marks)
- [ ] Implement API Server base implementation
- [ ] Implement Node Manager functionality
- [ ] Add Node functionality (CPU core allocation and container launch)

### Week 2 (15 Marks)
- [ ] Implement Pod Scheduler
- [ ] Implement Health Monitor with node heartbeat mechanism
- [ ] Implement Pod launch functionality with automatic node assignment

### Week 3 (10 Marks)
- [ ] Implement Node listing with health status
- [ ] System testing
- [ ] Documentation

## Project Structure
```
src/
├── api/           # API Server implementation
├── node/          # Node Manager and Node functionality
├── scheduler/     # Pod Scheduler implementation
├── monitor/       # Health Monitor implementation
└── common/        # Shared utilities and types
```

## Getting Started
1. Clone the repository
2. Install dependencies
3. Run the development server

## Dependencies
- Node.js
- Docker
- Express.js

## License
MIT 