# verify_energy_proof.py
import json
from utils import load_json, recompute_energy_from_preview

def verify_ed25519(pub_hex: str, message: bytes, sig_hex: str) -> bool:
    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        pub = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex))
        pub.verify(bytes.fromhex(sig_hex), message)
        return True
    except Exception:
        return False

def main():
    proof = load_json("data/energy_proof_of_creation.json")
    sensor = load_json("data/energy_sensor_simulation.json")
    msg = proof["message_signed"].encode("utf-8")
    ok = verify_ed25519(proof["public_key_hex"], msg, proof["signature_hex"]) if proof["signing_method"]=="ed25519" else False
    energy_preview = recompute_energy_from_preview(sensor)
    print("=== Verification Report ===")
    print(f"Signature verification: {ok} (method: {proof['signing_method']})")
    print(f"Energy from preview (J): {energy_preview:.9f}")
    print(f"Claimed energy (J): {proof['energy_joules']:.9f}")
    print(f"Difference (J): {proof['energy_joules']-energy_preview:.9f}")
    if proof["signing_method"]!="ed25519":
        print("HMAC fallback used; public verification not available.")
if __name__ == "__main__":
    main()
