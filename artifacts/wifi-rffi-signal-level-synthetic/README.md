# Wi-Fi RFFI Signal-Level Synthetic Traces

## Overview

Synthetic Wi-Fi signal traces generated at the bit level for RFFI-based impersonation detection. Each signal includes a random payload and a header encoding device identity, modulated using 16-QAM and OFDM. Hardware impairments such as CFO, IQ imbalance, phase noise, and non-linear distortions are introduced, along with AWGN and Rayleigh fading channel effects.

## Contents

- `data/legitimate/` — IQ traces for 4 legitimate devices
- `data/attacker/` — IQ traces for 4 attacker devices, each impersonating a legitimate device
- `scripts/analyze.py` — Feature extraction and XGBoost classification with confusion matrix

## Related Paper

X. Li, S. Lahoud, N. Zincir-Heywood, "Unsupervised Anomaly Detection for Wi-Fi Networks using RFFI," 2025 21st International Conference on Network and Service Management (CNSM), 2025.
https://doi.org/10.23919/CNSM67658.2025.11297558

## How to Use

1. Clone the repository
2. Install dependencies:
```bash
   pip install numpy matplotlib scikit-learn xgboost scipy
```
3. Run the analysis script:
```bash
   python scripts/analyze.py
```
   Output figures will be saved to `output/`.

## Maintainers

- Xinyi Li
- Samer Lahoud