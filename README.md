# InsideEdge — Smart Detection of Insider Threats

A smart security system that helps banks detect insider threats early by continuously monitoring employee activity, analyzing behavioral patterns, and flagging suspicious actions using graph database technology.

---

## The Problem

Traditional cybersecurity tools are built to detect external attacks. Insider threats — where the risk comes from within the organization — are among the hardest security risks to detect. Employees with legitimate access can cause significant damage, and most systems have no way to catch unusual behavior before damage occurs.

## What InsideEdge Does

InsideEdge monitors employee activity logs in real time, models relationships between employees, devices, and data assets using a graph database, and assigns dynamic risk scores to flag potential threats before they escalate.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Neo4j | Graph database for modeling relationships (Cypher queries) |
| Scikit-learn | ML-based anomaly detection |
| Matplotlib | Data visualization |
| Flask | Web dashboard backend |

---

## How It Works

**1. Data Collection**
Employee activity logs are gathered — including login details, transaction logs, and communication logs.

**2. Graph-Based Behavioral Model**
A Neo4j graph scheme maps relationships between employees, devices, data assets, and actions. This makes behavioral patterns visible and easy to analyze.

**3. Rule-Based Threat Detection**
A rule engine flags suspicious behaviors based on:
- Unusual login and logout times
- High volume of sensitive file access
- Large or abnormal transaction amounts
- Type of files accessed

**4. Risk Scoring**
Each user is assigned a dynamic risk score based on their actions, helping prioritize which users need immediate investigation.

**5. Interactive Web Dashboard** 
A Flask-based dashboard displays alerts, activity trends, and risk scores in a clear, easy-to-understand format.

---

## Project Architecture

```
Activity Logs (Login + Transactions + Communication)
        ↓
Graph-Based Behavioural Model (Neo4j)
        ↓
Rule-Based Threat Detection Engine
        ↓
Anomaly Detection Module (Scikit-learn)
        ↓
Risk Scoring System
        ↓
Interactive Web Dashboard 
```

---

## Outcomes

- Realistic bank log data simulation for threat modeling
- Graph-based visualization of employee behavior patterns
- Dynamic user risk scores updated in real time
- Alert system via web dashboard for security teams

---

## What I Learned

Building InsideEdge taught me that security is as much about understanding human behavior as it is about technology. Modeling relationships between people, devices, and actions using a graph database gave me a completely different perspective on how data can tell a story — and how that story can protect real organizations from real harm.

---

## Future Scope

- Integrate real-time streaming data using Kafka
- Expand ML model with larger labeled datasets
- Add role-based access control to the dashboard
- Deploy as a cloud-native microservice
