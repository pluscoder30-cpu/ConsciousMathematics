# utils.py
import json, hashlib, math
def load_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)
def recompute_energy_from_preview(sensor_json: dict) -> float:
    times = sensor_json.get("times", [])
    volts = sensor_json.get("volts_preview", [])
    amps = sensor_json.get("amps_preview", [])
    if len(times) < 2: return 0.0
    dt = times[1] - times[0]
    return sum((v*i)*dt for v,i in zip(volts, amps))
