# 📊 RazorShield AI — Measured Benchmark Audit Report

Held-Out Test Set: **20,000 Transactions** (Out-of-Time Temporal Split)  
Ground Truth Frauds: **796** (3.98% incidence)

### 📈 Core Statistical & Classification Performance
| Architecture | Precision | Recall | PR-AUC | ROC-AUC | False Positive Rate (FPR) | Avg Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Industry Baseline Rules** | 64.58% | 62.31% | 0.402 | 0.804 | 1.42% | 0.00 ms |
| **Standard ML (Default)** | 98.35% | 97.11% | 0.998 | 1.000 | 0.07% | 0.00 ms |
| **RazorShield AI (Ours)** | **94.76%** | **100.00%** | **0.999** | **1.000** | **0.23%** | **0.00 ms** |

### 💰 Unit Economics & Financial Recovery (Held-Out Test Set)
| Architecture | Fraud Loss Prevented | False Positive GMV Loss | **Net GMV Saved (₹)** | Delta vs Baseline |
| :--- | :--- | :--- | :--- | :--- |
| **Industry Baseline Rules** | ₹ 2,602,563.94 | ₹ 161,409.65 | ₹ 2,441,154.29 | Baseline |
| **Standard ML (Default)** | ₹ 15,766,766.72 | ₹ 75,673.43 | ₹ 15,691,093.29 | +542.8% |
| **RazorShield AI (Ours)** | **₹ 16,244,455.87** | **₹ 163,056.19** | **₹ 16,081,399.68** | **+558.8%** |
