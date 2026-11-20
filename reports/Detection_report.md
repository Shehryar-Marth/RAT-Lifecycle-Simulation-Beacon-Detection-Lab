# Detection Report — Beaconing Analysis

## 1. Objective
Demonstrate detection of fixed-interval vs jittered C2 beaconing
in a localhost lab.

## 2. Method
- Fixed beacon: 6-byte payload, 5s interval, port 4444
- Jittered beacon: 6-byte payload, 5s ±2s, port 4445
- Capture: Wireshark, loopback interface

## 3. Observations
| Property | Fixed | Jitter |
| :--- | :--- | :--- |
| Mean interval | 5.00s | X.XXs |
| Std. deviation | ~0 | X.XXs |
| Payload size | 6 B | 6 B |
| Port | 4444 | 4445 |

## 4. Detection
- Sigma rule: `rules/beacon_fixed.yml`
- Payload-size fingerprinting still catches jitter
- Jitter defeats naive interval counting — combine signals

## 5. Conclusion
Multi-signal detection (timing variance + payload fingerprint +
destination reputation) is required against jittered C2.
