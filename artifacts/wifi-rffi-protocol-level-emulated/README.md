# Wi-Fi RFFI Protocol-Level Emulated Traces

## Overview

Protocol-level emulated Wi-Fi 802.11 signal traces for RFFI-based impersonation detection. Signals are emulated using GNU Radio with device-specific hardware impairments including CFO and IQ imbalance, along with basic channel effects.

## Contents

- 4 legitimate device files: `legitimate_device_01.npy` to `legitimate_device_04.npy`
- 4 attacker device files: `attacker_device_05_impersonates_01.npy` to `attacker_device_08_impersonates_04.npy`
- `scripts/analyze.py`: feature extraction and XGBoost classification with confusion matrix

## Dataset Details

- Signal format: complex64 IQ samples
- Packet length: 3840 samples per packet
- Attacker devices share the MAC address of their target legitimate device

| File | Type | Packets |
|------|------|---------|
| `legitimate_device_01.npy` | Legitimate | 7919 |
| `legitimate_device_02.npy` | Legitimate | 8299 |
| `legitimate_device_03.npy` | Legitimate | 7595 |
| `legitimate_device_04.npy` | Legitimate | 8854 |
| `attacker_device_05_impersonates_01.npy` | Attacker | 1351 |
| `attacker_device_06_impersonates_02.npy` | Attacker | 1167 |
| `attacker_device_07_impersonates_03.npy` | Attacker | 1630 |
| `attacker_device_08_impersonates_04.npy` | Attacker | 1999 |

## Related Paper

X. Li, S. Lahoud, N. Zincir-Heywood, "Unsupervised Anomaly Detection for Wi-Fi Networks using RFFI," 2025 21st International Conference on Network and Service Management (CNSM), 2025.
https://doi.org/10.23919/CNSM67658.2025.11297558

## How to Use

1. Download the dataset from Zenodo: https://doi.org/10.5281/zenodo.20186947
2. Place the `.npy` files in a `data/` folder next to `scripts/`
3. Install dependencies:
```bash
   pip install numpy matplotlib scikit-learn xgboost scipy
```
4. Run the analysis script:
```bash
   python scripts/analyze.py
```
   Output figures will be saved to `output/`.

## Maintainers

- Xinyi Li
- Samer Lahoud