# RealSignal

RealSignal is a real-time streaming fraud detection and anomaly detection system built using Kafka, FastAPI, and Isolation Forest.

The system simulates financial transactions, streams them through Kafka, computes behavioral features in real time, and detects anomalous transactions using machine learning.


## Features

- Real-time transaction streaming using Kafka
- Online feature engineering
- Isolation Forest based anomaly detection
- Fraud transaction simulation
- FastAPI prediction and monitoring endpoints
- Dead Letter Queue (DLQ) for failed events
- Fault-tolerant consumer architecture
- Structured logging
- Dockerized setup



## Tech Stack

- Python
- FastAPI
- Kafka
- Zookeeper
- Scikit-learn
- Docker
- Pydantic



## Current System Flow

Transaction Simulator  
→ Kafka Producer  
→ Kafka Topic  
→ Kafka Consumer  
→ Feature Engineering  
→ Isolation Forest Inference  
→ Logging & Alerting

Failed events are routed to a Dead Letter Queue (DLQ).



## Reliability Features

- Schema validation fault isolation
- Inference-stage fault isolation
- DLQ-based failed event routing
- DLQ consumer for failed event inspection


