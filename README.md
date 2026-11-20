# RAT-Lifecycle-Simulation-Beacon-Detection-Lab
Built a safe RAT lifecycle simulation (6 stages, no harmful capability), mapped to MITRE ATT&amp;CK with detection signals. Added a localhost beacon lab, detected fixed vs jittered C2 in Wireshark, and authored a Sigma rule.
# Trojan Lifecycle Lab — Educational Simulation & Beacon Detection

**Purpose:** Understand how a Remote Access Trojan (RAT) operates
across its lifecycle, and how to detect each stage — *without
implementing any harmful capability.*

## ⚠️ Safety
- Localhost only (127.0.0.1)
- No persistence, no execution, no file access, no exfiltration
- Fixed low-entropy payload, for detection practice only
- Run only on a machine you own or in an isolated VM

## Contents
| File | Description |
| :--- | :--- |
| `trojan_lab.py` | Simulation + fixed/jittered beacons |
| `reports/detection_report.md` | ATT&CK mapping + detection notes |
| `screenshots/` | Wireshark IO graphs (fixed vs jittered) |

## Usage
```bash
python trojan_lab.py simulate
python trojan_lab.py beacon-fixed
python trojan_lab.py beacon-jitter
