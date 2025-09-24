# Consciousness Energy: Proof-of-Creation (Signed PoC)

**Status:** Computational Proof-of-Concept (Simulation, not hardware)  
**Goal:** Show a *verifiable*, cryptographically signed artifact that encodes an energy computation derived from voltage/current samples.  
**Why:** Claims are easy; verification is hard. This repo demonstrates a minimal pipeline that anyone can run to reproduce the calculation and verify the signature.

## What this does
- Simulates a short "energy extraction" run (voltage & current arrays).
- Computes instantaneous power and integrates to get energy in joules (and Wh).
- Produces a canonical JSON proof artifact and signs it (Ed25519 if available; HMAC fallback otherwise).
- Provides a verification script that checks the signature and recomputes energy from preview data.

> **Disclaimer:** This is a *simulation* used to demonstrate reproducible, signed evidence formatting. It is **not** a claim of real hardware energy extraction.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/verify_energy_proof.py
```
You should see a verification report. If your environment supports Ed25519 (via `cryptography`), signature verification will be **True**.

## Regenerate new proof artifacts
```bash
python scripts/simulate_and_sign_energy.py
python scripts/verify_energy_proof.py
```

## Files
- `data/energy_sensor_simulation.json` — simulated time samples (preview), summary stats, sensor-salt derivation
- `data/energy_proof_of_creation.json` — signature + public key + canonical message
- `scripts/simulate_and_sign_energy.py` — regenerate the dataset and proof
- `scripts/verify_energy_proof.py` — verify signature and recompute energy from preview arrays
- `scripts/utils.py` — helpers

## How to use this for real experiments
Replace the simulator with **real**, **calibrated** measurements:
1. Log synchronized **voltage (V)** and **current (A)** with timestamps or fixed sampling rate.
2. Integrate instantaneous power (P=V·I) to compute energy. Include uncertainties and instrument calibration.
3. Create the canonical JSON message with metadata (instruments, wiring, conditions).
4. Sign the message with a hardware-backed key and publish the **public key**.
5. Share raw data + proof so anyone can reproduce and verify.

## SEO / Topics
`consciousness`, `energy`, `proof-of-creation`, `cryptographic-proof`, `Ed25519`, `signed-artifacts`, `reproducible-science`, `open-science`, `simulation`, `data-signing`

## License
MIT
