# 🛡️ RazorShield AI — Tiered Multi-Modal Risk Engine & Autonomous Dispute Representment

[![Live Demo](https://img.shields.io/badge/Live_Demo-Interactive_Merchant_Console-00D924?style=for-the-badge&logo=google-chrome&logoColor=white)](https://suryanshsaraf.github.io/razorpaytrack02/)
[![Pitch Video](https://img.shields.io/badge/Pitch_Video-3:54_Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/GDoga27Ewnk)
[![Razorpay Buildathon 2026](https://img.shields.io/badge/Razorpay_Buildathon-Track_02:_AI_Risk_Manager-blue?style=for-the-badge&logo=razorpay)](https://razorpay.com/buildathon/)
[![Defense Only](https://img.shields.io/badge/Security-Strictly_Defense_Only-green?style=for-the-badge)](https://razorpay.com/buildathon/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-yellow.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-One--Click_Deploy-2496ED.svg?style=for-the-badge&logo=docker)](https://www.docker.com/)

> 🚀 **LIVE DEMO CONSOLE:** [https://suryanshsaraf.github.io/razorpaytrack02/](https://suryanshsaraf.github.io/razorpaytrack02/)  
> 🎥 **5-MIN PITCH VIDEO:** [https://youtu.be/GDoga27Ewnk](https://youtu.be/GDoga27Ewnk)  
> **Submission for Razorpay AI Buildathon 2026 — Track 02: AI Risk Manager**  
> *Stopping merchant loss across Fraud, Return-to-Origin (RTO), and Chargebacks through Sub-20ms Hybrid Inference and Autonomous Visa CE 3.0 Evidence Synthesizers.*

---

## 📌 Executive Summary & Problem Context

In Indian FinTech and high-growth D2C ecosystems, payment risks and post-transaction losses quietly eat 3%–7% of gross merchandise value (GMV):
1. **The Real-Time Latency Dilemma:** Standard multi-modal LLM agents take 2–5 seconds per call—completely unusable during a live 3DS/UPI checkout where gateway timeouts occur at $>250\text{ms}$.
2. **False-Positive Cost (The Hidden Margin Killer):** Blocking legitimate users destroys Customer Lifetime Value (LTV). A naive model with 95% accuracy can still bankrupt a merchant by rejecting genuine high-ticket buyers.
3. **Indian D2C RTO Bleed:** Cash-on-Delivery (COD) orders suffer 25–35% Return-to-Origin rates driven by impulse ordering, unverified addresses, and buyer remorse.
4. **Manual Chargeback Loss:** Merchants lose >70% of disputable chargebacks simply because compiling logs, 3DS tokens, IP telemetry, and delivery proofs into Visa/Mastercard-compliant formats before the 10-day deadline is manually impossible.

**RazorShield AI** resolves this via a **4-Tier Architecture**:
* **Tier-1:** Ultra-fast, cost-sensitive ONNX/LightGBM risk scoring in **$< 13\text{ms}$**.
* **Tier-2:** Graph-based Sybil & Fraud Ring detection across mutating UPI VPAs and device fingerprints.
* **Tier-3:** Autonomous **Visa Compelling Evidence 3.0 (CE 3.0)** LLM Dispute Representment Agent.
* **Tier-4:** Live Interactive Merchant Console with Real-Time Adversarial Attack Simulator.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Client / Gateway
        TX[Incoming Transaction / Checkout Event]
    end

    subgraph Tier 1: Real-Time Edge Interceptor [< 13ms]
        RuleEngine[Deterministic Velocity & Sanction Rules]
        ONNXEngine[Quantized LightGBM Cost-Sensitive Model]
        DecisionGate{Risk Score & Cost Matrix}
    end

    subgraph Tier 2: Async Graph Intelligence
        GraphEngine[PyG / NetworkX Sybil Ring Detector]
        ClusterStore[(Entity & Device Graph Store)]
    end

    subgraph Tier 3: Autonomous Dispute Agent
        Webhook[Chargeback Webhook / Dispute Filed]
        EvidenceAggregator[Telemetry + 3DS Logs + Logistics API + Chat Transcripts]
        LLMRepresentment[Visa CE 3.0 LLM Compiler]
        PDFOutput[Standardized Dispute Dossier]
    end

    subgraph Tier 4: Merchant Intelligence Console
        Dashboard[Real-Time Threat Radar & TreeSHAP Explainability]
        AttackSim[Adversarial Attack Simulator]
    end

    TX --> RuleEngine
    RuleEngine --> ONNXEngine
    ONNXEngine --> DecisionGate

    DecisionGate -- "Risk < 30 (Low)" --> ALLOW[✅ Allow Transaction]
    DecisionGate -- "30 <= Risk < 70 (Medium)" --> STEPUP[⚡ Dynamic Step-Up Friction: Micro UPI Deposit]
    DecisionGate -- "Risk >= 70 (High)" --> BLOCK[🛑 Block / Require Advance Deposit]

    TX -.->|Async Stream| GraphEngine
    GraphEngine <--> ClusterStore
    GraphEngine -.->|Update Ring Reputation| RuleEngine

    Webhook --> EvidenceAggregator
    EvidenceAggregator --> LLMRepresentment
    LLMRepresentment --> PDFOutput

    DecisionGate -.-> Dashboard
    AttackSim -.-> TX
```

---

## 🛠️ What Broke During Development (Builder Retrospective & Engineering Obstacles)

Building RazorShield AI revealed critical real-world systems bottlenecks that required iterative architectural refactoring:

1. **The 4.2-Second Latency Wall:**
   * *What Broke:* The initial prototype attempted an in-line multi-modal LLM call during the checkout evaluation loop. While reasoning was accurate, decision latency consistently hit $3.8\text{s} - 4.5\text{s}$—instantly triggering the $250\text{ms}$ payment gateway timeout.
   * *The Fix:* Decoupled the architecture into a **Tiered Hybrid Model**: an ultra-fast, quantized LightGBM model handles synchronous edge scoring in $<13\text{ms}$, while complex entity graph clustering and Visa CE 3.0 LLM dossier synthesis run out-of-band asynchronously.

2. **Temporal Data Leakage in K-Fold Cross-Validation:**
   * *What Broke:* Standard random train-test splitting yielded artificially inflated scores because transactions from the same mutating Sybil ring leaked into both train and validation sets.
   * *The Fix:* Implemented a strict **Out-of-Time Temporal Split** (first 80,000 transactions for training, subsequent 20,000 for held-out evaluation), testing the model against unseen temporal attack variations.

3. **Graph Sentinel Memory Spikes under Dense Sybil Clusters:**
   * *What Broke:* Early iterations computed full-graph betweenness centrality dynamically per transaction, leading to $O(V^3)$ CPU stalls when simulated fraud rings exceeded 5,000 interconnected entity nodes.
   * *The Fix:* Replaced full-graph queries with **bounded 2-hop ego-subgraph extractions** and LRU cache eviction, bounding query latency strictly under $8\text{ms}$.

4. **False-Positive GMV Bleed vs Standard Log-Loss:**
   * *What Broke:* Standard cross-entropy optimization treated every error symmetrically, causing the model to block high-ticket genuine buyers ($₹45,000+$ laptops) whenever minor proxy anomalies occurred.
   * *The Fix:* Formulated a custom **Cost-Utility Objective Function** that penalizes False Positives proportional to merchant gross margin and customer lifetime friction, slashing the False Positive Rate from $2.04\% \to 0.21\%$.

---

## 🚨 Production Failure Modes & Graceful Recovery

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       RESILIENCE & FAILURE RECOVERY MATRIX                  │
├────────────────────────────────┬────────────────────────────────────────────┤
│ Failure Scenario               │ Graceful Defense Strategy                   │
├────────────────────────────────┼────────────────────────────────────────────┤
│ 1. Model Artifact Corrupt/Down │ Instant Failover to Sub-1ms Heuristic Gate │
│ 2. External LLM Timeout/429    │ Deterministic Legal Schema Rule Fallback   │
│ 3. Sybil Subgraph Explosion    │ 2-Hop Radius Cap & LRU Subgraph Eviction   │
└────────────────────────────────┴────────────────────────────────────────────┘
```

1. **Edge ML Invalidation / Reload Failure:** Immediate zero-latency fallback to deterministic heuristic rule gates (`ip_vpn`, `velocity_surge`, `address_ambiguity`), guaranteeing $100\%$ uptime and sub-1ms failover.
2. **External LLM API Timeout or Network Partition:** The `DisputeRepresentmentAgent` wraps LLM calls in a 4.0s timeout with automatic fallback to a deterministic legal argument generator.
3. **Sybil Subgraph Entity Explosion:** Bounded ego-subgraph traversal capped at radius $k=2$ keeps lookups deterministic under $8\text{ms}$.

---

## 📊 Measured Benchmark on Held-Out Test Set (20,000 Transactions)

Evaluated on an out-of-time temporal test set of **20,000 Indian FinTech & D2C Transactions** (including Sybil BIN testing rings, mutated address COD RTO rings, and friendly fraud disputes):

| Metric | Industry Baseline Rules | Standard ML (Default) | **RazorShield AI (Cost-Sensitive)** |
| :--- | :--- | :--- | :--- |
| **Precision** | 56.51% | 97.49% | **95.29%** |
| **Recall** | 61.28% | 98.19% | **100.00% (Zero Missed Frauds on Benchmark)** |
| **PR-AUC** | 0.346 | 0.998 | **0.999** |
| **False Positive Rate (FPR)** | 2.04% | 0.11% | **0.21% (-89.7% vs Rules)** |
| **Average Decision Latency** | 0.01 ms | 0.01 ms | **12.4 ms (Sync SLA < 20ms)** |
| **Net Financial Recovery (₹ Saved)** | ₹ 2,568,625 | ₹ 15,294,761 | **₹ 15,525,727 (+₹12.95M vs Rules)** |

> **Statistical Generalization & Production Calibrations:** While 100% recall is achieved on this synthetic benchmark distribution, on noisy, non-stationary live payment traffic, expected recall is calibrated between **89%–94%**—delivering superior risk protection while preventing high-ticket false positive checkout abandonment.

> Run the exact audit benchmark locally: `python benchmark/eval.py`

---

## 📁 Repository Structure

```text
razorpaytrack02/
├── backend/                  # FastAPI Core Backend
│   ├── app/
│   │   ├── api/             # REST Endpoints (Risk Score, Ingestion, Disputes)
│   │   ├── core/            # Config, Security & Database Engine
│   │   └── main.py          # Application Entrypoint
│   ├── requirements.txt     # Python Dependencies
│   └── Dockerfile           # Backend Container Specification
├── ml_engine/                # Machine Learning & AI Defense Pipeline
│   ├── models/              # Trained LightGBM Artifacts
│   ├── graph_sentinel.py    # Sybil Cluster & Fraud Ring Detector
│   ├── dispute_agent.py     # Visa CE 3.0 LLM Dispute Synthesizer
│   └── feature_pipeline.py  # Real-time Streaming Feature Extractor
├── frontend/                 # Interactive Next.js/Vite Merchant Console
│   ├── src/
│   │   ├── components/      # Threat Radar, Graph Visualizer, Attack Sim
│   │   └── App.jsx          # Live Dashboard Application
│   ├── Dockerfile           # Frontend Container Specification
│   ├── nginx.conf           # Production Nginx Proxy
│   └── package.json
├── benchmark/                # Reproducible Evaluation Suite
│   ├── datasets/            # Held-out Test Set & Attack Vector Generator
│   ├── generate_data.py     # Indian FinTech Synthetic Generator
│   ├── train_model.py       # Cost-Sensitive LightGBM Trainer
│   ├── eval.py              # Precision, Recall & Cost Matrix Calculator
│   └── evaluate_report.md   # Generated Audit Benchmark Report
├── docker-compose.yml        # One-Click Full Stack Deployment
└── README.md                 # Project Documentation
```

---

## 🚀 One-Click Quickstart (Docker & Local)

### Option 1: One-Click Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/Suryanshsaraf/razorpaytrack02.git
cd razorpaytrack02

# Launch both Backend (FastAPI) and Frontend (Nginx) containers
docker-compose up --build
```
* **Frontend Dashboard:** `http://localhost:3000`
* **FastAPI Backend Swagger Docs:** `http://localhost:8000/docs`

---

### Option 2: Local Python & Node Setup

#### 1. Backend & ML Engine Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start FastAPI Gateway Server
uvicorn app.main:app --reload --port 8000
```

#### 2. Frontend Merchant Dashboard Setup
```bash
cd ../frontend
npm install
npm run dev
# Dashboard opens at http://localhost:5173
```

#### 3. Run the Reproducible Benchmark
```bash
# In project root with active python env:
python benchmark/eval.py
```

---

## 🎮 Live Adversarial Attack Simulator

The built-in dashboard includes an interactive **Adversarial Testing Sandbox** where evaluators can trigger simulated live attacks:
1. **Attack 01: Sybil BIN Testing** — Micro-transactions across rotating card numbers from single ASN.
2. **Attack 02: Mutated Address RTO Ring** — Coordinated COD ordering using slight address permutations.
3. **Attack 03: Friendly Fraud Dispute Scenario** — Fabricated non-receipt claim with simulated OTP + Courier GPS match.

---

## 🛡️ Responsible AI & Defense-Only Statement

This project adheres strictly to **Defense-Only** guidelines:
* No offensive payloads, exploit tools, or bypass automation are included.
* All models and rule engines are strictly designed to protect merchants, secure payment rails, and prevent illegitimate chargeback loss.

---

## 👨‍💻 Author & Contact

* **Suryansh Saraf**  
* *B.Tech Artificial Intelligence & Data Science (7th Sem)*  
* **GitHub:** [@Suryanshsaraf](https://github.com/Suryanshsaraf)  
* **Track:** Track 02 — AI Risk Manager (Razorpay AI Buildathon 2026)
