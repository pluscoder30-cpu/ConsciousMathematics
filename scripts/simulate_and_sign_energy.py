# simulate_and_sign_energy.py
import os, json, math, random, hashlib, hmac
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

SOUL_CODE = "425-434-266-775"
PHI = 1.618033988749895
CONSCIOUSNESS_FREQ = 528

def simulate_energy_run(duration_s=8.0, sample_rate=128, base_voltage=0.5, base_current=0.02, fluctuation=0.4):
    n = int(duration_s * sample_rate)
    times = [i / sample_rate for i in range(n)]
    volts, amps = [], []
    for t in times:
        eff_freq = CONSCIOUSNESS_FREQ % sample_rate
        pulse = 0.5 * (1 + math.sin(2*math.pi*eff_freq*t))
        v = base_voltage * (1 + fluctuation * pulse * (PHI - 1)) + random.gauss(0, 0.005)
        i = base_current * (1 + fluctuation * pulse * 0.5) + random.gauss(0, 0.0005)
        volts.append(v); amps.append(i)
    return times, volts, amps

def main():
    times, volts, amps = simulate_energy_run()
    powers = [v*i for v,i in zip(volts, amps)]
    dt = times[1] - times[0] if len(times)>1 else 1.0
    energy_j = sum(p*dt for p in powers)
    energy_wh = energy_j/3600.0
    mean_v = sum(volts)/len(volts)
    mean_i = sum(amps)/len(amps)
    rms_p = (sum(p*p for p in powers)/len(powers))**0.5
    feature_seed = f"{mean_v:.8f}|{mean_i:.8f}|{rms_p:.8f}|{len(times)}"
    sensor_salt = hashlib.sha256(feature_seed.encode()).hexdigest()

    seed_str = f"{SOUL_CODE}|phi_pow={PHI**PHI:.12f}|freq={CONSCIOUSNESS_FREQ}|sensor={sensor_salt}"
    derived_seed = hashlib.sha256(seed_str.encode()).digest()

    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        seed32 = derived_seed[:32]
        priv = ed25519.Ed25519PrivateKey.from_private_bytes(seed32)
        pub = priv.public_key()
        proof_msg = json.dumps({
            "type":"energy_proof","created_at":datetime.now(timezone.utc).isoformat(),
            "energy_joules":energy_j,"energy_wh":energy_wh,
            "duration_s": times[-1]-times[0], "sample_count":len(times),
            "feature_seed":feature_seed
        }, sort_keys=True).encode("utf-8")
        sig = priv.sign(proof_msg)
        signature_hex = sig.hex()
        pub_bytes = pub.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
        public_key_hex = pub_bytes.hex()
        signing_method = "ed25519"
    except Exception:
        signing_method = "hmac_fallback"
        proof_msg = json.dumps({
            "type":"energy_proof","created_at":datetime.now(timezone.utc).isoformat(),
            "energy_joules":energy_j,"energy_wh":energy_wh,
            "duration_s": times[-1]-times[0], "sample_count":len(times),
            "feature_seed":feature_seed
        }, sort_keys=True).encode("utf-8")
        signature_hex = hmac.new(derived_seed, proof_msg, hashlib.sha256).hexdigest()
        public_key_hex = hashlib.sha256(derived_seed).hexdigest()

    sensor_out = {
        "meta":{"created_at":datetime.now(timezone.utc).isoformat(),"note":"SIMULATED_SENSOR_DATA"},
        "params":{"duration_s": times[-1], "sample_rate":128, "consciousness_freq":CONSCIOUSNESS_FREQ},
        "feature_seed": feature_seed, "sensor_salt": sensor_salt,
        "times": times[:200], "volts_preview": volts[:200], "amps_preview": amps[:200],
        "powers_preview": [v*i for v,i in zip(volts[:200], amps[:200])],
        "summary":{"mean_v":mean_v,"mean_i":mean_i,"rms_p":rms_p,"energy_joules":energy_j,"energy_wh":energy_wh}
    }
    with open(os.path.join(DATA_DIR, "energy_sensor_simulation.json"), "w") as f:
        json.dump(sensor_out, f, indent=2)

    proof = {
        "proof_type":"energy_extraction_simulation_proof",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "description":"Signed proof of a simulated energy run (computational PoC).",
        "energy_joules": energy_j,"energy_wh": energy_wh,
        "duration_s": times[-1]-times[0],"sample_count": len(times),
        "feature_seed": feature_seed,"sensor_salt": sensor_salt,
        "signing_method": signing_method,"public_key_hex": public_key_hex,
        "signature_hex": signature_hex,"message_signed": proof_msg.decode("utf-8")
    }
    with open(os.path.join(DATA_DIR, "energy_proof_of_creation.json"), "w") as f:
        json.dump(proof, f, indent=2)

    print("Wrote data/energy_sensor_simulation.json and data/energy_proof_of_creation.json")

if __name__ == "__main__":
    main()
