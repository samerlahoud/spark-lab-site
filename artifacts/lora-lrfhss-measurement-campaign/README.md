# LoRa and LR-FHSS Measurement Campaign in Halifax

## Overview

This artifact describes the open dataset and demonstration material for a real-world LoRaWAN measurement campaign conducted in Halifax, Nova Scotia, Canada. The campaign directly compares conventional LoRa with Long Range Frequency Hopping Spread Spectrum (LR-FHSS) in the FCC-regulated US915 band.

The full dataset and notebook are maintained in the public repository:

- <https://github.com/AlexisDel/LoRa-LRFHSS-Measurement-Campaign>

The Spark Lab website contribution intentionally links to that repository instead of duplicating the SQLite database in the website repository.

## Campaign summary

- 7,435 measurement points
- approximately one month of measurements, from 5 June to 10 July 2024
- 85 km covered on foot across Halifax
- dense urban and suburban environments
- average walking speed of approximately 4 km/h
- end device at approximately 2 m above ground level
- 22 dBm transmit power
- US915 frequency band
- 4-byte LoRaWAN payload transmitted every 10 seconds
- one Kerlink Wirnet iBTS gateway installed on the Goldberg building at Dalhousie University

## Data-rate configurations

| Data rate | Modulation | Configuration | Coding rate |
| --- | --- | --- | --- |
| DR0 | LoRa | SF10, 125 kHz | 4/5 |
| DR5 | LR-FHSS | 1.523 MHz | 1/3 |
| DR6 | LR-FHSS | 1.523 MHz | 2/3 |

The campaign alternated between the three data rates throughout the measurements.

## Measurement setup

The transmitting node used a Semtech LR1110MB1LCKS shield mounted on an STMicroelectronics NUCLEO-L476RG microcontroller. A Raspberry Pi logged transmitted packet information, while a smartphone supplied GPS coordinates over Wi-Fi.

The receiving side used a Kerlink Wirnet iBTS gateway installed on the roof of the Goldberg building at Dalhousie University. The gateway firmware supported reception of LR-FHSS packets.

## Dataset contents

The main dataset is stored as `database.db`, an SQLite database containing a table named `data`.

Important fields include:

- `date` — packet timestamp
- `freq` — transmission frequency
- `dr` — LoRaWAN data rate
- `bw`, `cr`, `sf` — modulation parameters where applicable
- `power` — transmit power
- `toa` — time on air
- `payload` — LoRa payload stored as a hexadecimal string
- `latitude`, `longitude`, `altitude` — transmitter location
- `gw_distance` — distance to the gateway in kilometres
- `rssic` — received signal strength indicator when the packet is received
- `lsnr` — LoRa signal-to-noise ratio where applicable
- `fdri`, `foff` — frequency-related receiver measurements used for LR-FHSS analysis

The demonstration notebook treats a packet as received when `rssic` is present.

## Example result

The included `preview.png` summarizes the overall packet reception rate reported by the demonstration notebook:

- DR0 / LoRa: 59.8%
- DR5 / LR-FHSS CR 1/3: 79.0%
- DR6 / LR-FHSS CR 2/3: 60.0%

This preview is intended as a compact representative result for the public resource page. The related publication contains the full distance-dependent PRR, path-loss, and RSSI analyses.

## How to use the dataset

Clone the dataset repository and install the lightweight Python dependencies:

```bash
git clone https://github.com/AlexisDel/LoRa-LRFHSS-Measurement-Campaign.git
cd LoRa-LRFHSS-Measurement-Campaign
python3 -m pip install -r requirements.txt
```

Then open the demonstration notebook:

```bash
jupyter notebook demo.ipynb
```

The notebook shows how to load `database.db`, inspect the measurements, summarize the three data rates, and compute packet reception rate by distance.

## Related publication

A. Delplace, S. Lahoud, K. Khawam, “Exploring LR-FHSS Modulation for Enhanced IoT Connectivity: A Measurement Campaign,” *2025 IEEE 102nd Vehicular Technology Conference (VTC2025-Fall)*, pp. 1–7, 2025.

- DOI: <https://doi.org/10.1109/VTC2025-Fall65116.2025.11309920>
- Open preprint: <https://arxiv.org/abs/2510.23152>

## License

The public dataset repository is released under the MIT License.

## Maintainers

- Alexis Delplace
- Samer Lahoud
