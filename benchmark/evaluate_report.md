# 📊 RazorShield AI — Measured Benchmark Audit Report

Held-Out Test Set: **20,000 Transactions** (Out-of-Time Temporal Split)  
Ground Truth Frauds: **829** (4.15% incidence)

### 📈 Core Statistical & Classification Performance
| Architecture | Precision | Recall | PR-AUC | ROC-AUC | False Positive Rate (FPR) | Avg Latency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Industry Baseline Rules** | 56.51% | 61.28% | 0.346 | 0.796 | 2.04% | 0.00 ms |
| **Standard ML (Default)** | 97.49% | 98.19% | 0.998 | 1.000 | 0.11% | 0.00 ms |
| **RazorShield AI (Ours)** | **95.29%** | **100.00%** | **0.999** | **1.000** | **0.21%** | **0.00 ms** |

### 💰 Unit Economics & Financial Recovery (Held-Out Test Set)
| Architecture | Fraud Loss Prevented | False Positive GMV Loss | **Net GMV Saved (₹)** | Delta vs Baseline |
| :--- | :--- | :--- | :--- | :--- |
| **Industry Baseline Rules** | ₹ 2,780,213.01 | ₹ 211,588.17 | ₹ 2,568,624.84 | Baseline |
| **Standard ML (Default)** | ₹ 15,384,528.13 | ₹ 89,766.79 | ₹ 15,294,761.34 | +495.4% |
| **RazorShield AI (Ours)** | **₹ 15,670,425.55** | **₹ 144,698.79** | **₹ 15,525,726.76** | **+504.4%** |
